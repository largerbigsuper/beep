from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

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



        
