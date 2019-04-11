import csv
import json
import urllib.request
from pathlib import Path
from tqdm import tqdm


class ImageParser:
    def __collect_images(self, resp) -> []:
        return [image for images_list in resp for image in images_list["images"]]

    def __make_dir(self, path: Path):
        if not path.is_dir():
            path.mkdir()

    def __save_images(self, url: str, path: Path):
        arr = self.__collect_images(self.__get_response(url))
        for image in tqdm(arr, desc="download: "):
            last_segment = self.__get_last_segment(image)
            if not path.joinpath(last_segment).is_file():
                urllib.request.urlretrieve(image,
                                           path.joinpath(last_segment))

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
            for row in reader:
                path = Path(row["dir_name"])
                self.__make_dir(path)
                self.__save_images(row["url"], path)


if __name__ == "__main__":
    ImageParser().image_parser()
