import csv
import json
import random
import urllib.request
from pathlib import Path
from tqdm import tqdm


class ImageParser:
    def __get_images_array(self, url: str) -> []:
        array = []
        for item in self.__get_response(url):
            for image in item.get("images"):
                array.append(image)
        random.shuffle(array)
        return array

    def __save_images(self, url: str, dir_name: str, path: Path):
        array = self.__get_images_array(url)
        test = round(len(array) * 0.6)
        train = round(test + (len(array) * 0.2))

        for image in tqdm(array[:test], desc=dir_name + " fill test"):
            last_segment = self.__get_last_segment(image)
            if not path.joinpath("test").joinpath(last_segment).is_file():
                urllib.request.urlretrieve(image,
                                           str(path.joinpath("test").joinpath(last_segment)))

        for image in tqdm(array[test + 1:train], desc=dir_name + "fill train"):
            last_segment = self.__get_last_segment(image)
            if not path.joinpath("train").joinpath(last_segment).is_file():
                urllib.request.urlretrieve(image,
                                           str(path.joinpath("train").joinpath(last_segment)))

        for image in tqdm(array[train + 1:], desc=dir_name + "fill validation"):
            last_segment = self.__get_last_segment(image)
            if not path.joinpath("validation").joinpath(last_segment).is_file():
                urllib.request.urlretrieve(image,
                                           str(path.joinpath("validation").joinpath(last_segment)))

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
                path.mkdir(parents=True, exist_ok=True)
                path.joinpath("train").mkdir(parents=True, exist_ok=True)
                path.joinpath("validation").mkdir(parents=True, exist_ok=True)
                path.joinpath("test").mkdir(parents=True, exist_ok=True)
                self.__save_images(row["url"], row["dir_name"], path)


if __name__ == "__main__":
    ImageParser().image_parser()
