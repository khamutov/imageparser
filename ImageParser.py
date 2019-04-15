import csv
import json
import random
import urllib.request
from pathlib import Path
from tqdm import tqdm

from Decorators import make_dirs


class ImageParser:
    def __get_images_array(self, url: str) -> []:
        array = []
        for item in self.__get_response(url):
            for image in item.get("images"):
                array.append(image)
        return random.shuffle(array)

    def __save_images(self, url: str, path: Path):
        array = self.__get_images_array(url)

        for image,count in tqdm(range(len(array)), desc='load image_list'):
            if image == 5:
            elif image == 30:
            else:
            last_segment = self.__get_last_segment(array[image])
            urllib.request.urlretrieve(array[image],
                                       str(dirs[dir_count].joinpath(last_segment)))
        #     last_segment = self.__get_last_segment(image)
        #     if path.joinpath(last_segment).is_file():
        #         continue
        #     urllib.request.urlretrieve(image,
        #                                str(path.joinpath(last_segment)))

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
                self.__save_images(row["url"], path)


if __name__ == "__main__":
    ImageParser().image_parser()
