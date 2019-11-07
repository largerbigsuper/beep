import requests
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.core.cache import cache
from django.http import JsonResponse
from django.conf import settings

@require_GET
def data_ticker(request):
    """首页货币价格 15s刷新一次
    """
    cache_key = settings.CACHE_KEY_COIN_DATA
    data = cache.get(cache_key, {})
    
    ret_data = {
        'msg': 'ok',
        'data': data
    }

    return JsonResponse(data=ret_data)
