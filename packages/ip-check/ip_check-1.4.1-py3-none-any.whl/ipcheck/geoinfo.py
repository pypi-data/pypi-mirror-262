#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import geoip2.database
from typing import List
from ipcheck.app.ip_info import IpInfo
import sys
from ipcheck.app.utils import is_ip_address, download_file

GEO2CITY_DB_NAME = 'GeoLite2-City.mmdb'
GEO2ASN_DB_NAME = 'GeoLite2-ASN.mmdb'
GEO2CITY_DB_PATH = os.path.join(os.path.dirname(__file__), GEO2CITY_DB_NAME)
GEO2ASN_DB_PATH = os.path.join(os.path.dirname(__file__), GEO2ASN_DB_NAME)

def download_geo_db(url :str, path):
    print('正在下载geo database ... ...')
    res = download_file(url, path)
    result_str = '成功。' if res else '失败！'
    print('下载geo database到{} {}'.format(path, result_str))


def check_geo_city_db():
    if os.path.exists(GEO2CITY_DB_PATH):
        return True
    else:
        print('ip 数据库不存在，请手动下载{} 到 {}'.format(GEO2CITY_DB_NAME, GEO2CITY_DB_PATH))
        return False

def check_geo_asn_db():
    if os.path.exists(GEO2ASN_DB_PATH):
        return True
    else:
        print('ip 数据库不存在，请手动下载{} 到 {}'.format(GEO2ASN_DB_NAME, GEO2ASN_DB_PATH))
        return False


def get_geo_city(ip :str):
    if not check_geo_city_db() or not check_geo_asn_db():
        return 'NG-NG-NG'
    with geoip2.database.Reader(GEO2CITY_DB_PATH) as reader1, geoip2.database.Reader(GEO2ASN_DB_PATH) as reader2:
        response1 = reader1.city(ip)
        country = response1.country.name
        country = handle_blank_in_str(country)
        city = response1.city.name
        city = handle_blank_in_str(city)
        response2 = reader2.asn(ip)
        org = response2.autonomous_system_organization
        return '{}-{}({})'.format(country, city, org)

def get_geo_asn_infos(ip: str):
    asn, network = None, None
    if check_geo_asn_db():
        with geoip2.database.Reader(GEO2ASN_DB_PATH) as reader:
            response = reader.asn(ip)
            asn = response.autonomous_system_number
            network = response.network
    return asn, network

def handle_blank_in_str(handle_str: str):
    res = handle_str
    if handle_str:
        res = handle_str.replace(' ', '_')
    return res

def get_geo_cities(infos: List[IpInfo]) -> List[IpInfo]:
    if not check_geo_city_db() or not check_geo_asn_db():
        return infos
    res = []
    with geoip2.database.Reader(GEO2CITY_DB_PATH) as reader1, geoip2.database.Reader(GEO2ASN_DB_PATH) as reader2:
        for ipinfo in infos:
            ip = ipinfo.ip
            response1 = reader1.city(ip)
            country = response1.country.name
            country = handle_blank_in_str(country)
            city = response1.city.name
            city = handle_blank_in_str(city)
            response2 = reader2.asn(ip)
            org = response2.autonomous_system_organization
            ipinfo.geo_info = '{}-{}({})'.format(country, city, org)
            res.append(ipinfo)
    return res


def check_args_num(target_num: int):
    return len(sys.argv) == target_num

def main():
    if check_args_num(2):
        ip_str = sys.argv[1]
        if is_ip_address(ip_str):
            res = get_geo_city(ip_str)
            print('{} 归属地为: {}'.format(ip_str, res))
        else:
            print('请输入有效ip 地址！')
    else:
        print('获取ip 归属地信息')
        print('Usage:')
        print('  {} <ip>'.format(os.path.basename(sys.argv[0])))

def get_asn_details():
    if check_args_num(2):
        ip_str = sys.argv[1]
        if is_ip_address(ip_str):
            asn, network = get_geo_asn_infos(ip_str)
            print('ASN: {} Network: {}'.format(asn, network))
        else:
            print('请输入有效ip 地址！')
    else:
        print('获取ip asn 信息')
        print('Usage:')
        print('  {} <ip>'.format(os.path.basename(sys.argv[0])))

def update_db():
    if check_args_num(2):
        url = sys.argv[1]
        path = None
        if url.endswith(GEO2CITY_DB_NAME):
            path = GEO2CITY_DB_PATH
        if url.endswith(GEO2ASN_DB_NAME):
            path = GEO2ASN_DB_PATH
        if path:
            download_geo_db(url, path)
        else:
            print('请输入包含{} 或 {} 的url'.format(GEO2CITY_DB_NAME, GEO2ASN_DB_NAME))
    else:
        print('  {} <url>'.format(os.path.basename(sys.argv[0])))

if __name__ == '__main__':
    main()
