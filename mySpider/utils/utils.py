import io
import os

import cv2
import numpy as np
from PIL import Image

USER_AGENTS = np.array([
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
])
NUM_USER_AGENTS = len(USER_AGENTS)

def get_random_user_agent():
    return USER_AGENTS[np.random.randint(0, NUM_USER_AGENTS)]


def clean_domain(domain, delete_chars='\/:*?"<>|'):
    for c in delete_chars:
        domain = domain.replace(c, '')
    return domain

def get_url_folder_name(input_domain, output_dir, date):
    dir_list = os.listdir(output_dir)
    cleaned_domain = clean_domain(input_domain)
    cnt = 0
    for s_dir in dir_list:
        cnt += 1 if cleaned_domain in s_dir else 0
    return "+{}+{}+{}".format(cleaned_domain, date, cnt)

def white_screen(img_bytes):
    img = Image.open(io.BytesIO(img_bytes))
    img = img.convert("RGB")
    img_arr = np.asarray(img)
    img_arr = np.flip(img_arr, -1)  # RGB2BGR
    img = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)

    img_area = np.prod(img.shape)
    white_area = np.sum(img == 255)
    if white_area / img_area >= 0.99:
        return True
    return False