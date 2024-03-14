#!/usr/bin/env python3
# -*- coding: utf-8 -*-

DEFAULT_CONFIG = '''# 通用配置
[common]
# 测试端口
ip_port = 443


# 可用性检查配置
[valid test]
# 是否测试可用性
enabled = True
# 限制参与valid 测试的ip 数量
ip_limit_count = 1000
# 可用性检测域名
host_name = cloudflare.com
# 可用性检测路径, 固定的，取决于cloudflare
path = /cdn-cgi/trace
# 可用性测试多线程数量
thread_num = 64
# 可用性测试时的网络请求重试次数
max_retry = 2
# 可用性测试的网络请求timeout, 单位 s
timeout = 3
# 是否检测地址信息
get_loc = True

# rtt 测试配置
[rtt test]
enabled = True
# 限制参与rtt 测试的ip 数量
ip_limit_count = 1000
# rtt tcpping 间隔
interval = 0.2
# rtt 测试多线程数量
thread_num = 8
# rtt 测试的网络请求timeout, 单位 s
timeout = 3
# rtt 测试网络请求重试次数
max_retry = 2
# rtt 测试的延时及格值，单位 ms
max_rtt = 300
# 最大丢包率, 100 代表不控制
max_loss = 100
# rtt 测试次数
test_count = 10

# 下载速度测试配置
[speed test]
# 限制参与速度测试的ip 数量
ip_limit_count = 1000
# 测试下载文件的域名
host_name = cloudflaremirrors.com
# 测试下载文件的路径
file_path = /archlinux/iso/latest/archlinux-x86_64.iso
# 测试下载文件的重试次数
max_retry = 2
# 下载测试网络请求timeout, 单位 s
timeout = 3
# 下载时长限制, 单位 s
download_time = 10
# 最小达标速度, 单位 kB/s
download_speed = 5000
# 是否执行快速测速开关
fast_check = False'''