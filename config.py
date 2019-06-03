# -*- coding:utf-8 -*-

from fake_useragent import UserAgent

ua = UserAgent()

MAX_PAGES = 20

HEADERS = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN',
            'Cache-Control': 'no-cache',
            'Connection': 'Keep-Alive',
            'Host': 'www.dianping.com',
            'Referer': 'http://www.dianping.com/chengdu/ch10/g110',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': ua.random,
            # 'Cookie': '_lxsdk_cuid=16b19a5f8e9c8-0ed9d7366e4841-e353165-144000-16b19a5f8e9c8; _lxsdk=16b19a5f8e9c8-0ed9d7366e4841-e353165-144000-16b19a5f8e9c8; _hc.v=f12bd5e2-c281-13f6-7298-71f79a39231a.1559503436; _lxsdk_s=16b19a5f8eb-da1-ee9-194%7C%7C19'
}

PROXY_URL = 'http://localhost:5555/random'

MONGO_URI = 'localhost'
MONGO_PORT = 27017

DEFAULT_STAR = '三星级商户'
DEFAULT_NAME = 'Unnamed'
DEFAULT_NUM = 10
