import datetime
import os
import time
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import scrapy
from lxml import etree
from scrapy_playwright.page import PageMethod
from termcolor import colored
from tqdm import tqdm
import logging

from ..utils import utils


class WebpageSpider(scrapy.Spider):
    name = "webpage_spider"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_date = datetime.date.today()
        self._current_time = time.strftime("%H-%M-%S")
        self._start_time = None
        self._end_time = None
        self._requests_sent_cnt = 0
        self._requests_completed_cnt = 0

        #############################################
        ##### 1. Specify the URLs to be visited #####
        self._urls = pd.read_csv("./input/example_benign_urls.csv", index_col=None)["url"].values
        # self._urls = pd.read_csv("./input/example_phishing_urls.csv", index_col=None)["url"].values
        
        np.random.shuffle(self._urls)
        #############################################

        #############################################
        ##### 2. Set the output directory ###########
        self._output_dir = f"./output/{self._current_date}_{self._current_time}"
        if not os.path.exists(self._output_dir):
            os.mkdir(self._output_dir)
        #############################################
            
    def start_requests(self):
        self._start_time = time.time()
        for i, input_url in enumerate(tqdm(self._urls, desc="Requests Sent")):
            self._requests_sent_cnt += 1
            yield scrapy.Request(
                url=input_url,
                headers={
                    "User-Agent": utils.get_random_user_agent()
                    },
                meta={
                    "playwright": True,
                    "playwright_page_goto_kwargs": {
                        "wait_until": "load",
                    },
                    "playwright_page_methods": [
                        PageMethod("screenshot"),
                        PageMethod("content"),
                        PageMethod("set_viewport_size", {"width": 1280, "height": 720}),
                        PageMethod("wait_for_timeout", 5000),
                        ],
                    "rank": i,
                    "input_url": input_url,
                    }
                )

    def parse(self, response, **kwargs):
        # 1. Retrieve the response data
        rank = response.meta["rank"]

        input_url = response.meta["input_url"]
        landing_url = response.url
        landing_domain = urlparse(landing_url).netloc

        shot_bytes = response.meta["playwright_page_methods"][0].result
        html_str = response.meta["playwright_page_methods"][1].result
        html_str = etree.tostring(etree.HTML(html_str), pretty_print=True, encoding='utf-8')
        
        print(f"===== {colored('PROCESSING', 'yellow', attrs=['bold', 'reverse'])}   {rank:5d}-th REQUEST ({landing_url})")

        # 2. Configure the output folder
        folder_name = utils.get_url_folder_name(landing_domain, self._output_dir, f"[{self._current_date}]")
        url_folder_path = os.path.join(self._output_dir, folder_name)
        if not os.path.exists(url_folder_path):
            os.mkdir(url_folder_path)

        input_url_path = os.path.join(url_folder_path, "input_url.txt")
        info_path = os.path.join(url_folder_path, "info.txt")
        html_path = os.path.join(url_folder_path, "html.txt")
        shot_path = os.path.join(url_folder_path, "shot.png")
        
        # 3. Save the data
        with open(input_url_path, "w") as f:
            f.write(input_url)
        
        with open(info_path, "w") as f:
            f.write(landing_url)
        
        with open(html_path, "wb") as f:
            f.write(html_str)

        with open(shot_path, "wb") as f:
            f.write(shot_bytes)

        print(f"===== {colored('COMPLETED ', 'green', attrs=['bold', 'reverse'])}   {rank:5d}-th REQUEST ({landing_url})")
        self._requests_completed_cnt += 1

        return {
            "input_url": input_url,
            "landing_url": response.url
            }
    
    # def closed(self, reason):
    #     self._end_time = time.time()
    #     total_time = self._end_time - self._start_time
    #     avg_time = total_time / self._requests_sent_cnt

    #     print()
    #     print(f"############################")
    #     print(f"## URL SENT: {self._requests_sent_cnt:8d}")
    #     print(f"## URL DONE: {self._requests_completed_cnt:8d}")
    #     print(f"## TOT TIME: {total_time:7.2f}s")
    #     print(f"## AVG TIME: {avg_time:7.2f}s")
    #     print(f"## CLOSED:   {reason}")
    #     print(f"############################")

