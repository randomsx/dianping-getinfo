# from proxy import get_random_proxy

from parse_dianpu import *
from parse_comment import *
import requests
from config import *
import io
from font_ocr import DianPingFont
import pandas as pd


class Dianping():

    def __init__(self, dianping_font, font_io, dict_):
        self.headers = HEADERS
        self.url = 'http://www.dianping.com/changsha/ch10/g104p{}'
        self.dianping_font = dianping_font
        self.data_list = []
        self.font_io = font_io
        self.unicode_dict = dict_

    def run(self):
        """
        遍历页码，提取数据  仅测试一页
        """
        for page in range(3, 4):
            # try:
            res = requests.get(self.url.format(page), headers=self.headers)
            print(res)
            if res.status_code == 200:
                # 获取店铺列表页的css链接 css_link = 'http:' + \ re.findall('<link rel="stylesheet" type="text/css" href="(
                # //s3plus.*?)">', res.text, re.S)[0] print(css_link) css_result = requests.get(css_link).text

                html = res.text
                soup = BeautifulSoup(html, 'lxml')
                shop_list = soup.select('#shop-all-list')[0].find('ul').find_all('li')
                # print(shop_list)

                # 解析获取店铺信息
                for shop in shop_list:
                    data = parse_data(shop)
                    print(data)
                    print('爬取{}'.format(data['src']))
                    res = requests.get(data['src'], headers=self.headers)
                    print(res)
                    if res.status_code == 200:
                        # 详情页获取店铺号码并插入店铺信息集合
                        phone_info = re.findall('<p class="expand-info tel"(>.*?)</p>', res.text, re.S)[0]
                        print("phone_info:")
                        # print(phone_info)
                        phone_number = process_phone_number(phone_info)
                        print(phone_number.strip())
                        data['电话'] = phone_number

                        # 详情页获取详细地址
                        address = self.process_address_use_baidu(res.text)
                        print(address)
                        data['地址'] = address
                        self.data_list.append(data)
                        # comments = selector.css('.reviews-items > ul > li')
                        # 解析获取评论信息
                        # for comment in comments:
                        #     comment = parse_comment(comment, css_result, comment_dict)
                        # print(comment)
                        # self.mongodb(comment)
                        # except Exception as e:
                        #    print('抓取评论页失败:', e.args)
            else:
                print("提取数据失败")

    def process_address_use_baidu(self, response):
        address_str = re.findall('id="address">(.+?)</span>', response)[0]
        # print("address_str========================")
        # print(address_str)
        phone_number_dict = {
            'uniefeb': '1', 'unie4ff': '2', 'unif70d': '3', 'unie6ec': '4', 'unif404': '5', 'unie65d': '6',
            'unie284': '7',
            'unif810': '8', 'unie27b': '9', 'uniec2d': '0', '&nbsp;': ' ', '</p>': ''
        }

        # 提取电话的unicode码
        addr = re.sub('<e class="address">&#x', ' uni', re.sub(';</e>', ' ', address_str))
        addr = re.sub('<d class="num">&#x', ' uni', re.sub(';</d>', ' ', addr))
        address_result = ''
        # 分割，正则来获取所有unicode码
        for i in addr.split():
            if i in phone_number_dict.keys():
                address_result += phone_number_dict[i]
                continue

            address_result += self.get_unicode_value(i)

        return address_result

    def get_unicode_value(self, unicode):
        """
        获取unicode编码对应的汉字，当前使用百度API
        """
        if len(unicode) != 7 and len(unicode) != 8:
            return unicode
        if unicode in self.unicode_dict.keys():
            return self.unicode_dict[unicode]
        data = self.dianping_font.ocr_one(unicode, self.font_io)
        # print("----")
        # print(unicode)
        # print(data)
        # print("----")
        if data is None:
            return ''

        self.unicode_dict[unicode] = data
        return data


if __name__ == "__main__":
    # 读文件，解析unicode需要
    font_path = 'woff/5b0ad8bda40cc82dfb2e009a80893543.woff'
    with open(font_path, mode='rb') as f:
        font_bytes = f.read()
    font_io = io.BytesIO(font_bytes)

    with open("unicode_dict.txt", mode='r+', encoding='utf-8') as ff:
        dict_ = eval(ff.read())
        dianping_font = DianPingFont()
        dianping = Dianping(dianping_font, font_io, dict_)

        dianping.run()

        print(dianping.data_list)
        # 结果存入CSV中
        # todo : 随机生成名字，防止被覆盖
        pd.DataFrame(dianping.data_list).to_csv('result.csv', encoding='utf-8')
        font_io.close()

    # todo:如何读取后覆盖写？
    # 更新查出的字典
    with open("unicode_dict.txt", mode='w+', encoding='utf-8') as ff:
        ff.write(str(dianping.unicode_dict))
