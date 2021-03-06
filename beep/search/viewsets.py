from itertools import chain

from django.db.models import Sum
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .models import mm_SearchHistory, mm_SearchKeyWord, mm_HotSearch
from .serializers import SearchHistorySerializer, SearchKeyWordSerializer, HotSearchSerializer
from .filters import SearchKeyWordFilter
from utils.pagination import Size_15_Pagination
from beep.ad.models import mm_Ad



class SearchHistoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """搜索历史
    list -- 我的搜索历史
    clear_history -- 清空搜索记录
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SearchHistorySerializer

    def get_queryset(self):
        if self.action in ['list', 'clear_history']:
            return mm_SearchHistory.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def clear_history(self, request):
        queryset = self.get_queryset()
        queryset.update(user=None)
        return Response()



class SearchKeyWordViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """热门搜索
    list -- 热门搜索
    """

    permission_classes = []
    serializer_class = SearchKeyWordSerializer
    queryset = mm_SearchKeyWord.all()
    filter_class = SearchKeyWordFilter

    def list(self, request, *args, **kwargs):
        """推荐搜索关键字
        """
        queryset = self.filter_queryset(self.get_queryset())
        # 需指定order_by() 不然groupby会去读默认的ordering字段做groupby
        data = queryset.values('keyword').annotate(frequency=Sum('frequency')).order_by('-frequency')

        return Response(data=data[:10])


class HotSearchViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """热搜榜
    """

    permission_class = []
    serializer_class = HotSearchSerializer
    pagination_class = Size_15_Pagination

    def get_queryset(self):
        return mm_HotSearch.all().order_by('-is_top', '-task_id', '-frequency')

    # FIXME 增加缓存一分钟
    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        """去除置顶重复的内容
        """
        hot_list = mm_HotSearch.filter(is_top=True).all()[:30]
        hot_names_set = {hot.keyword for hot in hot_list}
        normal_list = list(mm_HotSearch.exclude(is_top=True).order_by('-task_id', '-frequency')[:30])
        for hot in normal_list:
            if hot.keyword in hot_names_set:
                normal_list.remove(hot)
        page = list(chain(hot_list, normal_list))[:15]
        ad_hotSearch_dict = mm_Ad.get_hot_search_ad()
        if ad_hotSearch_dict:
            ad_blog_ids = {ad_blog.id for ad_blog in ad_hotSearch_dict.values()}
            _page = [obj for obj in page if obj.id not in ad_blog_ids]
            ads = sorted(ad_hotSearch_dict.items())
            for index, blog in ads:
                if index < 1:
                    continue
                idx = index - 1
                if len(_page) >= index:
                    _page.insert(idx, blog)
            page = _page
        serializer = HotSearchSerializer(page, many=True)
        data = {
            'results': serializer.data
        }
        return Response(data=data)

