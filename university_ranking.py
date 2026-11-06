# -*- coding: utf-8 -*-
"""
实验二 案例1：中国大学排名爬取与存储（代码重构可复用版）
参考教材 4.2 节 P73，目标网址 http://www.bspider.top/gaosan/
"""
import csv
import os

import requests
from bs4 import BeautifulSoup

# ① 请求配置：目标网址、请求头、超时时间
PAGE_URL = "http://www.bspider.top/gaosan/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}
CSV_PATH = "output/university_ranking.csv"
ROW_SELECTOR = "table>tbody>tr"


def get_html(url, headers=HEADERS, timeout=10):
    """② 发送 GET 请求，返回网页 HTML 源码（含编码处理与异常捕获）"""
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        return resp.text
    except requests.RequestException as err:
        print(f"网页请求失败：{url} -> {err}")
        return ""


def parse(html):
    """③ 用 BeautifulSoup(lxml) + CSS 选择器解析表格，返回二维列表"""
    soup = BeautifulSoup(html, "lxml")
    rows = soup.select(ROW_SELECTOR)          # 一次查找定位全部数据行
    out_list = []
    for row in rows:
        tds = row.select("td")                # 二次查找：行内单元格
        if len(tds) < 6:
            continue
        out_list.append([
            tds[0].get_text(strip=True),      # 名次
            tds[1].get_text(strip=True),      # 学校名称
            tds[2].get_text(strip=True),      # 总分
            tds[3].get_text(strip=True),      # 全国排名
            tds[4].get_text(strip=True),      # 星级排名
            tds[5].get_text(strip=True),      # 办学层次
        ])
    return out_list


def save_csv(item, path=CSV_PATH):
    """④ 将二维列表写入 CSV 文件（utf-8 + newline=''，避免空行）"""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows(item)
    return os.path.abspath(path)


def crawl(url=PAGE_URL, path=CSV_PATH):
    """通用入口：内部调用三个通用函数，外部只需传网址与保存路径"""
    html = get_html(url)
    if not html:
        return []
    out_list = parse(html)
    saved = save_csv(out_list, path)
    print(f"共解析 {len(out_list)} 条记录")
    print(f"已保存：{saved}")
    return out_list


if __name__ == "__main__":
    data = crawl()
    for row in data[:4]:
        print(f"{row[0]}  {row[1]}  {row[2]}")
