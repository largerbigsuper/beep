#!/usr/bin/python
# 海报生成
# 模版图片要求 宽度 1080

import os
import math
import datetime
import uuid

from PIL import Image, ImageDraw, ImageFont



BASE_PATH = os.path.dirname(os.path.abspath(__file__))

class Template_V1:

    def __init__(self, *args, **kwargs):
        self.save_path = '/tmp/{name}.png'.format(name=uuid.uuid4())
        self.head = os.path.join(BASE_PATH, 'templates', 'post_head.png')
        self.bottom = os.path.join(BASE_PATH, 'templates', 'post_bottom.png')
        self.qrcode = os.path.join(BASE_PATH, 'templates', 'post_qrcode.png')
        self.font_pingfang_sc_regular = os.path.join(BASE_PATH, 'font', 'PingFang-SC-Regular.ttf')
        self.font_pingfang_bold = os.path.join(BASE_PATH, 'font', 'PingFang-Bold-2.ttf')
        self.font_title = ImageFont.truetype(self.font_pingfang_bold, 45)
        self.font_content = ImageFont.truetype(self.font_pingfang_sc_regular, 35)
        self.font_date = ImageFont.truetype(self.font_pingfang_sc_regular, 30)
        self.font_alter = ImageFont.truetype(self.font_pingfang_sc_regular, 30)
        self.color_bg = '#FEFFFF'
        self.color_title = '#000000'
        self.color_content = '#8E8F90'
        self.color_date = '#8E8F90'
        self.color_alter = '#8E8F90'
        self.default_line_height = 8
        self.alter_msg = '免责声明：本文不代表币博立场，且不构成投资建议，请谨慎对待。'


    def get_head(self):
        """返回头部图片
        """
        im = Image.open(self.head)
        return im

    def get_title(self, title):
        """返回标题部分图片
        """
        top = 20
        left = 90
        max_width = 1080 - left * 2
        lines = self._get_lines(title, font=self.font_title, max_width=max_width)
        _width, _height = self.font_title.getsize('我')
        title_height = top + len(lines) * _height + (len(lines) - 1) * self.default_line_height
        size = (1080, title_height)
        im = Image.new('RGBA', size, color=self.color_bg)
        draw = ImageDraw.Draw(im)
        
        for index, line in enumerate(lines):
            draw.text((left, top + index * _height + index * self.default_line_height), line, font=self.font_title, fill=self.color_title)
        # im.show()
        return im

    def get_date(self, date):
        weekday_map = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期日',
        }
        date_format = '%Y-%m-%d %H:%M'
        date_str = date.strftime(date_format)
        weekday_str = weekday_map[date.weekday()]
        date_content = date_str + ' '  + weekday_str
        top = 20
        max_width = 1080
        lines = self._get_lines(date_content, font=self.font_date, max_width=max_width)
        _width, _height = self.font_date.getsize(date_content)
        left = (max_width - _width) / 2
        title_height = top + _height 
        size = (1080, title_height)
        im = Image.new('RGBA', size, color=self.color_bg)
        draw = ImageDraw.Draw(im)
        
        for index, line in enumerate(lines):
            draw.text((left, top + index * _height), line, font=self.font_date, fill=self.color_title)
        # im.show()
        return im

    def get_content(self, content):
        top = 20
        left = 80
        max_width = 1080 - left * 2
        lines = self._get_lines(content, font=self.font_content, max_width=max_width)
        _width, _height = self.font_content.getsize('我')
        im_height = top + len(lines) * _height + (len(lines) - 1) * self.default_line_height
        size = (1080, im_height)
        im = Image.new('RGBA', size, color=self.color_bg)
        draw = ImageDraw.Draw(im)
        
        for index, line in enumerate(lines):
            draw.text((left, top + index * _height + index * self.default_line_height), line, font=self.font_content, fill=self.color_content)
        # im.show()
        return im

    def get_alter(self):
        """免责声明"""

        top = 20
        left = 80
        _width, _height = self.font_content.getsize(self.alter_msg)
        im_height = top + _height + top
        size = (1080, im_height)
        im = Image.new('RGBA', size, color=self.color_bg)
        draw = ImageDraw.Draw(im)
        draw.text((left, top), self.alter_msg, font=self.font_alter, fill=self.color_alter)
        # im.show()
        return im

    def get_bottom(self):
        im = Image.open(self.bottom)
        qrcode = self.get_qrcode()
        right = 90
        height = 20
        box = (1080 - qrcode.width - right,  height)
        im.paste(qrcode, box)
        return im

    def get_qrcode(self):
        im = Image.open(self.qrcode)
        size = (180, 180)
        im = im.resize(size, Image.ANTIALIAS)
        # im.resize(size)
        # im.show()
        return im

    def _get_lines(self, text, font, max_width):
        """切分字符串为行
        
        Arguments:
            text {[type]} -- [description]
            font {[type]} -- [description]
            max_width {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        lines = []
        paragraphs = text.split('\n')
        _width, _height = font.getsize('我')
        print('width:', _width, 'height:', _height)
        max_count_inline = int(max_width / _width)
        for paragraph in paragraphs:
            length = len(paragraph)
            line_count = math.ceil(length / max_count_inline * 1.0)
            for line_num in range(line_count):
                cut_from = line_num * max_count_inline
                cut_to = (line_num + 1) * max_count_inline
                lines.append(paragraph[cut_from: cut_to])
        print(lines)
        return lines

    def generate_post(self, title, date, content):
        post_height = 0
        post_width = 1080
        im_head = self.get_head()
        im_title = self.get_title(title)
        im_date = self.get_date(date)
        im_content = self.get_content(content)
        im_alter = self.get_alter()
        im_bottom = self.get_bottom()
        images = [im_head, im_title, im_date, im_content, im_alter, im_bottom]
        post_height = sum([im.height for im in images])
        size = (post_width, post_height)
        post_image = Image.new(mode='RGBA', size=size)
        current_height = 0
        for im in images:
            box = (0, current_height)
            post_image.paste(im, box=box)
            current_height += im.height
        # post_image.show()
        post_image.save(self.save_path)



if __name__ == "__main__":
    p = Template_V1()
    title = '四方精创半年报：具备从区块链底层平台到应用解决方案的全方位研发交付能力。'
    date = datetime.datetime.now()
    content = """新京报讯（记者 顾志娟）10月19日，首届“直通乌镇”全球互联网大赛首次亮相世界互联网大会，并于今日在乌镇举行半决赛。“直通乌镇”是国际性比赛，其中一个来自香港站的视频AI项目引起了投资人的关注。
该项目主要运用动摄面部识别技术，来自华飞思科技有限公司，搭配无人机和IoT设备， 专门用于抖动场景的视频拍摄， 在大人潮中做远距离的识别和跟踪。据华飞思公司执行董事李丽珍介绍，其人脸识别技术只需一个低清和移动中的摄像头，一般仅需2百万像素，便可以在大范围中实时识别上百张面孔，这突破了传统技术，不用要求厂家安装至少50个固定和高清的摄像头，可以大幅降低成本。
    """
    p.generate_post(title, date, content)
    # p.get_qrcode()
