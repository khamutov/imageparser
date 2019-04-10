import json
import urllib.request
import os
from tqdm import tqdm


def __get(url: str) -> json:
    return json.load(urllib.request.urlopen(url=url)).get("data")


def image_parser():
    counter = 0
    with open("url") as f:
        for lines in f.readlines():
            line = lines.split(" ")
            if not os.path.isdir(line[1]):
                os.makedirs(line[1])
            for images in __get(line[0]):
                for count in tqdm(range(len(images.get("images")))):
                    if os.path.isfile(line[1] + "\\" + str(counter) + ".jpg"):
                        counter += 1
                        continue
                    urllib.request.urlretrieve(images.get("images")[count],
                                               line[1] + "\\" + str(counter) + ".jpg")
                    counter += 1


if __name__ == "__main__":
    image_parser()
