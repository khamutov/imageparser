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
from MoveImagesToFolder import MoveImages

sem = asyncio.Semaphore(3)
file_name = "url.csv"

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

    def __get_response(self, url: str) -> str:
        return json.load(urllib.request.urlopen(url=url)).get("data")


    def __get_last_segment(self, url: str) -> str:
        return str(Path(url).name.split("?")[0])

    def image_parser(self, file_name: str = "url.csv"):
        file = Path(file_name)
        with open(file, "r") as f:
            reader = csv.DictReader(f, ["url", "dir_name"], delimiter=";")
            for row in tqdm(reader):
                path = Path(row["dir_name"])
                make_dirs(path)
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.__save_images(row["url"], row["dir_name"], path))

if __name__ == "__main__":
    with open(file_name,"r") as f:
        ImageParser().image_parser()
        reader = csv.DictReader(f, ["url", "dir_name"], delimiter=";")
        for row in reader:
            path = Path(row["dir_name"])
            images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            move_images = MoveImages(images)
            for dir in move_images.dir_name:
                move_images.move_images(path_from=path,path_to=path.joinpath(dir))



