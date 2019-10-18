from random import choice
import string

from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

# from django.conf import settings
TENCENT_SMS_APP_NAME = 'beep'
TENCENT_SMS_APP_ID = '1400257398'
TENCENT_SMS_APP_KEY = '539997d686b988efbe69c5478666670f'
TENCENT_SMS_SIGN = '杭州各一网络科技有限公司'
TENCENT_SMS_TEMPLATE_ID = '427500'
TENCENT_SMS_TEMPLATE_NAME = 'beep'
TENCENT_SMS_TEMPLATE_CONTENT = '您的验证码为{1}，请于{2}分钟内填写。如非本人操作，请忽略本短信。'
TENCENT_SMS_TEMPLATE_LOGIN_ID = '437862'
TENCENT_SMS_TEMPLATE_LOGIN_NAME = 'beep_login'
TENCENT_SMS_TEMPLATE_LOGIN_CONTENT = '{1}为您的登录验证码，请于{2}分钟内填写。如非本人操作，请忽略本短信。'

class SMSServer:

    def __init__(self, app_id, app_key):
        self.ssender = SmsSingleSender(app_id, app_key)
    
    def _gen_code(self):
        code = ''.join([choice(string.digits) for _ in range(4)])
        return code
    
    def _send(self, phone, template_id, sign=TENCENT_SMS_SIGN):
        code = self._gen_code()
        params = [code, 3]
        try:
            result = self.ssender.send_with_param(86, phone, template_id, params, sign=sign, extend="", ext="")
            return code
        except HTTPError as e:
            print(e)
        except Exception as e:
            print(e)
        print(result)
    
    def send_enroll_or_password(self, phone):
        return self._send(phone, TENCENT_SMS_TEMPLATE_ID)
    
    def send_login(self, phone):
        return self._send(phone, TENCENT_SMS_TEMPLATE_LOGIN_ID)
    


smsserver = SMSServer(TENCENT_SMS_APP_ID, TENCENT_SMS_APP_KEY)

if __name__ == "__main__":
    phone = '18258185399'
    params = ['9527', 2]
    # smsserver.send_enroll(phone, params)
    smsserver.send_login(phone, params)

        
