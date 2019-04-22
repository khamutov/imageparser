# coding=utf-8
import csv


class Meta:

    def __write_to_file(self, data: []):
        with open("meta.csv", "w") as file:
            csv_reader = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_reader.writerow(data)

    def collect_meta(self, dir_name: str, data: []):
        with open("meta.csv", "w", newline='') as file:
            for item in data.get("data"):
                for image in item["images"]:
                    csv_reader = csv.writer(file, delimiter=';')
                    csv_reader.writerow([dir_name,
                                         image.split("?")[0],
                                         item["photobank_id"]]
                                        )
