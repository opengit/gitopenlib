#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-08-23 21:13:01
# @Description :  网络请求相关的封装，还未测试，仅仅写上去


import asyncio

import aiohttp


async def get(url: str, params: dict = None, **kwargs):
    async with aiohttp.ClientSession().get(url, params=params, **kwargs) as response:
        assert response.status == 200


async def post(url: str, data: bytes, **kwargs):
    async with aiohttp.ClientSession().post(url, data=data, **kwargs) as response:
        assert response.status == 200
        return response
