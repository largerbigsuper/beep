import logging
import json
import hashlib

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from utils.qiniucloud import QiniuService
from . import const

logger = logging.getLogger('wehub')


def socket_test(request):
    return render(request, 'websocket_client_test.html')


@csrf_exempt
@require_POST
def wehub_api(request):

    request_object = json.loads(request.body)
    appid = request_object.get('appid', None)
    action = request_object.get('action', None)
    wxid = request_object.get('wxid', None)
    req_data_dict = request_object.get('data', {})

    if appid is None or action is None or wxid is None:
        rsp_dict = {"error_code": 1, "error_reason": '参数错误', "data": {}}
        logger.error(rsp_dict)
        return JsonResponse(rsp_dict)
    error_code, error_reason, ack_data, ack_type = main_req_process(
        wxid, action, req_data_dict)

    rsp_dict = {'error_code': error_code, 'error_reason': error_reason,
                'ack_type': str(ack_type), 'data': ack_data}

    return JsonResponse(rsp_dict)


@csrf_exempt
@require_POST
def upload_file(request):
    """文件上传
    file_index的md5值是该文件的文件名
    Arguments:
        file_index {string} -- wehub上传的文件索引
        file {file} -- wehub上传的文件   
    """
    # 取出file_index
    file_index = request.POST.get('file_index', None)  # 从form中提取file_index的值
    logger.info("file_index: {}".format(file_index))
    file_data = request.FILES['file']
    logger.info("request.files:{0}".format(file_data))
    file_type = file_data.name.split('.')[-1]
    file_name = hashlib.md5(file_index.encode('utf8')).hexdigest() + '.' + file_type
    
    path = QiniuService.upload_data(file_data, file_name)
    logger.info('[upload_file] {}'.format(path))

    rt_dict = {'error_code': 0,
               'error_reason': '',
               'ack_type': 'upload_file_ack',
               'file_index': file_index}
    return JsonResponse(rt_dict)


# 主要的逻辑处理
def main_req_process(wxid, action, request_data_dict):
    logger.info("action = {0}, data = {1}".format(action, request_data_dict))
    ack_type = 'common_ack'
    if action in const.FIX_REQUEST_TYPES:
        ack_type = str(action)+'_ack'

    if wxid is None or action is None:
        return 1, 'param error:acton is None', {}, ack_type
    if action == 'login':
        nonce = request_data_dict.get("nonce", "")
        logger.info("nonce = {0}".format(nonce))

        ack_data_dict = {}
        protocol_dict = {
            "type": "websocket",
            "param": {
                    'ws_url': const.WEBSOCKET_URL,
                'heartbeat_interval': 30
            }
        }
        ack_data_dict.update({'extension_protocol': protocol_dict})
        # 验证签名
        if len(nonce) > 0:
            nonce_str = str(wxid)+'#'+str(nonce)+'#'+str(const.SECRET_KEY)
            md5_object = hashlib.md5()
            md5_object.update(nonce_str.encode("utf-8"))
            logger.info("nonce_str = {0},md5 = {1}".format(
                nonce_str, str(md5_object.hexdigest())))
            ack_data_dict.update({'signature': str(md5_object.hexdigest())})

        return 0, "", ack_data_dict, ack_type

    return 0, 'no error', {}, ack_type
