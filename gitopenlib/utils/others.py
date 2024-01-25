#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-10-26 14:48:44
# @Description :  存放一些其他工具函数


__version__ = "0.4.1"

from re import sub
import time
import traceback
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
import requests

from gitopenlib.utils import basics as gb

import os
import urllib.parse
import urllib.request


def sendBotMsg(
    key=None,
    subject=None,
    message=None,
    func_main=None,
):
    """
    发送任务执行完毕的通知到企业微信群组机器人。

    Args:
        key: 企业微信机器人的key
        subject: 主题描述
        message: 通知内容
        func_main: 回调方法，启用这个功能，可以将任务开始和结束时间都统计
    """
    spend_time = ""
    if func_main is None:
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 邮件内容
        if message is None or len(message) == 0:
            message = "\n任务执行完毕....\n\n" + "{}\n\n".format(now_time)

        # 主题描述
        if subject is None or len(subject) == 0:
            subject = "【任务执行完毕】({})".format(now_time)

    else:
        is_success = True
        start_time = time.time()
        start_ftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 执行回调主函数，也可能报错，但是报错的话，也算任务执行完毕，因此也要发送邮件，
        # 不过是通知任务失败的邮件
        try:
            func_main()
        except Exception:
            is_success = False
            traceback.print_exc()
            error_info = traceback.format_exc()
        spend_time = time.time() - start_time
        spend_time = round(spend_time, 3)
        spend_time = gb.fmt_seconds(spend_time)
        end_ftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 通知内容
        if message is None or len(message) == 0:
            message = (
                "\n任务成功！\n\n"
                + "任务开始时间：\n\n"
                + "{}\n\n".format(start_ftime)
                + "任务结束时间：\n\n"
                + "{}\n\n".format(end_ftime)
                + "任务耗时：\n\n"
                + "{}\n\n".format(spend_time)
            )
            if not is_success:
                message = message.replace(
                    "\n任务成功！\n\n",
                    "\n任务失败！\n\n错误信息：{}\n\n".format(error_info),
                )

        # 主题描述
        if subject is None or len(subject) == 0:
            #  subject = "【任务执行完毕】({})".format(now_time)
            subject = "【任务成功】开始：{}".format(start_ftime)
            if not is_success:
                subject = subject.replace("成功", "失败")

    # 发送信息到微信
    def sc_send(key, subject="", message=""):
        url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}".format(key)
        content = f"{subject}\n{message}"
        data = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": ["@all"],
            },
        }
        r = requests.post(url, json=data, headers={"Content-Type": "application/json"})

        return r.text

    ret = sc_send(key, subject, message)
    if '"errmsg":"ok"' in ret:
        if len(spend_time) > 0:
            gb.pts(f"# Sent to WeChat successfully ({spend_time})... ")
        else:
            gb.pts("# Sent to WeChat successfully...")
    else:
        gb.pts("# Send to WeChat failed...")


def sendTaskMsg(
    key=None,
    subject=None,
    message=None,
    func_main=None,
):
    """
    发送任务执行完毕的通知到微信。

    Args:
        key: server酱的key
        subject: 主题描述
        message: 通知内容
        func_main: 回调方法，启用这个功能，可以将任务开始和结束时间都统计
    """
    if func_main is None:
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 邮件内容
        if message is None or len(message) == 0:
            message = "任务执行完毕....\n\n" + "{}\n\n".format(now_time)

        # 主题描述
        if subject is None or len(subject) == 0:
            subject = "【任务执行完毕】({})".format(now_time)

    else:
        is_success = True
        start_time = time.time()
        start_ftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 执行回调主函数，也可能报错，但是报错的话，也算任务执行完毕，因此也要发送邮件，
        # 不过是通知任务失败的邮件
        try:
            func_main()
        except Exception:
            is_success = False
            traceback.print_exc()
            error_info = traceback.format_exc()
        spend_time = time.time() - start_time
        spend_time = round(spend_time, 3)
        end_ftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 通知内容
        if message is None or len(message) == 0:
            message = (
                "任务成功！\n\n"
                + "任务开始时间：\n\n"
                + "{}\n\n".format(start_ftime)
                + "任务结束时间：\n\n"
                + "{}\n\n".format(end_ftime)
                + "任务耗时：\n\n"
                + "{}\n\n".format(gb.fmt_seconds(spend_time))
            )
            if not is_success:
                message = message.replace(
                    "任务成功！\n\n",
                    "任务失败！\n\n错误信息：{}\n\n".format(error_info),
                )

        # 主题描述
        if subject is None or len(subject) == 0:
            #  subject = "【任务执行完毕】({})".format(now_time)
            subject = "【任务成功】开始：{}".format(start_ftime)
            if not is_success:
                subject = subject.replace("成功", "失败")

    # 发送信息到微信
    def sc_send(text, desp="", key="[SENDKEY]"):
        postdata = urllib.parse.urlencode({"text": text, "desp": desp}).encode("utf-8")
        url = f"https://sctapi.ftqq.com/{key}.send"
        req = urllib.request.Request(url, data=postdata, method="POST")
        with urllib.request.urlopen(req) as response:
            result = response.read().decode("utf-8")
        return result

    ret = sc_send(subject, message, key)
    if '"code":0' in ret:
        gb.pts("# Sent to WeChat successfully...")
    else:
        gb.pts("# Send to WeChat failed...")


def sendTaskOK(
    to_addr="sunjiajiacn@qq.com",
    username="gitopen@sina.cn",
    host="smtp.sina.cn",
    host_port=465,
    password=None,
    subject=None,
    message=None,
    func_main=None,
):
    """
    发送任务执行完毕通知邮件。

    Args:
        to_addr: 邮件接收地址
        username: 发件人地址
        host: smtp地址（SSL）
        host_port: smtp端口（SSL）
        password: 帐户密码
        subject: 邮件主题描述
        message: 邮件内容
        func_main: 回调方法，启用这个功能，可以将任务开始和结束时间都统计
    """
    if func_main is None:
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 邮件内容
        if message is None or len(message) == 0:
            message = "<p>任务执行完毕....</p>" + "<p>{}</p>".format(now_time)

        msg = MIMEText(message, "html", _charset="utf-8")

        # 邮件主题描述
        if subject is None or len(subject) == 0:
            subject = "【任务执行完毕】({})".format(now_time)
        msg["Subject"] = subject
        msg["From"] = username
        msg["To"] = to_addr

    else:
        is_success = True
        start_time = time.time()
        start_ftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 执行回调主函数，也可能报错，但是报错的话，也算任务执行完毕，因此也要发送邮件，
        # 不过是通知任务失败的邮件
        try:
            func_main()
        except Exception as e:
            is_success = False
            traceback.print_exc()
            error_info = traceback.format_exc()
        spend_time = time.time() - start_time
        spend_time = round(spend_time, 3)
        end_ftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 邮件内容
        if message is None or len(message) == 0:
            message = (
                "<p><h2>任务成功！</h2></p>"
                + "<p>任务开始时间：</p>"
                + "<p>{}</p>".format(start_ftime)
                + "<p>任务结束时间：</p>"
                + "<p>{}</p>".format(end_ftime)
                + "<p>任务耗时：</p>"
                + "<p>{}</p>".format(gb.fmt_seconds(spend_time))
            )
            if not is_success:
                message = message.replace(
                    "<p><h2>任务成功！</h2></p>",
                    "<p><h2>任务失败！</h2></p><p><b>错误信息：{}</b></p>".format(
                        error_info
                    ),
                )

        msg = MIMEText(message, "html", _charset="utf-8")

        # 邮件主题描述
        if subject is None or len(subject) == 0:
            #  subject = "【任务执行完毕】({})".format(now_time)
            subject = "【任务成功】开始：{}，结束：{}，耗时：{}".format(
                start_ftime, end_ftime, gb.fmt_seconds(spend_time)
            )
            if not is_success:
                subject = subject.replace("成功", "失败")
        msg["Subject"] = subject
        msg["From"] = username
        msg["To"] = to_addr

    # 发送邮件
    with SMTP_SSL(host=host, port=host_port) as smtp:
        # 登录发送邮件服务器
        smtp.login(user=username, password=password)
        # 实际发送、接收邮件配置
        smtp.sendmail(from_addr=username, to_addrs=to_addr, msg=msg.as_string())
