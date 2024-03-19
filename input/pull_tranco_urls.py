import os
import shutil
import zipfile

import pandas as pd
import requests


def download_zip(url, destination):
    with requests.get(url, stream=True) as response:
        with open(destination, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
    print("Zip file downloaded successfully")

def unzip_file(zip_file, destination):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(destination)
    print("Zip file extracted successfully")
    os.remove(zip_file)

if __name__ == "__main__":
    zip_url = 'https://tranco-list.eu/download_daily/7XX9X'
    zip_destination = './input/tranco_top_1m.zip'
    download_zip(zip_url, zip_destination)

    unzip_destination = './input/tranco_top_1m'
    unzip_file(zip_destination, unzip_destination)

    df = pd.read_csv(os.path.join(unzip_destination, 'top-1m.csv'), index_col=None, header=None, names=['rank', 'url']).head(10000)[["url"]]
    df = df.sample(n=100).reset_index(drop=True)
    df["url"] = "https://" + df["url"] + "/"

    df.to_csv("./input/example_benign_urls.csv", index=False)




