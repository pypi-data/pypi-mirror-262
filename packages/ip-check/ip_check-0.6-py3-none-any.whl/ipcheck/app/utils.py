#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ipaddress
import os
import random
from datetime import datetime
import sys


def is_ip_address(ip_str: str):
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip is not None
    except ValueError:
        return False


def is_ip_network(net_str: str):
    try:
        net = ipaddress.ip_network(net_str, strict=False)
        return net is not None
    except ValueError:
        return False


def get_ip_version(ip_str: str):
    ip = ipaddress.ip_address(ip_str)
    return ip.version


def gen_ip_form_network(ip_str):
    net = ipaddress.ip_network(ip_str, strict=False)
    hosts = list(net.hosts())
    all_ips = [str(ip) for ip in hosts]
    return all_ips


def find_txt_in_dir(dir):
    L = []
    if os.path.isdir(dir):
        for f in os.listdir(dir):
            file = os.path.join(dir, f)
            if os.path.isfile(file) and file.endswith('.txt'):
                L.append(file)
    return L


# 通过指定目标list 大小，从src_list 生成新的list
def adjust_list_by_size(src_list: list, target_size):
    if (target_size > len(src_list)):
        return src_list
    return random.sample(src_list, target_size)


def gen_time_desc():
    current_time = datetime.now()
    # 格式化时间为字符串，精确到秒
    return '{}: {}'.format('生成时间为', current_time.strftime("%Y-%m-%d %H:%M:%S"))

def show_freshable_content(content: str):
    print(content, end='\r')
    sys.stdout.flush()

def write_file(content: str, path: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
