from django.db.models import Sum
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .models import mm_SearchHistory, mm_SearchKeyWord
from .serializers import SearchHistorySerializer, SearchKeyWordSerializer
from .filters import SearchKeyWordFilter



class SearchHistoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """搜索历史
    list -- 我的搜索历史
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SearchHistorySerializer

    def get_queryset(self):
        if self.action == 'list':
            return mm_SearchHistory.filter(user=self.request.user)


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

