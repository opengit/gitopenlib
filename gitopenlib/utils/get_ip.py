#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2022
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2022-08-13 22:08:47
# @Description :  Get the ip address.


__version__ = "0.0.1"


import requests
from requests import HTTPError
from lxml import etree
from gitopenlib.utils import basics as gb
import socket


def get_text(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.9999.0 Safari/537.36"
    }
    resp = requests.get(url, headers=header)
    if resp.status_code != 200:
        raise HTTPError("Please check your network!")

    return resp.text


def get_wan(html):
    html = etree.fromstring(html, parser=etree.HTMLParser())
    ipv4 = html.xpath("//p[1]/a[1]/text()")[0]

    info = html.xpath("//p[1]/text()")[-1].split("来自：")[-1].split()
    location, service = info[0], info[1]

    result = {"wan_ip": ipv4, "location": location, "service": service}

    return result


def get_lan():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        return ip


def get_ip():
    url1 = "https://2022.ip138.com/"
    html = get_text(url1)
    wan_res = get_wan(html)

    lan_ip = get_lan()
    wan_res["lan_ip"] = lan_ip
    gb.printj(wan_res, sort_keys=True)
    return wan_res


#  if __name__ == "__main__":
#      get_ip()
