# coding=utf-8
import csv
import json
import shutil
import urllib.request
import asyncio
from pathlib import Path

import aiohttp as aiohttp
from tqdm import tqdm

from MoveImagesToFolder import MoveImages

sem = asyncio.Semaphore(3)

file_name = "url.csv"

path_to = ""


def move_images_to_folder(path_src: Path, path_to: Path, path_dist: Path, dir_name: str, images: []):
    for image in tqdm(images, desc="move images to {} len {}".format(dir_name, len(images))):
        if not path_dist.joinpath(image).is_file():
            shutil.copyfile(src=path_src.joinpath(image), dst=path_to.joinpath(path_dist.joinpath(image)))


class ImageParser:
    def __get_images_array(self, url: str) -> []:
        array = []
        for item in self.__get_response(url):
            for image in item.get("images"):
                array.append(image)
        return array

    async def __fetch(self, path_to: Path, url, session, path: Path):
        async with sem:
            async with session.get(url) as response:
                temp = path_to.joinpath(path.joinpath(self.__get_last_segment(str(response.url))))
                with open(temp, 'wb') as f:
                    f.write(await response.read())

    async def __save_images(self, path_to: Path, url: str, dir_name: str, path: Path):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for image in (self.__get_images_array(url)):
                if not path_to.joinpath(path.joinpath(self.__get_last_segment(image))).is_file():
                    tasks.append(self.__fetch(path_to, image, session, path))

            for task in tqdm(tasks, desc="download {}".format(dir_name)):
                await task

    def __get_response(self, url: str) -> str:
        return json.load(urllib.request.urlopen(url=url)).get("data")

    def __get_last_segment(self, url: str) -> str:
        return str(Path(url).name.split("?")[0])

    def image_parser(self, path_to: Path, file_name: str = "url.csv"):
        file = Path(file_name)
        with open(file, "r") as f:
            reader = csv.DictReader(f, ["url", "dir_name"], delimiter=";")
            for row in tqdm(reader):
                path = Path(row["dir_name"])
                path_to.joinpath(path).mkdir(parents=True, exist_ok=True)
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.__save_images(path_to,row["url"], row["dir_name"], path))


if __name__ == "__main__":
    with open(file_name, "r") as f:
        ImageParser().image_parser(path_to=Path('images'))
        MoveImages().move_images(path_from=Path('images'), path_to=Path('images_net'))
