import requests
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.core.cache import cache
from django.http import JsonResponse

@require_GET
def data_ticker(request):
    """首页货币价格 15s刷新一次
    """
    market_list = ['BTC', 'ETH', 'LTC', 'XRP', 'BCH', 'EOS', 'TRX']
    market_key_list = [x + '_USDT' for x in market_list]
    # market = request.GET.get('market', '')

    api_url = 'https://www.mxc.ceo/open/api/v1/data/ticker?market='

    cache_key = 'coin_price'
    data = cache.get(cache_key, {})
    if not data:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
            "Accept": "application/json",
        }
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            all_data = response.json()['data']
            data = {}
            for market_key in market_key_list:
                data[market_key] = all_data[market_key]
            cache.set(cache_key, data, 15)
        else:
            data = {}
    ret_data = {
        'msg': 'ok',
        'data': data
    }

    return JsonResponse(data=ret_data)
