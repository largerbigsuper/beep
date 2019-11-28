import json

import requests

from utils.exceptions import BeepException

class WeiXinApiList:
    api_userinfo = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}'

class WeChatApi(WeiXinApiList):

    def __init__(self, access_token, openid):
        self.access_token = access_token
        self.openid = openid
        self.url_userinfo = self.api_userinfo.format(self.access_token, self.openid)

    def get_user_info(self):
        """获取用户个人信息（UnionID机制）
        # ok
        {
        "openid":"OPENID",
        "nickname":"NICKNAME",
        "sex":1,
        "province":"PROVINCE",
        "city":"CITY",
        "country":"COUNTRY",
        "headimgurl": "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0",
        "privilege":[
        "PRIVILEGE1",
        "PRIVILEGE2"
        ],
        "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"

        }
        # error
        {
        "errcode":40003,"errmsg":"invalid openid"
        }
        """
        resp = requests.get(self.url_userinfo)
        resp_dict = resp.json()
        if resp_dict.get('errcode', 0) != 0:
            msg = json.dumps(resp_dict, ensure_ascii=False)
            raise BeepException(msg)
        else:
            return resp_dict


