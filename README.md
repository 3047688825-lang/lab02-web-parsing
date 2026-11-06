# lab02-web-parsing

大数据采集与处理 实验二：网页解析（代码重构可复用版）

使用 `requests` + `BeautifulSoup(lxml)` + CSS 选择器解析网页，结果保存为 CSV。

## 案例

| 案例 | 说明 | 目标网址 | 源码 |
| ---- | ---- | -------- | ---- |
| 案例1 | 中国大学排名爬取存储（教材 4.2 节 P73） | http://www.bspider.top/gaosan/ | [university_ranking.py](university_ranking.py) |
| 案例2 | 百度新闻热点爬取与存储（教材 4.3 节 P77） | http://www.bspider.top/baidunews/ | [baidu_news.py](baidu_news.py) |

## 项目结构

```
lab02-web-parsing/
├── university_ranking.py   # 案例1：中国大学排名
├── baidu_news.py           # 案例2：百度新闻
├── requirements.txt        # 依赖清单
└── output/                 # 运行后生成的 CSV（已 gitignore）
    ├── university_ranking.csv
    └── baidu_news.csv
```

## 运行方式

```bash
pip install -r requirements.txt
python university_ranking.py
python baidu_news.py
```

## 代码设计

两个案例均采用同一套可复用结构，三步分离：

- `get_html(url)`：发送 GET 请求，`raise_for_status()` 校验状态码，`apparent_encoding` 处理中文编码，`try/except requests.RequestException` 捕获网络异常
- `parse(html)`：`BeautifulSoup(html, "lxml")` 解析，CSS 选择器定位（案例1 用 `table>tbody>tr` 二次查找 `td`；案例2 用选择器字典同时抓取两类新闻，并去重、过滤 `href="#"` 占位链接）
- `save_csv(item)`：`open(path, "w", newline="", encoding="utf-8-sig")` 写入 CSV，避免空行与中文乱码
- `crawl(url, path)`：三步串联的统一入口，更换网址或选择器即可复用

## 实测结果

- 案例1：解析 **821 条**大学排名记录（名次、学校名称、总分、全国排名、星级排名、办学层次）
- 案例2：解析 **126 条**新闻（热点要闻 + 焦点新闻，含新闻类型、新闻标题、详情链接）
