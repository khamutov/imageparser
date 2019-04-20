import csv
import json
import random
import shutil
import urllib.request
import os
import asyncio
from pathlib import Path

import aiohttp as aiohttp
from tqdm import tqdm

from Decorators import make_dirs

sem = asyncio.Semaphore(3)


def move_images_to_folder(path: Path, arr: [], file="categories.csv"):
    random.shuffle(arr)
    with open(file, "r") as f:
        reader = csv.DictReader(f, ["section", "percent"], delimiter=";")
        last = int(0)
        for row in reader:
            for image in tqdm(arr[last:
            round(last + round(len(arr) * int(row.get("percent"))) / 100)], desc="move images:"):
                shutil.copyfile(src=path.joinpath(image),
                                dst=path.joinpath(row.get("section")).joinpath(image))
            last = round(last + round(len(arr) * int(row.get("percent"))) / 100)


class ImageParser:
    def __get_images_array(self, url: str) -> []:
        array = []
        for item in self.__get_response(url):
            for image in item.get("images"):
                array.append(image)
        return array

    async def __fetch(self, url, session, path: Path):
        async with sem:
            async with session.get(url) as response:
                with open(path.joinpath(self.__get_last_segment(str(response.url))), 'wb') as f:
                    f.write(await response.read())


    async def __save_images(self, url: str, path: Path):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for image in (self.__get_images_array(url)):
                if not path.joinpath(self.__get_last_segment(image)).is_file():
                    tasks.append(self.__fetch(image, session, path))

            for task in tqdm(tasks, desc="download: "):
                await task

        move_images_to_folder(path, [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])


    def __get_response(self, url: str) -> str:
        return json.load(urllib.request.urlopen(url=url)).get("data")


    def __get_last_segment(self, url: str) -> str:
        return str(Path(url).name.split("?")[0])


    def image_parser(self, file_name: str = "url.csv"):
        file = Path(file_name)
        if not file.is_file():
            raise Exception("file not found")

        with open(file, "r") as f:
            reader = csv.DictReader(f, ["url", "dir_name"], delimiter=";")
            for row in tqdm(reader, desc="Done: "):
                path = Path(row["dir_name"])
                make_dirs(path)
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.__save_images(row["url"], path))


if __name__ == "__main__":
    ImageParser().image_parser()
