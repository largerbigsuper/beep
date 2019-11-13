import requests
from django.core.cache import cache
from django.conf import settings

from celery import shared_task
from config.celery import app


@app.task
def update_ticker_cache():
    """更新首页货币价格信息
    """

    cache_key = settings.CACHE_KEY_COIN_DATA
    
    market_list = ['BTC', 'ETH', 'LTC', 'XRP', 'BCH', 'EOS', 'TRX']
    market_key_list = [x + '_USDT' for x in market_list]
    api_url = 'https://www.mxc.ceo/open/api/v1/data/ticker?market='
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        "Accept": "application/json",
    }
    data = {}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        all_data = response.json()['data']
        for market_key in market_key_list:
            data[market_key] = all_data[market_key]
    cache.set(cache_key, data, 60 * 60)


