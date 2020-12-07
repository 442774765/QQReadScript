#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# @Time    : 2020/12/5 下午9:13
# @Author  : TNanko
# @Site    : https://tnanko.github.io
# @File    : bilibili.py
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
    """
    格式化输出 json 或者 dict 格式的变量
    :param dict:
    :return:
    """
    return print(json.dumps(dict, indent=4, ensure_ascii=False))

def sign(headers):
    url = 'https://api.live.bilibili.com/sign/doSign'
    try:
        response = requests.get(url=url, headers=headers).json()
        # pretty_dict(response)
        if response['code'] == 0:
            return response['data']
        elif response['code'] == 1011040:
            return get_sign_info(headers=headers)
        else:
            return
    except:
        print(traceback.format_exc())
        return

def get_sign_info(headers):
    url = 'https://api.live.bilibili.com/sign/GetSignInfo'
    try:
        response = requests.get(url=url, headers=headers).json()
        # pretty_dict(response)
        if response['code'] == 0:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return

def bilibili():
    # 读取 bilibili 配置
    config_latest, config_current = read()
    try:
        bilibili_config = config_current['jobs']['bilibili']
    except:
        print(traceback.format_exc())
        print('配置文件中没有此任务！请更新您的配置文件')
        return
    if bilibili_config['enable']:
        # 获取config.yml账号信息
        accounts = bilibili_config['parameters']['ACCOUNTS']
        for account in accounts:
            headers = {
                'Cookie': account['COOKIE'],
                'Host': 'api.live.bilibili.com',
                'Origin': 'api.live.bilibili.com',
                'Referer': 'http://live.bilibili.com/',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15'
            }
            utc_datetime, beijing_datetime = get_standard_time()
            symbol = '=' * 16
            print(f'\n{symbol}【bilibili】{utc_datetime.strftime("%Y-%m-%d %H:%M:%S")}/{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")} {symbol}\n')

            start_time = time.time()
            title = f'☆【bilibili】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")} ☆'
            content = ''
            sign_result = sign(headers=headers)
            if sign_result:
                content += f"【bilibili】签到成功！本月累计({sign_result['hadSignDays']},{sign_result['allDays']})次，说明{sign_result['text']}"
            else:
                content += f"【bilibili】签到失败！说明：{sign_result['message']}"

            content += f'\n🕛耗时：%.2f秒' % (time.time() - start_time)
            print(title)
            print(content)
            if bilibili_config['notify']:
                # 消息推送方式
                notify_mode = bilibili_config['notify_mode']
                try:
                    # 推送消息
                    notify.send(title=title, content=content, notify_mode=notify_mode)
                except TypeError:
                    print('请确保配置文件的对应的脚本任务中，参数 notify_mode 下面有推送方式\n')
            else:
                print('未进行消息推送，原因：未设置消息推送。如需发送消息推送，请确保配置文件的对应的脚本任务中，参数 notify 的值为 true\n')
    else:
        print('未执行该任务，如需执行请在配置文件的对应的任务中，将参数 enable 设置为 true\n')

def main():
    bilibili()


if __name__ == '__main__':
    main()