import requests
import json

from django.core.cache import cache
from utils.exceptions import ContentException

class WeiXinOpenApi(object):

    MINI_PROGRAM_APP_ID = 'wx1743dc274cf46871'
    MINI_PROGRAM_APP_SECRET = '648a7ae2cbf66aa7e48992d76f46e621'
    MINI_PROGRAM_ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(MINI_PROGRAM_APP_ID, MINI_PROGRAM_APP_SECRET)

    def __init__(self):
        self.cache_key = 'wx_token'
        self.check_url = 'https://api.weixin.qq.com/wxa/msg_sec_check?access_token={}'

    def check_content(self, content, raise_exception=True):
        url = self._get_check_url()
        if isinstance(content, dict):
            _content_str = ''
            check_list = ['title', 'content', 'topic_str', 'name', 'sub_name', 'desc', 'text']
            for key in check_list:
                _content_str += content.get(key, ' ')
            content = _content_str
        data = {
            'content': content
        }
        data_json = json.dumps(data, ensure_ascii=False).encode('utf-8')
        headers = {
            'Content-type': 'application/json',
        }
        # params = {
        #     'access_token': self.get_token()
        # }
        response = requests.post(url, data=data_json, headers=headers)
        print(url)
        if response.status_code == 200:
            resp_dict = response.json()
            errcode = resp_dict['errcode']
            errmsg = resp_dict['errmsg']
            if errcode != 0 and raise_exception:
                raise ContentException('内容违规')

            return errcode, errmsg


    def get_token(self):
        token = cache.get(self.cache_key)
        # token = ''
        if not token:
            token = self._get_token()
            self.token = token
        return token

    def _get_token(self):
        response = requests.get(self.MINI_PROGRAM_ACCESS_TOKEN_URL)
        if response.status_code == 200:
            data_json = response.json()
            access_token = data_json['access_token']
            expires_in = data_json['expires_in']
            cache.set(self.cache_key, expires_in - 100)
            print(access_token)
            return access_token

    def _get_check_url(self):
        token = self.get_token()
        return self.check_url.format(token)


if __name__ == "__main__":
    print(WeiXinOpenApi().check_content('特3456书yuuo莞6543李zxcz蒜7782法fgnv级'))