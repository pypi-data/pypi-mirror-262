#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @description : description
# @file    : main.py
# @author  : xingpeidong
# @email   : xpd1437@126.com
# @time    : 2024/3/14 16:56
"""
import json
import os
import sys
import time

from insta_python_api import http_requests

def main():
    try:
        # 获取配置文件数据
        yaml_config = http_requests.get_config()
        # 生成接口地址和URI
        host = yaml_config["instafogging"]["host"]
        uri = yaml_config['instafogging']['uri']['get_logfile']
        request_url = host + uri
        # 获取请求headers
        headers = http_requests.get_headers(yaml_config)
        # print(time.strftime('%Y-%m-%d %H:%M:%S'))
        data = {
            "format_time": "5min",
            "start_time": time.strftime('%Y-%m-%d 00:00:00'),
            "end_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            # "domain": "example.domain"
        }
        request_data = json.dumps(data)
        print("POST", request_url, headers, request_data)

        response = http_requests.send_request("POST", request_url, headers, request_data)
        print(response)


    except ValueError as ve:
        return str(ve)

if __name__ == "__main__":
    sys.exit(main())