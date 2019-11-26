import base64
import json
from Crypto.Cipher import AES

import logging
logger = logging.getLogger('api_weixin')

class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))
        logger.info('decrypted: {}'.format(decrypted))
        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

def main():
    appId = 'wx300f2f1d32b30613'
    sessionKey = 'S3454hUNUnBVibG+2WIfXQ=='
    encryptedData = 'eyoDfvnAIshzivxh8mj2L6GK2n99T0Pa3qcfJbnuHRrJrDKntAQIY8OZ52L13nY784gtWhWbj7uaangjRmPjACgsGqwRRR27y29iyA3Nc106rIoLBKnR40eD3LgxScfiBf8tV2lCIyjU/nOBFUOvKXinhULhI0GtQhLq5TW611QLlxoh291bK/wtUW131RfRwoexg1CHtH52dCcYYTOPuO5X7Bjj8KB2vxlnysEa9WYPCMEiH4XLXwE1+Q2oKV9lvAKlS3Iut9wC3MVMxXtudr00qjgp6JKfIH7F7iaZUGybqMlW+lbo3ylau+1SIRBRLs9qD672e+Ml6CKtIme9DnSEZ8i4E+XvlbfKbaYtB9ZlDhoRNfaGmHjuIkjkeblpVypnLuTgl8fxN6AuLeQpCD43Bl/kFp4//S6fc0klzshCDXNuJ22ptqRGbSUN+oyk9BPZTkP0CcDd55DrSy/PcQ=='
    iv = 'sqj1RrMAW7LeJfrTMyQ4uA=='

    pc = WXBizDataCrypt(appId, sessionKey)
    """{'openId': 'oGZUI0egBJY1zhBYw2KhdUfwVJJE', 'nickName': 'Band', 'gender': 1, 'language': 'zh_CN', 'city': 'Guangzhou', 'province': 'Guangdong', 'country': 'CN', 'avatarUrl': 'http://wx.qlogo.cn/mmopen/vi_32/aSKcBBPpibyKNicHNTMM0qJVh8Kjgiak2AHWr8MHM4WgMEm7GFhsf8OYrySdbvAMvTsw3mo8ibKicsnfN5pRjl1p8HQ/0', 'unionId': 'ocMvos6NjeKLIBqg5Mr9QjxrP1FA', 'watermark': {'timestamp': 1477314187, 'appid': 'wx4f4bc4dec97d474b'}}
    """

    print(pc.decrypt(encryptedData, iv))

if __name__ == '__main__':
    main()
