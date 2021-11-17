#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-10-26 14:48:44
# @Description :  存放一些其他工具函数


__version__ = "0.0.4"

import time
from email.mime.text import MIMEText
from smtplib import SMTP_SSL


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
        start_time = time.time()
        start_ftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 执行回调主函数
        func_main()
        spend_time = time.time() - start_time
        end_ftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 邮件内容
        if message is None or len(message) == 0:
            message = (
                "<p>任务开始时间：</p>"
                + "<p>{}</p>".format(start_ftime)
                + "<p>任务结束时间：</p>"
                + "<p>{}</p>".format(end_ftime)
                + "<p>任务耗时：</p>"
                + "<p>{}</p>".format(spend_time)
            )

        msg = MIMEText(message, "html", _charset="utf-8")

        # 邮件主题描述
        if subject is None or len(subject) == 0:
            #  subject = "【任务执行完毕】({})".format(now_time)
            subject = "【任务】开始：{}，结束：{}，耗时：{}秒".format(
                start_ftime, end_ftime, spend_time
            )
        msg["Subject"] = subject
        msg["From"] = username
        msg["To"] = to_addr

    # 发送邮件
    with SMTP_SSL(host=host, port=host_port) as smtp:
        # 登录发送邮件服务器
        smtp.login(user=username, password=password)
        # 实际发送、接收邮件配置
        smtp.sendmail(from_addr=username, to_addrs=to_addr, msg=msg.as_string())
