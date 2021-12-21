#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests

def url_exist(url):
    req = requests.head(url)
    if req.status_code == 200:
        print('%s exists!'% url )
        return True
    else:
        print('%s does not exist!'% url )
        return False

def save_data_dual(url_data):
    with open(r'D:\nytimes\nytimes_lens_dual.txt', 'w', encoding='utf-8') as f:
        for item in url_data:
            f.write(item + '\n')

def url_filter(url_list):
    url_dual = []
    for url in url_list:
        dual = url.strip() + 'dual/'
        if url_exist(dual):
            url_dual.append(dual)

    return url_dual

def main():

    with open(r'D:\nytimes\nytimes_lens.txt', 'r', encoding='utf-8') as f:
        url_data = f.readlines()
        url_dual = url_filter(url_data)
        save_data_dual(url_dual)

main()