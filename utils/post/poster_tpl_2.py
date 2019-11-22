#!/usr/bin/python
# 海报生成
# 模版图片要求 宽度 1080

import os
import math
import datetime
import uuid

from PIL import Image, ImageDraw, ImageFont

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

class Template_V2:

    def __init__(self, *args, **kwargs):
        self._width = 375 * 2
        self._width_content = 351 * 2
        self.padding = 12 * 2
        self.padding_content = 13 * 2
        self.save_path = '/tmp/{name}.jpg'.format(name=uuid.uuid4())
        self.head = os.path.join(BASE_PATH, 'templates_v2', 'post_head_v2_702.png')
        self.logo = os.path.join(BASE_PATH, 'templates_v2', 'logo_v2.png')
        self.bg = os.path.join(BASE_PATH, 'templates_v2', 'bg_v2.png')
        self.qrcode = os.path.join(BASE_PATH, 'templates', 'post_qrcode.png')
        self.circle_upper = os.path.join(BASE_PATH, 'templates_v2', 'circle_upper.png')
        self.circle_buttom = os.path.join(BASE_PATH, 'templates_v2', 'circle_buttom.png')
        self.font_pingfang_sc_regular = os.path.join(BASE_PATH, 'font', 'PingFang-SC-Regular.ttf')
        self.font_pingfang_bold = os.path.join(BASE_PATH, 'font', 'PingFang-Bold-2.ttf')
        self.font_title = ImageFont.truetype(self.font_pingfang_bold, 20 * 2)
        self.font_content = ImageFont.truetype(self.font_pingfang_sc_regular, 13 * 2)
        self.font_date = ImageFont.truetype(self.font_pingfang_sc_regular, 12 * 2)
        self.font_slogan = ImageFont.truetype(self.font_pingfang_sc_regular, 11 * 2)
        self.font_alter = ImageFont.truetype(self.font_pingfang_sc_regular, 11 * 2)
        self.color_bg = '#FEFFFF'
        self.color_title = '#333333'
        self.color_content = '#666666'
        self.color_date = '#999999'
        self.color_slogan = '#999999'
        self.color_alter = '#333333'
        self.default_line_height = 8
        self.alter_msg = '投资有风险，入市须谨填。本资讯不作为投资理财建议。'
        self.slogan = 'Amazing things come from the INSIDE '


    def get_head(self):
        """返回头部图片
        """
        head = Image.open(self.head).convert('RGBA')
        # head = head.resize((int(head.width / 2), int(head.height / 2)), Image.ANTIALIAS)
        return head

    def get_title(self, title):
        """返回标题部分图片
        """
        top = 23 * 2
        left = self.padding_content
        max_width = self._width_content - left * 2
        lines = self._get_lines(title, font=self.font_title, max_width=max_width)
        _width, _height = self.font_title.getsize('我')
        title_height = top + len(lines) * _height + (len(lines) - 1) * self.default_line_height
        size = (self._width_content, title_height)
        im = Image.new('RGBA', size)
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
        top = 6 * 2
        max_width = self._width_content
        lines = self._get_lines(date_content, font=self.font_date, max_width=max_width)
        _width, _height = self.font_date.getsize(date_content)
        left = self.padding_content
        title_height = top + _height 
        size = (self._width_content, title_height)
        im = Image.new('RGBA', size)
        draw = ImageDraw.Draw(im)
        
        for index, line in enumerate(lines):
            draw.text((left, top + index * _height), line, font=self.font_date, fill=self.color_date)
        return im

    def get_content(self, content):
        top = 23 * 2
        left = self.padding_content
        max_width = self._width_content - left * 2
        lines = self._get_lines(content, font=self.font_content, max_width=max_width, is_content=True)
        _width, _height = self.font_content.getsize('我')
        im_height = top + len(lines) * _height + (len(lines) - 1) * self.default_line_height
        size = (self._width_content, im_height)
        im = Image.new('RGBA', size)
        draw = ImageDraw.Draw(im)
        
        for index, line in enumerate(lines):
            draw.text((left, top + index * _height + index * self.default_line_height), line, font=self.font_content, fill=self.color_content)
        return im

    def get_circle_upper(self):
        im = Image.open(self.circle_upper).convert('RGBA')
        im = im.resize((351 * 2, 60 * 2), Image.ANTIALIAS)
        return im

    def get_circle_buttom(self):
        im = Image.open(self.circle_buttom).convert('RGBA')
        im = im.resize((351 * 2, 60 * 2), Image.ANTIALIAS)
        return im
    
    def add_content_bg(self, im_content):
        im = Image.new('RGBA', im_content.size)
        im_upper = self.get_circle_upper()
        im_buttom = self.get_circle_buttom()
        size = (im_content.width, im_content.height - im_upper.height - im_buttom.height)
        im_middle = Image.new('RGBA', size, color=self.color_bg)
        box_upper = (0, 0)
        box_middle = (0, im_upper.height)
        box_buttom = (0, im.height - im_buttom.height)
        im.paste(im_upper, box=box_upper, mask=im_upper)
        im.paste(im_middle, box=box_middle, mask=im_middle)
        im.paste(im_buttom, box=box_buttom, mask=im_buttom)
        im.paste(im_content, box=(0, 0), mask=im_content)
        return im
    
    def get_logo(self):
        """获取logo
        """
        top = 40 * 2
        logo = Image.open(self.logo)
        logo = logo.resize((90 * 2, 18 *2))
        size = (self._width_content, logo.height + top)
        im = Image.new('RGBA', size)
        box = (self.padding_content, top)
        r,g,b,a = logo.split()
        im.paste(logo, box=box, mask=a)
        return im

    def get_slogan(self):
        top = 10 * 2
        left = self.padding_content
        _width, _height = self.font_content.getsize(self.slogan)
        im_height = top + _height + top
        size = (self._width_content, im_height)
        im = Image.new('RGBA', size)
        draw = ImageDraw.Draw(im)
        draw.text((left, top), self.slogan, font=self.font_alter, fill=self.color_slogan)
        return im

    def get_alter(self):
        """免责声明"""
        top = 40 * 2
        buttom = 24 * 2
        left = self.padding_content
        _width, _height = self.font_content.getsize(self.alter_msg)
        im_height = top + _height + buttom
        size = (self._width_content, im_height)
        im = Image.new('RGBA', size)
        draw = ImageDraw.Draw(im)
        draw.text((left, top), self.alter_msg, font=self.font_alter, fill=self.color_alter)
        return im

    def get_qrcode(self):
        im = Image.open(self.qrcode)
        size = (80 * 2, 80 * 2)
        im = im.resize(size, Image.ANTIALIAS)
        return im

    def _get_lines(self, text, font, max_width, is_content=False):
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
        max_count_inline = int(max_width / _width)
        expected_count = int(max_width / _width)
        for paragraph in paragraphs:
            # 中文分行， 只做一次估算每行文字个数，然后计算长度做大致补充
            if is_content:
                paragraph = '　　' + paragraph
            start = 0
            end = expected_count
            while end < len(paragraph) + expected_count:
                p = paragraph[start: end]
                _w, _ = font.getsize(p)
                _v = max_width - _w
                more = _v // _width
                if more > 0:
                    end += more
                    p = paragraph[start: end]
                lines.append(p)
                start = end
                end = start + expected_count
        print(lines)
        return lines

    def get_inner_poster(self, title, date, content):
        """生成底部
        """
        im_title = self.get_title(title)
        im_date = self.get_date(date)
        im_content = self.get_content(content)
        im_logo = self.get_logo()
        im_slogan = self.get_slogan()
        im_alter = self.get_alter()

        images = [im_title, im_date, im_content, im_logo, im_slogan, im_alter]
        post_height = sum([im.height for im in images])
        size = (self._width_content, post_height)
        post_image = Image.new(mode='RGBA', size=size)
        current_height = 0
        for im in images:
            box = (0, current_height)
            post_image.paste(im, box=box)
            current_height += im.height

        post_image = self.add_qrcode(post_image)
        post_image = self.add_content_bg(post_image)
        post_image = self.add_head(post_image)
        post_image = self.add_bg(post_image)

        post_image = post_image.convert('RGB')
        post_image.show()
        post_image.save(self.save_path)


    def add_qrcode(self, im):
        qrcode = self.get_qrcode()
        right = 14 * 2
        height = 59 * 2
        box = (self._width_content - qrcode.width - right,  im.height - qrcode.height - height)
        im.paste(qrcode, box)
        return im

    def add_head(self, im):
        im_head = self.get_head()
        middle = 70 * 2
        h = im_head.height + im.height - middle
        size = (self._width_content, h)
        im_content = Image.new(mode='RGBA', size=size)
        # 黏贴头部, 保持透明
        box_head = (0, 0)
        im_content.paste(im_head, box=box_head, mask=im_head)
        # 黏贴内容
        box_im = (0, im_head.height - middle)
        im_content.paste(im, box=box_im, mask=im)

        return im_content
    
    def add_bg(self, im):
        bg = Image.open(self.bg).convert('RGBA')
        h = im.height + self.padding * 2
        size = (self._width, h)
        bg = bg.resize(size, Image.ANTIALIAS)
        box = (self.padding, self.padding)
        bg.paste(im, box=box, mask=im)
        
        return bg


    def generate_post(self, title, date, content):
        
        self.get_inner_poster(title, date, content)

        return self.save_path
        # return self._upload()


if __name__ == "__main__":
    p = Template_V2()
    title = '四方精创半年报：具备从区块链底层平台到应用解决方案的全方位研发交付能力。'
    date = datetime.datetime.now()
    content = """新京报讯（记者 顾志娟）10月19日，首届“直通乌镇”全球互联网大赛首次亮相世界互联网大会，并于今日在乌镇举行半决赛。“直通乌镇”是国际性比赛，其中一个来自香港站的视频AI项目引起了投资人的关注。
该项目主要运用动摄面部识别技术，来自华飞思科技有限公司，搭配无人机和IoT设备， 专门用于抖动场景的视频拍摄， 在大人潮中做远距离的识别和跟踪。据华飞思公司执行董事李丽珍介绍，其人脸识别技术只需一个低清和移动中的摄像头，一般仅需2百万像素，便可以在大范围中实时识别上百张面孔，这突破了传统技术，不用要求厂家安装至少50个固定和高清的摄像头，可以大幅降低成本。
    """
    p.generate_post(title, date, content)
    # p.get_qrcode()
