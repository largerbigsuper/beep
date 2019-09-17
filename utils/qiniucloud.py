from qiniu import Auth
from django.conf import settings


class QiniuService:
    # 构建鉴权对象
    print(settings.SITE_ID)
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY
    qiniuAuth = Auth(access_key, secret_key)
    bucket_name_dict = settings.QINIU_BUCKET_NAME_DICT
    bucket_domain_dict = settings.QINIU_BUCKET_DOMAIN_DICT

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
            'fsizeLimit': 10 * 1024 * 1024
        }
        #3600为token过期时间，秒为单位。3600等于一小时
        token = cls.qiniuAuth.upload_token(bucket_name, None, 3600, policy)
        return token
