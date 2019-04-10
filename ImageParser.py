import json
import urllib.request
from pathlib import Path
from tqdm import tqdm


def __get(url: str) -> json:
    return json.load(urllib.request.urlopen(url=url)).get("data")


def get_last_segment(url: str) -> str:
    return str(Path(url).name.split("?")[0])


def image_parser():
    with open("url") as f:
        for lines in f.readlines():
            if not lines.strip():
                continue
            line = lines.split(" ")
            path = Path(line[1].rstrip())
            if not path.is_dir():
                path.mkdir()
            for images in __get(line[0]):
                for count in tqdm(range(len(images.get("images")))):
                    last_segment = get_last_segment(images.get("images")[count])
                    if path.joinpath(last_segment).is_file():
                        continue
                    urllib.request.urlretrieve(images.get("images")[count],
                                               path.joinpath(last_segment))


if __name__ == "__main__":
    image_parser()
