#! /usr/bin/env python
# -*- coding: utf-8 -*-


def main():
    with open(r'D:\nytimes\dual\NYT_all_url_dual.txt', 'r', encoding='utf-8') as f:
        all_url = f.readlines()
        uni_url = list(set(all_url))
        uni_url.sort(key = all_url.index)
        url_cnt = len(uni_url)
        print(url_cnt)
        with open(r'D:\nytimes\dual\NYT_url_dual_remove_dup.txt', 'a', encoding='utf-8') as f_out:
            for row in uni_url:
                f_out.write(row)


if __name__ == '__main__':

    main()