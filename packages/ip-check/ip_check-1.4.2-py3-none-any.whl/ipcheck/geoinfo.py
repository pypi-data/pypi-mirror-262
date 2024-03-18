#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import geoip2.database
from typing import List
from ipcheck.app.ip_info import IpInfo
from ipcheck.app.utils import is_ip_address, download_file
import argparse

GEO2CITY_DB_NAME = 'GeoLite2-City.mmdb'
GEO2ASN_DB_NAME = 'GeoLite2-ASN.mmdb'
GEO2CITY_DB_PATH = os.path.join(os.path.dirname(__file__), GEO2CITY_DB_NAME)
GEO2ASN_DB_PATH = os.path.join(os.path.dirname(__file__), GEO2ASN_DB_NAME)

def download_geo_db(url :str, path):
    print('正在下载geo database ... ...')
    res = download_file(url, path)
    result_str = '成功。' if res else '失败！'
    print('下载geo database到{} {}'.format(path, result_str))


def check_geo_loc_db():
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


def get_geo_asn(infos: List[IpInfo]) -> List[IpInfo]:
    res = []
    if check_geo_asn_db():
        with geoip2.database.Reader(GEO2ASN_DB_PATH) as reader:
            for info in infos:
                response = reader.asn(info.ip)
                info.asn = response.autonomous_system_number
                info.network = response.network
                res.append(info)
    else:
        res = infos
    return res

def handle_blank_in_str(handle_str: str):
    res = handle_str
    if handle_str:
        res = handle_str.replace(' ', '_')
    return res


# 获取位置信息与组织
def get_geo_loc_org(infos: List[IpInfo]) -> List[IpInfo]:
    if not check_geo_loc_db() or not check_geo_asn_db():
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


def get_loc():
    parser = argparse.ArgumentParser(description='geo-info 获取ip(s) 的归属地信息')
    parser.add_argument("sources", nargs="+", help="待获取归属地信息的ip(s)")
    args = parser.parse_args()
    ips = [ip_str for ip_str in args.sources if is_ip_address(ip_str)]
    if ips:
        ipinfos = [IpInfo(ip) for ip in ips]
        res = get_geo_loc_org(ipinfos)
        for r in res:
            print(r.geo_loc_str)
    else:
        print('请检查是否输入了有效ip(s)')


def get_asn():
    parser = argparse.ArgumentParser(description='geo-asn 获取ip(s) 的ASN 信息')
    parser.add_argument("sources", nargs="+", help="待获取asn信息的ip(s)")
    args = parser.parse_args()
    ips = [ip_str for ip_str in args.sources if is_ip_address(ip_str)]
    if ips:
        ipinfos = [IpInfo(ip) for ip in ips]
        res = get_geo_asn(ipinfos)
        for r in res:
            print(r.geo_asn_str)
    else:
        print('请检查是否输入了有效ip(s)')


def update_db():
    parser = argparse.ArgumentParser(description='geo-db 升级geo 数据库')
    parser.add_argument("url", help="geo db 下载链接")
    args = parser.parse_args()
    url = args.url
    path = None
    if url.endswith(GEO2CITY_DB_NAME):
        path = GEO2CITY_DB_PATH
    if url.endswith(GEO2ASN_DB_NAME):
        path = GEO2ASN_DB_PATH
    if path:
        download_geo_db(url, path)
    else:
        print('请输入包含{} 或 {} 的url'.format(GEO2CITY_DB_NAME, GEO2ASN_DB_NAME))

if __name__ == '__main__':
    get_loc()
