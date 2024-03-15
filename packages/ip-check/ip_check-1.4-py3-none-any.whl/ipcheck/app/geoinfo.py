#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import geoip2.database
from typing import List
from ipcheck.app.ip_info import IpInfo
import sys
from ipcheck.app.utils import is_ip_address, download_file

GEO2CITY_DB_NAME = 'GeoLite2-City.mmdb'
GEO2CITY_DB_PATH = os.path.join(os.path.dirname(__file__), GEO2CITY_DB_NAME)
# GEO2CITY_DB_URL = 'https://github.com/P3TERX/GeoLite.mmdb/releases/download/2024.03.13/GeoLite2-City.mmdb'

def download_geo_db(url :str):
    return download_file(url, GEO2CITY_DB_PATH)


def check_geo_db():
    if os.path.exists(GEO2CITY_DB_PATH):
        return True
    else:
        return False


def get_geo_info(ip :str):
    if not check_geo_db():
        print('ip 数据库不存在，请手动下载{} 到 {}'.format(GEO2CITY_DB_NAME, GEO2CITY_DB_PATH))
        return 'Unkonwn-Unknown'
    with geoip2.database.Reader(GEO2CITY_DB_PATH) as reader:
        response = reader.city(ip)
        country = response.country.names.get('zh-CN', 'Unknown')
        city = response.city.names.get('zh-CN', 'Unknown')
        return '{}-{}'.format(country, city)

def get_geo_ipfos(infos: List[IpInfo]) -> IpInfo:
    if not check_geo_db():
        print('ip 数据库不存在，请下载{} 到 {}'.format(GEO2CITY_DB_NAME, GEO2CITY_DB_PATH))
        return infos
    res = []
    with geoip2.database.Reader(GEO2CITY_DB_PATH) as reader:
        for ipinfo in infos:
            ip = ipinfo.ip
            response = reader.city(ip)
            country = response.country.names.get('zh-CN', 'Unknown')
            city = response.city.names.get('zh-CN', 'Unknown')
            ipinfo.geo_info = '{}-{}'.format(country, city)
            res.append(ipinfo)
    return res
    


def check_args_num(target_num: int):
    return len(sys.argv) == target_num

def main():
    if check_args_num(2):
        ip_str = sys.argv[1]
        if is_ip_address(ip_str):
            res = get_geo_info(ip_str)
            print('{} 归属地为: {}'.format(res))
    else:
        print('Usage:')
        print('  {} <ip>'.format(sys.argv[0]))


if __name__ == '__main__':
    main()
