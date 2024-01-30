# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 22:40:10 2024

@author: daria
"""

# Todo's:
    
# v Connect to GitHub
# v Get correct links from image search
# v Save them correctly
# v Verify data
# Load them into resnet18
# Train
# Save the model
# Check if it works
# Add some interface
# In the future: add stuff to combine train new models
# 
# import torch
# Add colors:
# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKCYAN = '\033[96m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'
# ^ https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal


from duckduckgo_search import DDGS
import requests
import os
from multiprocessing import Process, Queue
import multiprocessing
import PIL.Image


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
            print('\033[91m' + "Oops, this link can not be downloaded: ", link, "\nReason: ", e)


def verify_image(image_path: str) -> bool:
    try:
        img = PIL.Image.open(image_path)
        img.draft(img.mode, (32, 32))
        img.load()
        return True
    except:
        return False


def verify_image_worker(q: multiprocessing.Queue, path: str):
    res = verify_image(path)
    q.put((path, res))


def verify_images(path_to_images: list[str]) -> list[(int, bool)]:
    processes = []
    to_return = []
    q = Queue()
    # Iterate through all image paths
    for path in path_to_images:
        p = Process(target=verify_image_worker, args=(q, path))
        p.start()
        processes.append(p)
    # Get all stuff
    for p in processes:
        res = q.get()
        to_return.append(res)
    # Wait for all processes
    for p in processes:
        p.join()
    to_return.sort()
    return to_return


def get_image_list_in(folder_path: str) -> list[str]:
    to_return = []
    for f in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, f)):
            to_return.append(os.path.join(folder_path, f))
    return to_return


if __name__ == "__main__":
    # Get image links
    links_kiwi = get_image_links("kiwi fruit", 100)
    links_potato = get_image_links("potato vegetable", 100)
    # Download the images
    download_links(links_potato, "potato")
    download_links(links_kiwi, "kiwi")
    # Get the files in the maps
    kiwi_paths = get_image_list_in("kiwi")
    potato_paths = get_image_list_in("potato")
    # Verify them
    verified_kiwis = verify_images(kiwi_paths)
    verified_potatoes = verify_images(potato_paths)
    print("\033[92m" + "To be continued...")
