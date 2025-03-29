from rest_framework import viewsets 
from .models import Notification 
from .serializers import NotificationSerializer 
from rest_framework.permissions import IsAuthenticated 
from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response


class NotificationCreateListView(generics.ListCreateAPIView): 
    queryset = Notification.objects.all() 
    serializer_class = NotificationSerializer 
    permission_classes = [IsAuthenticated] 
    
    def get_queryset(self): 
        return self.queryset.filter(user=self.request.user).order_by('-created_at')
    
    
my_notifications=NotificationCreateListView.as_view()




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_notifications_as_read(request):
    Notification.objects.filter(user=request.user, read=False).update(read=True)
    return Response({"message": "All notifications marked as read."})