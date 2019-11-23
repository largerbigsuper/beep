import requests
import json
import logging

from django.core.cache import cache
from utils.exceptions import ContentException

class WeiXinOpenApi(object):

    MINI_PROGRAM_APP_ID = 'wx300f2f1d32b30613'
    MINI_PROGRAM_APP_SECRET = '2d6b9fef49827381af8dd26b4b66f5e5'
    MINI_PROGRAM_ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(MINI_PROGRAM_APP_ID, MINI_PROGRAM_APP_SECRET)

    def __init__(self):
        self.logger = logging.getLogger('api_weixin')
        self.cache_key = 'wx_token'
        self.check_url = 'https://api.weixin.qq.com/wxa/msg_sec_check?access_token={}'

    def check_content(self, content, raise_exception=True):
        url = self._get_check_url()
        if isinstance(content, dict):
            _content_str = ''
            check_list = ['title', 'content', 'topic_str', 'name', 'sub_name', 'desc', 'text']
            for key in check_list:
                _content_str += content.get(key,'')
            content = _content_str
        data = {
            'content': content
        }
        data_json = json.dumps(data, ensure_ascii=False).encode('utf-8')
        errcode, errmsg = self._check_content(data_json)

        if errcode != 0:
            self.logger.warning('raisk content: {}'.format(data_json))
            if raise_exception:
                raise ContentException(errmsg)
            
            return errcode, errmsg
        return 0, 'ok'

    def _check_content(self, content_utf8, refresh=False):
        if not content_utf8:
            return 0, 'ok'
        headers = {
            'Content-type': 'application/json',
        }
        url = self._get_check_url(refresh)
        response = requests.post(url, data=content_utf8, headers=headers)
        if response.status_code == 200:
            resp_dict = response.json()
            errcode = resp_dict['errcode']
            errmsg = resp_dict['errmsg']
            if errcode == 40001:
                return self._check_content(content_utf8, refresh=True)
            
            return errcode, errmsg

    def get_token(self, refresh=False):
        if refresh:
            token = self._get_token()
        else:
            token = cache.get(self.cache_key)
            if not token:
                token = self._get_token()
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

    def _get_check_url(self, refresh=False):
        token = self.get_token(refresh)
        return self.check_url.format(token)


class WeiXinSubscribeMessageApi(object):

    URL_SEND = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={}'
    URL_TPL_LIST = 'https://api.weixin.qq.com/wxaapi/newtmpl/gettemplate?access_token={}'
    logger = logging.getLogger('api_weixin')

    def gettemplate(self):
        """获取模板列表
        """
        token = WeiXinOpenApi().get_token()
        url = self.URL_TPL_LIST.format(token)
        rep = requests.get(url)
        if rep.status_code == 200:
            print(rep.json())

    def send(self, touser, template_id, page, params_data):
        """推送订阅消息
        """
        token = WeiXinOpenApi().get_token()
        url = self.URL_SEND.format(token)
        headers = {
            'Content-type': 'application/json',
        }
        data = {
            'touser': touser,
            'template_id': template_id,
            'page': page,
            'data': params_data
        }
        data_json = json.dumps(data, ensure_ascii=False).encode('utf-8')
        rep = requests.post(url, data=data_json, headers=headers, verify=False)
        if rep.status_code == 200:
            ret = rep.json()
            if ret['errcode'] != 0:
                self.logger.error(ret)


class WeiXinData(object):

    def __init__(self):
        self.data = {}
    
    def set_key(self, key, value):
        self.data[key] = {'value': value}
    
    def data_json(self):
        return json.dumps(self.data, ensure_ascii=False)


if __name__ == "__main__":
    print(WeiXinOpenApi().check_content('特3456书yuuo莞6543李zxcz蒜7782法fgnv级'))