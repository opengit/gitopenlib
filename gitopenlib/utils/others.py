#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-10-26 14:48:44
# @Description :  存放一些其他工具函数


__version__ = "0.0.1"

import time
from email.mime.text import MIMEText
from smtplib import SMTP_SSL


def sendMail(
    to_addrs="sunjiajiacn@qq.com",
    username="sunjiajiacn@qq.com",
    password=None,
    message=None,
    subject=None,
):
    """
    Args:
        message: 邮件内容
        subject: 邮件主题描述
        to_addrs: 实际收件人，多个目标地址使用英文逗号隔开
        username: 账户名
        password: 帐户密码
    """
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 邮件内容
    if message is None or len(message) == 0:
        message = "<p>任务执行完毕....</p>" + "<p>{}</p>".format(now_time)

    msg = MIMEText(message, "html", _charset="utf-8")

    # 邮件主题描述
    if subject is None or len(subject) == 0:
        subject = "【任务执行完毕】({})".format(now_time)
    msg["Subject"] = subject

    # 发送邮件
    with SMTP_SSL(host="smtp.qq.com", port=465) as smtp:
        # 登录发送邮件服务器
        smtp.login(user=username, password=password)
        # 实际发送、接收邮件配置
        smtp.sendmail(
            from_addr=username, to_addrs=to_addrs.split(","), msg=msg.as_string()
        )
