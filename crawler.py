# -*- coding:utf-8 -*-

import sys
import os
import argparse
import requests
import cv2
from googleapiclient.discovery import build

fileDir = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument(
    "--dir", type=str, default=os.path.join(fileDir, "images"), help="image directory")
parser.add_argument("--num", type=int, default=10, help="number of images")
parser.add_argument("--interval", type=int, default=10000,
                    help="interval in milliseconds")
parser.add_argument("--queries", type=str, nargs="+", help="search queries")
args = parser.parse_args()

api_key = "AIzaSyClbBZDV4d18HOQDN_EJe87epvTu8iiVOY"
engine_id = "011535217716291083397:nygvrfvfuwk"
service = build("customsearch", "v1", developerKey=api_key)

for query in args.queries:

    try:

        search_response = service.cse().list(
            q=query,
            cx=engine_id,
            lr="lang_ja",
            num=args.num,
            start=1,
            searchType="image"
        ).execute()

        for index, item in enumerate(search_response["items"]):

            url = item["link"]

            image_response = requests.get(url)

            if image_response.status_code == 200 and "image" in image_response.headers["content-type"]:

                filename = os.path.join(
                    args.dir, query + str(index).zfill(3) + os.path.splitext(url)[1])

                with open(filename, "wb") as fout:

                    fout.write(image_response.content)

                image = cv2.imread(filename)

                cv2.imshow("image", image)

                key = cv2.waitKey(args.interval)

                if key == ord("q"):

                    sys.exit(0)

        # startIndex = search_response.get("queries").get("nextPage")[0].get("startIndex")

    except Exception as exception:

        print(exception)
