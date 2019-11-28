import os
import datetime
import uuid
import logging

from django.core.files.storage import Storage
from django.conf import settings
from qiniu import Auth, put_data, put_file

# 图片样式
beep_logo_cover = '-beep_logo'

class QiniuService:
    # 构建鉴权对象
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY
    qiniuAuth = Auth(access_key, secret_key)
    bucket_name_dict = settings.QINIU_BUCKET_NAME_DICT
    bucket_domain_dict = settings.QINIU_BUCKET_DOMAIN_DICT
    logger = logging.getLogger('qiniu')

    @classmethod
    def get_bucket_name(cls, file_type):
        return cls.bucket_name_dict[file_type]

    @classmethod
    def gen_app_upload_token(cls, bucket_name):
        """
        app 上传token生成
        :param bucket_name: 文件存储空间名
        :param filename: 上传到七牛后保存的文件名
        :param user_id: 用户user_id
        :return:
        """
        # 上传策略示例
        # https://developer.qiniu.com/kodo/manual/1206/put-policy
        # policy = {
        #  # 'callbackUrl':'https://requestb.in/1c7q2d31',
        #  # 'callbackBody':'filename=$(fname)&filesize=$(fsize)'
        #  # 'persistentOps':'imageView2/1/w/200/h/200'
        #     'saveKey': '%s/$(etag)$(ext)' % user_id
        #  }
        policy = {
            # 'saveKey': '%s/$(etag)$(ext)' % user_id,
            'fsizeLimit': 500 * 1024 * 1024
        }
        #3600为token过期时间，秒为单位。3600等于一小时
        token = cls.qiniuAuth.upload_token(bucket_name, None, 3600, policy)
        return token
    
    @classmethod
    def upload_local_image(cls, image_path):
        """上传本地图片
        """
        name = os.path.basename(image_path)
        # 构建鉴权对象
        token = cls.gen_app_upload_token(QiniuService.get_bucket_name('image'))
        ret, info = put_file(token, cls._new_name(name), image_path)
        if info.status_code == 200:
            base_url = '%s%s' % (QiniuService.bucket_domain_dict['image'], ret.get("key"))
            # 表示上传成功, 返回文件名
            return base_url
        else:
            # 上传失败
            raise Exception("上传七牛失败")

    @classmethod
    def upload_data(cls, file_data, save_name):
        """上传内存文件
        """
        cls.logger.info('save_name: {}'.format(save_name))
        # 构建鉴权对象
        token = cls.gen_app_upload_token(QiniuService.get_bucket_name('image'))
        ret, info = put_data(token, save_name, file_data.read(), fname=save_name)

        if info.status_code == 200:
            base_url = '%s%s' % (QiniuService.bucket_domain_dict['image'], ret.get("key"))
            # 表示上传成功, 返回文件名
            cls.logger.info('base_url: {}'.format(base_url))
            return base_url

        else:
            # 上传失败
            cls.logger.error('{} upload failed: {}, {}'.format(save_name, info, ret))
            raise Exception("上传七牛失败")


    @staticmethod
    def _new_name(name):
        new_name = "file/{0}/{1}.{2}".format(datetime.datetime.now().strftime("%Y/%m/%d"), str(uuid.uuid4()).replace('-', ''),
                                             name.split(".").pop())
        return new_name


class StorageObject(Storage):
    def __init__(self):
        self.now = datetime.datetime.now()
        self.file = None

    def _new_name(self, name):
        new_name = "file/{0}/{1}.{2}".format(self.now.strftime("%Y/%m/%d"), str(uuid.uuid4()).replace('-', ''),
                                             name.split(".").pop())
        return new_name

    def _open(self, name, mode):
        return self.file

    def _save(self, name, content):
        """
        上传文件到七牛
        """
        # 构建鉴权对象
        token = QiniuService.gen_app_upload_token(QiniuService.get_bucket_name('image'))
        self.file = content
        file_data = content.file
        ret, info = put_data(token, self._new_name(name), file_data.read())

        if info.status_code == 200:
            base_url = '%s%s' % (QiniuService.bucket_domain_dict['image'], ret.get("key"))
            # 表示上传成功, 返回文件名
            file_type = base_url.split('.')[-1]
            if file_type in ['mp4']:
                return base_url
            else: 
                return base_url + beep_logo_cover
        else:
            # 上传失败
            raise Exception("上传七牛失败")

    def exists(self, name):
        # 验证文件是否存在，因为我这边会去生成一个新的名字去存储到七牛，所以没有必要验证
        return False

    def url(self, name):
        # 上传完之后，已经返回的是全路径了
        return name

def get_filename(filename):
    new_name = "file/{0}/{1}.{2}".format(datetime.datetime.now().strftime("%Y/%m/%d"), str(uuid.uuid4()).replace('-', ''),
                                            filename.split(".").pop())
    return new_name
