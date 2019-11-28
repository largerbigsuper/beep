#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午11:31
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : exceptions.py
from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import ugettext_lazy as _


class DBException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('数据异常')
    default_code = '数据异常'


class ContentException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('内容违规')
    default_code = '内容违规'

class BeepException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('未知错误')
    default_code = '未知错误'