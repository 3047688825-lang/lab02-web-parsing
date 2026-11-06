# -*- coding: utf-8 -*-
"""
实验二 案例2：百度新闻热点爬取与存储（代码重构可复用版）
参考教材 4.3 节 P77，目标网址 http://www.bspider.top/baidunews/
"""
import csv
import os
import re

import requests
from bs4 import BeautifulSoup

PAGE_URL = "http://www.bspider.top/baidunews/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}
CSV_PATH = "output/baidu_news.csv"

# 两类新闻的 CSS 选择器：热点要闻（div.hotnews）与焦点新闻（ul.focuslistnews）
SELECTORS = {
    "热点要闻": "div.hotnews ul li a",
    "焦点新闻": "ul.focuslistnews li a",
}


def get_html(url, headers=HEADERS, timeout=10):
    """① 发送 GET 请求，返回网页 HTML 源码"""
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        return resp.text
    except requests.RequestException as err:
        print(f"网页请求失败：{url} -> {err}")
        return ""


def parse(html):
    """② 用 BeautifulSoup(lxml) 与 CSS 选择器提取标题和详情链接"""
    soup = BeautifulSoup(html, "lxml")
    out_list = [["新闻类型", "新闻标题", "详情链接"]]
    seen = set()
    for category, selector in SELECTORS.items():
        for a in soup.select(selector):
            title = re.sub(r"\s+", " ", a.get_text(" ", strip=True)).strip()
            link = a.get("href", "").strip()
            if not title or link == "" or link == "#":
                continue                      # 过滤无效的占位链接
            if title in seen:
                continue                      # 过滤重复标题
            seen.add(title)
            out_list.append([category, title, link])
    return out_list


def save_csv(item, path=CSV_PATH):
    """③ 将解析结果写入 CSV 文件"""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        csv.writer(f).writerows(item)
    return os.path.abspath(path)


def crawl(url=PAGE_URL, path=CSV_PATH):
    """通用入口：抓取、解析、存储三步串联"""
    html = get_html(url)
    if not html:
        return []
    out_list = parse(html)
    saved = save_csv(out_list, path)
    print(f"共解析 {len(out_list) - 1} 条新闻")
    print(f"已保存：{saved}")
    return out_list


if __name__ == "__main__":
    data = crawl()
    for row in data[1:5]:
        print(f"{row[0]}：{row[1]}")
