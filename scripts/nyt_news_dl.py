#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import requests
from bs4 import BeautifulSoup


def html_downloader(url):
    res = requests.get(url).text
    return res


def make_article(url):
    article = {}

    html = html_downloader(url)
    soup = BeautifulSoup(html, 'lxml')

    header_chn_soup = soup.find(class_="article-header").find("header").find('h1')
    header_chn = header_chn_soup.get_text() if header_chn_soup else ''
    article['header_chn'] = header_chn

    header_eng_soup = soup.find(class_="article-header").find("header").find(class_="en-title")
    header_eng = header_eng_soup.get_text() if header_eng_soup else ''
    article['header_eng'] = header_eng

    byline_soup = soup.find(class_="byline-box")
    if byline_soup:
        author_soup = byline_soup.find('address')
        author = author_soup.get_text() if author_soup else ''
        article['author'] = author

        pub_date_soup = byline_soup.find('time')
        pub_date = pub_date_soup.get_text() if pub_date_soup else ''
        article['pub_date'] = pub_date

        datetime_soup = byline_soup.find('time')
        datetime = datetime_soup['datetime'] if datetime_soup else '1970-01-01 00:00:00'
        article['datetime'] = datetime
    else:
        article['author'] = ''
        article['pub_date'] = ''
        article['datetime'] = '1970-01-01 00:00:00'

    author_info_soup = soup.find(class_="author-info")
    author_info = author_info_soup.get_text() if author_info_soup else ''
    article['author_info'] = author_info

    content = []
    para_list = soup.find_all(class_="article-paragraph")
    for para in para_list:
        paragraph = para.get_text()
        content.append(paragraph)

    article['content'] = '\n'.join(content)

    return article


def save_article(codict, path):
    file_name = codict['header_chn']
    file_name = re.sub(r'[\\/:*?"<>|]+', '_', file_name)
    prefix = codict['datetime'][:10]
    whole_content = codict['header_chn'] + '\n' + codict['header_eng'] + '\n' + codict['author'] + '\n' + \
                    codict['pub_date'] + '\n' + codict['content'] + '\n' + codict['author_info']
    os.chdir(os.path.join(r"/root/temp/nytimes", path))
    with open('%s_%s_%s.txt' % (prefix, path, file_name), 'w', encoding='utf-8') as f:
        f.write(whole_content)
        print('%s has been saved.' % file_name)


def make_dir(path):
    is_ex = os.path.exists(os.path.join(r"./nytimes", path))
    if not is_ex:
        print('create', path, 'directory.')
        os.makedirs(os.path.join(r"./nytimes", path))
        return True
    else:
        print('directory named ', path, 'has existed.')
        return False

def downloader(category, path):
    make_dir(path)
    for link in category:
        link = link.strip()
        content = make_article(link)
        save_article(content, path)


def main():

    with open('NYT_url_dual_remove_dup.txt', 'r', encoding='utf-8') as f:
        urls = f.readlines()
        
        opinion = urls[:2800]
        downloader(opinion, path='opinion')
        real_estate = urls[2800:3418]
        downloader(real_estate, path='real_estate')
        travel = urls[3418:3892]
        downloader(travel, path='travel')
        style = urls[3892:5034]
        downloader(style, path='style')
        culture = urls[5034:7236]
        downloader(culture, path='culture')
        education = urls[7236:7822]
        downloader(education, path='education')
        health = urls[7822:8722]
        downloader(health, path='health')
        science = urls[8722:9365]
        downloader(science, path='science')
        technology = urls[9365:10629]
        downloader(technology, path='technology')
        business = urls[10629:13576]
        downloader(business, path='business')
        china = urls[13576:17866]
        downloader(china, path='china')
        world = urls[17866:]
        downloader(world, path='world')


if __name__ == '__main__':
    main()