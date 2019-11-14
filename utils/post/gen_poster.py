#!/usr/bin/python
# 海报生成
# 模版图片要求 宽度 1080

import os
import math
import datetime
from PIL import Image, ImageDraw, ImageFont

from .poster_tpl_1 import Template_V1
from .poster_tpl_2 import Template_V2

from ..qiniucloud import QiniuService

class Post:

    def generate_post(self, title, date, content, tpl_id=1):
        if tpl_id == 1:
            path =  Template_V1().generate_post(title, date, content)
        else:
            path = Template_V2().generate_post(title, date, content)
        
        return self._upload(path)

    def _upload(self, path):
        return QiniuService.upload_local_image(path)

if __name__ == "__main__":
    p = Post()
    title = '四方精创半年报：具备从区块链底层平台到应用解决方案的全方位研发交付能力。'
    date = datetime.datetime.now()
    content = """新京报讯（记者 顾志娟）10月19日，首届“直通乌镇”全球互联网大赛首次亮相世界互联网大会，并于今日在乌镇举行半决赛。“直通乌镇”是国际性比赛，其中一个来自香港站的视频AI项目引起了投资人的关注。
该项目主要运用动摄面部识别技术，来自华飞思科技有限公司，搭配无人机和IoT设备， 专门用于抖动场景的视频拍摄， 在大人潮中做远距离的识别和跟踪。据华飞思公司执行董事李丽珍介绍，其人脸识别技术只需一个低清和移动中的摄像头，一般仅需2百万像素，便可以在大范围中实时识别上百张面孔，这突破了传统技术，不用要求厂家安装至少50个固定和高清的摄像头，可以大幅降低成本。
    """
    p.generate_post(title, date, content)
    # p.get_qrcode()
