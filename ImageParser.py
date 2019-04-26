# coding=utf-8
import csv
import json
import urllib.request
import urllib.parse
import asyncio
import aiofiles as aiof
from pathlib import Path

import aiohttp as aiohttp
from tqdm import tqdm

from CollectMeta import Meta
from MoveImagesToFolder import MoveImages

sem = asyncio.Semaphore(15)

file_name = "url.csv"
max_page = 2


class ImageParser:
    @classmethod
    def __get_images_array(cls, data: [], path_to: Path) -> []:
        array = []
        for item in data:
            for image in item.get("images"):
                image = image.split("?").pop(0)
                if not path_to.joinpath(cls.__get_last_segment(image)).is_file():
                    array.append(image)
        return array

    @classmethod
    async def __fetch(cls, path_to: Path, dir_name: Path, url: str):
        async with sem:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url) as response:
                    temp = path_to.joinpath(dir_name.joinpath(cls.__get_last_segment(str(response.url))))
                    async with aiof.open(temp, 'wb') as f:
                        await f.write(await response.read())

    @classmethod
    async def __save_images(cls, path_to: Path, path_dir_name: Path, url: str):
        cls.last_page = -1
        for i in range(1, max_page + 1):
            if cls.last_page == max_page:
                break
            response = cls.__get_response(url=url, params={"page": i})
            cls.last_page = response["last_page"]
            image_array = cls.__get_images_array(data=response.get("data"), path_to=path_to.joinpath(path_dir_name))
            tasks = [asyncio.create_task(cls.__fetch(path_to=path_to, dir_name=path_dir_name, url=image)) for image in
                     image_array]
            for task in tqdm(tasks, desc="download label {}".format(path_dir_name)):
                await task

    @classmethod
    def __get_response(cls, url: str, params={"page": 1}) -> str:
        resp = json.load(urllib.request.urlopen(url + "?" + urllib.parse.urlencode(params)))
        Meta().collect_meta(dir_name=cls.dir_name, data=resp)
        return resp

    @classmethod
    def __get_last_segment(cls, url: str) -> str:
        return Path(url).name

    @classmethod
    def image_parser(cls, path_to: Path):
        reader = csv.DictReader(f, ["url", "dir_name"], delimiter=";")
        for row in tqdm(reader):
            cls.dir_name = row["dir_name"]
            path = Path(cls.dir_name)
            path_to.joinpath(path).mkdir(parents=True, exist_ok=True)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(cls.__save_images(path_to, path, row["url"]))


if __name__ == "__main__":
    with open(file_name, "r") as f:
        ImageParser.image_parser(path_to=Path('images'))
        MoveImages.move_images(path_from=Path('images'), path_to=Path('images_net'))
