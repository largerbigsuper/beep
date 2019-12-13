#!/usr/bin/python

import os
import math
import datetime
import uuid
from io import BytesIO

import requests
import qrcode
from PIL import Image, ImageDraw, ImageFont

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Template_Activity:

    def __init__(self, *args, **kwargs):
        self._width = 375 * 3
        self._height = 668 * 3
        self._width_content = 351 * 3
        self._width_user_header = 89 * 3
        self._height_user_header = 89 * 3
        self._width_logo = 327 * 3
        self._height_logo = 180 * 3
        self._width_qrcode = 80 * 3
        self._height_qrcode = 80 * 3
        self.padding = 12 * 3
        self.padding_content = 13 * 3
        self.padding_title = 16 * 3
        self.save_path = '/tmp/{name}.jpg'.format(name=uuid.uuid4())
        self.bg = os.path.join(BASE_PATH, 'templates_activity', 'activity_bg.png')
        self.mask_upper = os.path.join(BASE_PATH, 'templates_activity', 'mask_upper@3x.png')
        self.mask_lower = os.path.join(BASE_PATH, 'templates_activity', 'mask_lower@3x.png')
        self.bg = os.path.join(BASE_PATH, 'templates_activity', 'activity_bg.png')
        self.font_pingfang_sc_regular = os.path.join(BASE_PATH, 'font', 'PingFang-SC-Regular.ttf')
        self.font_pingfang_bold = os.path.join(BASE_PATH, 'font', 'PingFang-Bold-2.ttf')
        self.font_user_name = ImageFont.truetype(self.font_pingfang_bold, 28 * 3)
        self.font_user_desc = ImageFont.truetype(self.font_pingfang_bold, 11 * 3)
        self.font_title = ImageFont.truetype(self.font_pingfang_bold, 20 * 3)
        self.color_bg = '#FEFFFF'
        self.color_user_name = '#FFBE60'
        self.color_user_desc = '#FFFFFF'
        self.color_title = '#333333'
        self.default_line_height = 8

    def _download_img(self, url, size):
        """获取图片
        """
        r = requests.get(url)
        im = Image.open(BytesIO(r.content)).convert('RGBA')
        im = im.resize(size, Image.ANTIALIAS)
        # im.show()
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

    def _get_text_im(self, text, font, max_width, fill, padding=0, align='left'):
        """获取文本图片
        """
        if not text:
            text = '     '
        lines = self._get_lines(text, font=font, max_width=max_width - self.padding_content * 2)
        _width, _height = font.getsize('我')
        title_height = len(lines) * _height + (len(lines) - 1) * self.default_line_height
        size = (max_width, title_height)
        im = Image.new('RGBA', size)
        draw = ImageDraw.Draw(im)
        if align == 'left':
            for index, line in enumerate(lines):
                draw.text((padding, index * _height + index * self.default_line_height), line, font=font, fill=fill)
        elif align == 'center':
            line_width, _ = font.getsize(text)
            padding = int((max_width - line_width) / 2)
            draw.text((padding, 0), text, font=font, fill=fill)
        
        return im

    def get_user_header(self, url):
        """返回头部图片
        """
        size = (self._width_user_header, self._height_user_header)
        im = self._download_img(url, size)

        # 画圆
        draw = ImageDraw.Draw(im)
        w, h = im.size
        # 研究源码后发现，如果使用'1'模式的图像，内部也会转换成'L'，所以直接用'L'即可
        alpha_layer = Image.new('L', (w, w), 0)
        draw = ImageDraw.Draw(alpha_layer)
        draw.ellipse((0, 0, w, w), fill=255)
        # 接着替换图像的alpha层
        im.putalpha(alpha_layer)
        
        # 画圈
        draw_circle = ImageDraw.Draw(im)
        r = self._width_user_header / 2
        x = y = r
        draw_circle.ellipse((x-r, y-r, x+r, y+r), width=6)
        # im.show()
        return im

    def get_activity_logo(self, url):
        """返回活动图片
        """
        size = (self._width_logo, self._height_logo)
        im = self._download_img(url, size)
        # im.show()
        return im

    def get_user_name(self, text):
        """获取用户名
        """
        im = self._get_text_im(text=text,
                               font=self.font_user_name,
                               max_width=self._width_content,
                               fill=self.color_user_name,
                               align='center'
                               )
        # im.show()
        return im

    def get_user_desc(self, text):
        """用户简介
        """
        im = self._get_text_im(text=text,
                               font=self.font_user_desc,
                               max_width=self._width_content,
                               fill=self.color_user_desc,
                               align='center'
                               )
        # im.show()
        return im

    def get_title(self, text):
        """返回标题部分图片
        """
        im = self._get_text_im(text=text,
                               font=self.font_title,
                               max_width=self._width_content,
                               fill=self.color_title,
                               padding=self.padding_content,
                               align='left'
                               )
        # im.show()
        return im
    
    def get_logo(self, url):
        """获取logo
        """
        mask_height = 30 * 3
        size = (self._width_logo, self._width_logo + 2 * mask_height)
        logo = Image.new('RGBA', size)
        activity_logo = self.get_activity_logo(url)
        logo.paste(activity_logo, box=(0, mask_height))
        # # 上蒙版
        mask_upper = Image.open(self.mask_upper).resize((95 * 3, 109 * 3), Image.ANTIALIAS)
        logo.paste(mask_upper, box=(- self.padding_content, 0), mask=mask_upper)
        # 下蒙版
        mask_lower = Image.open(self.mask_lower).resize((95 * 3, 109 * 3), Image.ANTIALIAS)
        logo.paste(mask_lower, box=(logo.width - mask_lower.width + self.padding_content,  mask_lower.height + mask_height), mask=mask_lower)

        return logo

    def get_qrcode(self, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=self._width_qrcode,
            border=0,
        )
        qr.add_data(url)
        qr.make(fit=True)
        im = qr.make_image(fill_color="black", back_color="white")
        size = (self._width_qrcode, self._height_qrcode)
        im = im.resize(size, Image.ANTIALIAS)
        return im


    def get_bg(self):
        """获取背景图
        """
        im = Image.open(self.bg).convert('RGBA')
        return im
    
    def generate_post(self, user_cover, user_name, user_desc, title, logo, qrcode_path):
        """生成底部
        """
        im_user_header = self.get_user_header(user_cover)
        im_user_name = self.get_user_name(user_name)
        im_user_desc = self.get_user_desc(user_desc)
        im_title = self.get_title(title)
        # im_logo = self.get_activity_logo(logo)
        im_logo = self.get_logo(logo)
        im_qrcode = self.get_qrcode(qrcode_path)

        post_image = self.get_bg()
        current_height = 0
        # 填充背景
        box_user_header = (143 * 3, 44 * 3)
        post_image.paste(im_user_header, box=box_user_header, mask=im_user_header)

        box_user_name = (self.padding, 140 * 3)
        post_image.paste(im_user_name, box=box_user_name, mask=im_user_name)

        box_user_desc = (self.padding, 180 * 3)
        post_image.paste(im_user_desc, box=box_user_desc, mask=im_user_desc)

        box_title = (self.padding, 224 * 3)
        post_image.paste(im_title, box=box_title, mask=im_title)

        box_logo = (24 * 3, 288 * 3)
        post_image.paste(im_logo, box=box_logo, mask=im_logo)

        box_qrcode = (self._width - 26 * 3 - self._width_qrcode, self._height - 41 * 3 - self._width_qrcode)
        post_image.paste(im_qrcode, box=box_qrcode)

        post_image = post_image.convert('RGB')
        # post_image.show()
        
        post_image.save(self.save_path)
        print(self.save_path)
        
        return self.save_path


if __name__ == "__main__":
    p = Template_Activity()
    user_cover = 'https://cdn.beepcrypto.com/1576123714473.BitUniverse logo.jpg'
    user_name = '小喵'
    user_desc = '行情分析，币圈资讯，区块链创造未来。'
    title = '具备从区块链底层平台到应用解决方案！'
    logo = 'https://cdn.beepcrypto.com/1576122174189.banner75.png-beep_logo-beep_logo'
    qrcode_path = 'https://cdn.beepcrypto.com/1576122174189.banner75.png-beep_logo-beep_logo'

    p.generate_post(user_cover, user_name, user_desc, title, logo, qrcode_path)
