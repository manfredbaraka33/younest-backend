from django.shortcuts import render
from .models import Feedback
from rest_framework import generics
from .serializers import FeedbackSerializer


class FeedbackListCreateView(generics.ListCreateAPIView):
    queryset=Feedback.objects.all()
    serializer_class = FeedbackSerializer
    
    
get_feedback=FeedbackListCreateView.as_view()
    
