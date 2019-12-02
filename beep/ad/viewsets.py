from rest_framework import viewsets
from rest_framework.decorators import action

from .filters import AdFilter
from .serializers import AdSerializer
from .models import mm_Ad



class AdViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = []
    filter_class = AdFilter
    serializer_class = AdSerializer

    def get_queryset(self):
        return mm_Ad.valid().filter(ad_type=mm_Ad.TYPE_LINK)
