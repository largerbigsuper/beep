from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializers import NewsSerializer, AdminNewsSerialzier
from .models import mm_News

class NewsViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = []
    serializer_class = NewsSerializer
    queryset = mm_News.published_news()


class AdminNewsViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = AdminNewsSerialzier
    queryset = mm_News.all()

