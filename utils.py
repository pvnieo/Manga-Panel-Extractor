# stdlib
import json
import os

import cv2
# 3p
import numpy as np
import requests
from bs4 import BeautifulSoup
from skimage import io


def download_lmages(url, folder):
    # Send a GET request to the URL
    response = requests. get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all the unage tags and extract the image URLS
    img_tags = soup.find_all("img")
    img_urls = [img['src'] for img in img_tags if img['src'].startswith("https://cdn.onepiecechapters.com/file/CDN-M-A-N/") and img['src'].endswith(".png")]

    # Create the folder if not exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Download each image
    for img_url in img_urls:
        img_name = os.path.basename(img_url)
        img_data = requests.get(img_url).content
        img_path = os.path.join(folder, img_name)
        with open(img_path, "wb") as f:
            f.write(img_data)

    print("All images downloaded successfully!")



def save_file(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def get_files(img_dir):
    imgs, masks, xmls = list_files(img_dir)
    return imgs, masks, xmls


def list_files(in_path):
    img_files = []
    mask_files = []
    gt_files = []
    for (dirpath, dirnames, filenames) in os.walk(in_path):
        for file in filenames:
            filename, ext = os.path.splitext(file)
            ext = str.lower(ext)
            if ext == '.jpg' or ext == '.jpeg' or ext == '.gif' or ext == '.png' or ext == '.pgm':
                img_files.append(os.path.join(dirpath, file))
            elif ext == '.bmp':
                mask_files.append(os.path.join(dirpath, file))
            elif ext == '.xml' or ext == '.gt' or ext == '.txt':
                gt_files.append(os.path.join(dirpath, file))
            elif ext == '.zip':
                continue
    return img_files, mask_files, gt_files


def load_image(img_file):
    img = io.imread(img_file)           # RGB order
    if img.shape[0] == 2:
        img = img[0]
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    if img.shape[2] == 4:
        img = img[:, :, :3]
    img = np.array(img)

    return img