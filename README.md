# WebpageSpider: A Concurrent Webpage Data Scraper

## 1. Introduction
WebpageSpider is a concurrent webpage data scraper based on [Scrapy](https://scrapy.org/) and [Playwright](https://playwright.dev/python/), particularly used to fetch static webpage data for the following phishing detectors:
- [KnowPhish Detector](https://arxiv.org/abs/2403.02253)
- [PhishIntention](https://www.usenix.org/conference/usenixsecurity22/presentation/liu-ruofan)
- [Phishpedia](https://www.usenix.org/conference/usenixsecurity21/presentation/lin)

The data of a webpage $w$ comprises the following 4 files:
- **input_url.txt**: The input URL of $w$
- **info.txt**: The landing URL of $w$
- **html.txt**: The HTML of $w$
- **shot.png**: A screenshot of $w$ with 1280*720 resolution


## 2. Installation
1. Set up the conda environment in your Linux machine

```
conda create -n webpage_spider python=3.10 
conda activate webpage_spider
```

2. Install the required Python package
```
bash ./install.sh
```

## 3. Start Crawling
You can just simply specify your input URL list within the ```__init__()``` method at ```./mySpider/spiders/webpage_spider.py```, and then run the following command
```
scrapy crawl webpage_spider
```
The scaper can concurrently process 16 URL requests at the same time. You can modify the maximum concurrent requests at ```./mySpider/settings.py```.

(Optional) By default, WebpageSpider will look at the csv file in ```./input/``` to get a list of input URLs and output the crawled data at a folder in ```./output```. We also provide two scripts to fetch a few examples of benign and phishing URLs
- Benign (from [Tranco](https://tranco-list.eu/))
```
python ./input/pull_tranco_urls.py
```

- Phishing: (from [OpenPhish](https://openphish.com/))
```
python ./input/pull_openphish_urls.py
```

## 4. Citation
If you find this project helpful, please consider citing our paper
```
@misc{li2024knowphish,
      title={KnowPhish: Large Language Models Meet Multimodal Knowledge Graphs for Enhancing Reference-Based Phishing Detection}, 
      author={Yuexin Li and Chengyu Huang and Shumin Deng and Mei Lin Lock and Tri Cao and Nay Oo and Bryan Hooi and Hoon Wei Lim},
      year={2024},
      eprint={2403.02253},
      archivePrefix={arXiv},
      primaryClass={cs.CR}
}
```
