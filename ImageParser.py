# coding=utf-8
import csv
import json
import urllib.request
import urllib.parse
import asyncio
from pathlib import Path

import aiohttp as aiohttp
from tqdm import tqdm

from CollectMeta import Meta
from MoveImagesToFolder import MoveImages

sem = asyncio.Semaphore(3)

file_name = "url.csv"
max_page = 1


class ImageParser:
    def __get_images_array(self, url: str, page_params: {} = {"page": 1}) -> []:
        array = []
        for item in self.__get_response(url, urllib.parse.urlencode(page_params)):
            for image in item.get("images"):
                array.append(image.split("?")[0])
        return array

    async def __fetch(self, path_to: Path, url, session, path: Path):
        async with sem:
            async with session.get(url=url) as response:
                temp = path_to.joinpath(path.joinpath(self.__get_last_segment(str(response.url))))
                with open(temp, 'wb') as f:
                    f.write(await response.read())

    async def __save_images(self, path_to: Path, url: str, dir_name: str, path: Path):
        tempCount = 1
        while tempCount <= max_page and len(self.__get_images_array(url, {"page": tempCount})) != 0:
            async with aiohttp.ClientSession() as session:
                tasks = []
                for image in (self.__get_images_array(url, {"page": tempCount})):
                    if not path_to.joinpath(path.joinpath(self.__get_last_segment(image))).is_file():
                        tasks.append(self.__fetch(path_to, image, session, path))
                for task in tqdm(tasks, desc="download {} page {}".format(dir_name, tempCount)):
                    await task
                tempCount += 1

    def __get_response(self, url: str, params) -> str:
        resp = json.load(urllib.request.urlopen(url + "?" + params))
        Meta().collect_meta(dir_name=self.dir_name, data=resp)
        return resp.get("data")

    def __get_last_segment(self, url: str) -> str:
        return str(Path(url).name.split("?")[0])

    def image_parser(self, path_to: Path):
        reader = csv.DictReader(f, ["url", "dir_name"], delimiter=";")
        for row in tqdm(reader):
            self.dir_name = row["dir_name"]
            path = Path(self.dir_name)
            path_to.joinpath(path).mkdir(parents=True, exist_ok=True)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.__save_images(path_to, row["url"], self.dir_name, path))


if __name__ == "__main__":
    with open(file_name, "r") as f:
        ImageParser().image_parser(path_to=Path('images'))
        MoveImages().move_images(path_from=Path('images'), path_to=Path('images_net'))
