from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, permissions, status, views
from .serializers import UserSerializer, UserProfileDetailSerializer, UserLogoutSerializer
from . import models

class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()

class UserProfileDetail(generics.ListAPIView):
    serializer_class =  UserProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = 'user' 
    
    def get_queryset(self):
        return models.Profile.objects.filter(user=self.request.user)


class UserLogoutViews(views.APIView):
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Successful logout", status=status.HTTP_200_OK)