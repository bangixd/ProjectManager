from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, permissions, status, views
from .serializers import UserSerializer, \
    UserProfileDetailSerializer, UserLogoutSerializer, \
    ChangePasswordSerializers, PasswordResetConfirmSerializer, PasswordResetRequestSerializer
from . import models
from django.utils.http import urlsafe_base64_encode, \
    urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from ProjectManager.settings import DEFAULT_FROM_EMAIL

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
    
    
class ChangePasswordUser(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializers
    model = models.User
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                response = {
                    'status': 'Error',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': "something went wrong",
                    'data': []
                }
                return Response(response)
            
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': "password updated successfully",
                'data': []
            }
            return Response(response)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = models.User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse('accounts:password-rest-confirm', kwargs={'uidb64': uid, 'token': token})
            )
            send_mail('Password Reset Request of POJIO',
                      f'Click the link blow to rest your password: {reset_url}',
                      f'{DEFAULT_FROM_EMAIL}',
                      [email],
                      fail_silently=False, )
            return Response({'detail': 'Password reset link has ben sent'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email not found in database'}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64=None, token=None, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = models.User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, models.User.DoesNotExist):
            user = None
        if user and default_token_generator.check_token(user, token):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user)
            return Response({"detail": 'Password have been reset with the new pass'})
        else:
            return Response({"detail": 'Password have been reset'})
