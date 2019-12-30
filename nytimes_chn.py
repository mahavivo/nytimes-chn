#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
import re
import requests
from bs4 import BeautifulSoup


def html_downloader(url):
    res = requests.get(url).text
    return res

def html_parser(html):
    articles = []
    soup = BeautifulSoup(html, 'lxml')
    article_list = soup.find_all(class_="regularSummaryHeadline")
    for article in article_list:
        article_link = article.find('a')['href']
        real_link = home_url + article_link
        articles.append(real_link)
        print(real_link)
    
    page_next = soup.find(class_="pagination").find(class_="next")
    if page_next:
        page_next = home_url + page_next.find('a')['href']
        return articles, page_next
    else:
        return articles, None

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

def save_article(codict):
    file_name = codict['header_chn']
    file_name = re.sub(r'[\\/:*?"<>|]+', '_', file_name)
    prefix = codict['datetime'][:10]
    whole_content = codict['header_chn'] + '\n' + codict['header_eng'] + '\n' + codict['author'] + '\n' + \
                    codict['pub_date'] + '\n' + codict['content'] + '\n' + codict['author_info']

    with open('%s_%s.txt' % (prefix, file_name), 'w', encoding='utf-8') as f:
        f.write(whole_content)

def url_exist(url):
    req = requests.head(url)
    if req.status_code == 200:
        print('%s exists!'% url )
        return True
    else:
        print('%s does not exist!'% url )
        return False

def save_data(url_data):
    with open('nytimes_%s.txt' % category, 'w', encoding='utf-8') as f:
        for item in url_data:
            f.write(item + '\n')

def save_data_dual(url_data):
    with open('nytimes_%s_dual.txt' % category, 'w', encoding='utf-8') as f:
        for item in url_data:
            f.write(item + '\n')

def url_filter(url_list):
    url_dual = []
    for url in url_list:
        dual = url + 'dual/'
        if url_exist(dual):
            url_dual.append(dual)

    return url_dual

def make_dir(path):
    is_ex = os.path.exists(os.path.join(r"D:\nytimes", path))
    if not is_ex:
        print('create', path, 'directory.')
        os.makedirs(os.path.join(r"D:\nytimes", path))
        os.chdir(os.path.join(r"D:\nytimes", path))
        return True
    else:
        print('directory named ', path, 'has existed.')
        return False

def main():
    url = home_url + '/' + category + '/1/'
    url_data = []
    while url:
        html = html_downloader(url)
        links, url = html_parser(html)
        url_data.extend(links)

    make_dir(category)
    save_data(url_data)

    url_dual = url_filter(url_data)
    save_data_dual(url_dual)

    for link in url_data:
        link = link.strip()
        content = make_article(link)
        save_article(content)


if __name__ == '__main__':

    home_url = 'https://cn.nytimes.com'
    category = 'travel'

    main()