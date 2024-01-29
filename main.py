# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 22:40:10 2024

@author: daria
"""

# todo's: 
    
# v Connect to GitHub
# v Get correct links from image search
# v Save them correctly
# Clear the data (look what they do in the book)
# Load them into resnet18
# Train
# Save the model
# Check if it works
# Add some interface
# In the future: add stuff to combine train new models
# 
# import torch
from duckduckgo_search import DDGS
import requests
import os


def get_image_links(keyword: str, max_res: int) -> list:
    my_images = DDGS().images(keyword, max_results=max_res)
    links_to_return = []
    for a in my_images:
        links_to_return.append(a.get("image"))
    return links_to_return


def extract_name(url: str) -> str:
    inter_result = url.split('/')[-1]
    return inter_result.split('?')[0]


def download_links(links: list, folder_name: str):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    for link in links:
        try:
            to_save = requests.get(link).content
            with open(folder_name + "/" + extract_name(link), 'wb') as s:
                s.write(to_save)
        except Exception as e:
            print("Oops, this link can not be downloaded: ", link)


def verify_image(image_path:str) -> bool:
    try:

        return True
    except:
        return False


def verify_images(path_to_images: list[str]) -> list[bool]:
    for im in path_to_images:
        return []


if __name__ == "__main__":
    links_kiwi = get_image_links("kiwi fruit", 100)
    links_potato = get_image_links("potato", 100)
    download_links(links_potato, "potato")
    download_links(links_kiwi, "kiwi")

