#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

from PIL import Image
from bs4 import BeautifulSoup


class ChesiccMethod(object):
    @staticmethod
    def query_edu(q_code: str):
        return f'https://www.chsi.com.cn/xlcx/bg.do?vcode={q_code}&srcid=bgcx'

    @staticmethod
    def query_edu_img(img_pos: str):
        return f'https://www.chsi.com.cn{img_pos}'


class Chesicc(object):
    @staticmethod
    def query_edu(q_code: str):
        if isinstance(q_code, int):
            q_code = str(q_code)
        url = ChesiccMethod.query_edu(q_code)
        response = requests.post(url, timeout=10)
        msg = response.content.decode('utf-8')
        return msg

    @staticmethod
    def query_edu_img(img_pos: str):
        url = ChesiccMethod.query_edu_img(img_pos)
        img = Image.open(requests.get(url, stream=True).raw)
        img.show()

    @staticmethod
    def chsi_parser(page, get_img: bool = False):
        soup = BeautifulSoup(page, features='lxml-xml')
        result_table = soup.find('div', {'class': 'clearfix', 'id': 'resultTable'})
        info_dict = dict()
        if result_table is None:
            return info_dict
        if get_img:
            result_table.find('img', {'id': 'photoPositon'})
        info_list = result_table.find_all('td')[3:33]
        for index in range(0, len(info_list), 2):
            info_key = info_list[index].contents[0]
            info_value = info_list[index + 1].find('div').contents[0]
            info_dict[info_key] = info_value.replace(' ', '').replace('\n', '')
        return info_dict

    @staticmethod
    def get_chsi_info(q_code: str):
        content = Chesicc.query_edu(q_code)
        info_dict = Chesicc.chsi_parser(content)
        return info_dict
