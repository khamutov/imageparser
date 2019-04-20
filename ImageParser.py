# coding=utf-8
import csv
import json
import shutil
import urllib.request
import os
import asyncio
from pathlib import Path

import aiohttp as aiohttp
from tqdm import tqdm

from Decorators import make_dirs

sem = asyncio.Semaphore(3)
valid_pct=0.2
train_pct=0.2

def move_images_to_folder(path_src:Path, path_dist: Path, dir_name:str, images : []):
    for image in tqdm(images,desc="move images to {} len {}".format(dir_name,len(images))):
        if not path_dist.joinpath(image).is_file():
            shutil.copyfile(src=path_src.joinpath(image),dst=path_dist.joinpath(image))

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
                    print("download",url)
                    f.write(await response.read())


    async def __save_images(self, url: str, dir_name: str, path: Path):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for image in (self.__get_images_array(url)):
                if not path.joinpath(self.__get_last_segment(image)).is_file():
                    tasks.append(self.__fetch(image, session, path))

            for task in tqdm(tasks, desc="download {}".format(dir_name)):
                await task
        images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        validation_idx = round(len(images) * valid_pct)
        test_idx = round(validation_idx + len(images) * train_pct)
        move_images_to_folder(path,path.joinpath("train"),"train",images[:validation_idx])
        move_images_to_folder(path,path.joinpath("test"),"test",images[validation_idx: test_idx])
        move_images_to_folder(path,path.joinpath("validation"),"validation",images[test_idx:])




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
                loop.run_until_complete(self.__save_images(row["url"], row["dir_name"], path))


if __name__ == "__main__":
    ImageParser().image_parser()
