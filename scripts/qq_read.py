#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# @Time    : 2020/12/3 1:28
# @Author  : TNanko
# @Site    : https://tnanko.github.io
# @File    : qq_read.py
# @Software: PyCharm
import sys
import os
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
import json
import time
import requests
import traceback
from setup import get_standard_time
from utils import notify
from utils.configuration import read


def qq_reader():
    qq_reader_config = read()['jobs']['qq_reader']
    if qq_reader_config['enable']:
        utc_datetime, beijing_datetime = get_standard_time()
        symbol = '=' * 16
        print(f'\n{symbol}【企鹅阅读】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")} {symbol}')
        start_time = time.time()
        title = f'☆【企鹅阅读】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")} ☆'
        content = ''



        print(title)
        print(f'🕛耗时：{time.time()-start_time}秒')
        # 发送消息推送
        if qq_reader_config['notify']:
            notify.send(title=title, content=content)
        else:
            print('未进行消息推送，如需发送消息推送请在配置文件的对应的任务中，将参数notify设置为true')
    else:
        print('未执行该任务，如需执行请在配置文件的对应的任务中，将参数enable设置为true')

def main():
    qq_reader()


if __name__ == '__main__':
    main()
