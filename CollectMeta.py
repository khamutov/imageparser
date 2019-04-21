# coding=utf-8
import csv

class Meta:

    def __write_to_file(self, data: []):
        with open("meta.csv","w") as file:
            csv_reader = csv.writer(file,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_reader.writerow(data)


    def collect_meta(self, dir_name: str, data : [] ):
        with open("meta.csv","w",newline='') as file:
            for item in data.get("data"):
                csv_reader = csv.writer(file,delimiter=';')
                csv_reader.writerow([dir_name,
                                     [f.split("?")[0]for f in item["images"]],
                                     item["brand_id"],
                                     item["brand_name"]])

