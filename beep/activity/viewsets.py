from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ActivityCreateSerializer, ActivityListSerializer
from .models import mm_Activity
from .filters import ActivityFilter

class ActivityViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = mm_Activity.all()
    filter_class = ActivityFilter
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityListSerializer
        else:
            return ActivityCreateSerializer
        

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        mm_Activity.update_data(instance.id, 'total_view')
        serializer = self.get_serializer(instance)

        return Response(serializer.data)


        
