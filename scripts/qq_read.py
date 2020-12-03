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

def pretty_dict(dict):
    return print(json.dumps(dict, indent=4, ensure_ascii=False))

def get_user_info(headers):
    url = 'https://mqqapi.reader.qq.com/mqq/user/init'
    try:
        response = requests.get(url=url, headers=headers).json()
        # pretty_dict(response)
        if response['code'] == 0:
            return response
        else:
            return
    except:
        print(traceback.format_exc())
        return

def qq_reader():
    qq_reader_config = read()['jobs']['qq_reader']
    # 获取config.yml账号信息
    accounts = qq_reader_config['parameters']['ACCOUNTS']
    # 每次上传的时间
    upload_time = qq_reader_config['parameters']['UPLOAD_TIME']

    # 开启脚本执行
    if qq_reader_config['enable']:
        for account in accounts:
            # 可自定义的书籍url
            book_url = account['BOOK_URL']
            # 更换ywsession，Cookie
            headers = {
                'Accept': '*/*',
                'ywsession': account['YWSESSION'],
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Cookie': account['COOKIE'],
                'Host': 'mqqapi.reader.qq.com',
                'User-Agent': 'QQ/8.4.17.638 CFNetwork/1197 Darwin/20.0.0',
                'Referer': 'https://appservice.qq.com/1110657249/0.30.0/page-frame.html',
                'Accept-Language': 'zh-cn',
                'Accept-Encoding': 'gzip, deflate, br',
                'mpversion': '0.30.0'
            }
            utc_datetime, beijing_datetime = get_standard_time()
            symbol = '=' * 16
            start_time = time.time()
            print(f'\n{symbol}【企鹅阅读】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")} {symbol}')
            title = f'☆【企鹅阅读】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")} ☆'
            content = ''

            user_info = get_user_info(headers=headers)
            if user_info:
                content += f'【用户昵称】{user_info["data"]["user"]["nickName"]}'


            content += f'\n🕛耗时：{time.time()-start_time}秒'
            print(title)
            print(content)
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
