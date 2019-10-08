from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

from django.conf import settings

class SMSServer:

    def __init__(self, app_id, app_key):
        self.ssender = SmsSingleSender(app_id, app_key)
    
    def _send(self, phone, template_id, params, sign):
        try:
            result = self.ssender.send_with_param(86, phone,template_id, params, sign=sign, extend="", ext="")
        except HTTPError as e:
            print(e)
        except Exception as e:
            print(e)
        print(result)
    
    def send_enroll(self, phone, params, sign):
        return self._send(phone, settings.TENCENT_SMS_TEMPLATE_ID, params)

smsserver = SMSServer(settings.TENCENT_SMS_APP_ID, settings.TENCENT_SMS_APP_KEY)

        
