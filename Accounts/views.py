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
from rest_framework.permissions import AllowAny
from .permissions import IsAnonymousUser
from rest_framework_simplejwt.views import TokenObtainPairView

class UserCreate(generics.CreateAPIView):
    """
    API endpoint to create a new user account.

    This endpoint allows anonymous users to register a new account by providing 
    the necessary user details (username, email, password, etc.).

    **Method:** POST  
    **Request Body:** User details  
    **Permissions:** Open to anonymous users  
    **Response:** Returns user details upon successful registration.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAnonymousUser]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()


class UserProfileDetail(generics.ListAPIView):
    """
    API endpoint to retrieve the profile details of the authenticated user.

    This endpoint fetches profile information for the currently logged-in user.

    **Method:** GET  
    **Permissions:** Requires user authentication.  
    **Response:** Returns the profile details of the authenticated user.
    """
    serializer_class =  UserProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = 'user' 
    
    def get_queryset(self):
        return models.Profile.objects.filter(user=self.request.user)


class UserLogoutViews(views.APIView):
    """
    API endpoint for logging out a user.

    This endpoint invalidates the user's token to log them out of the system.

    **Method:** POST  
    **Request Body:** Refresh token.  
    **Permissions:** Requires user authentication.  
    **Response:** A success message upon successful logout.
    """
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Successful logout", status=status.HTTP_200_OK)
    
    
class UserLoginView(TokenObtainPairView):
    """
    API endpoint for logging in a user and obtaining JWT tokens.

    This endpoint allows users to log in by providing their username and password,
    and upon successful authentication, it returns access and refresh tokens.

    **Method:** POST  
    **Request Body:** username (or phone number), password  
    **Permissions:** Open to all users  
    **Response:** Returns access and refresh tokens upon successful login.
    """
    permission_classes = [AllowAny]
    
class ChangePasswordUser(generics.UpdateAPIView):
    """
    API endpoint to update the authenticated user's password.

    This endpoint allows a user to update their password by providing the 
    old password and a new password.

    **Method:** PUT  
    **Request Body:** Old password, new password, confirm password.  
    **Permissions:** Requires user authentication.  
    **Response:** A success message upon successful password update.
    """
    serializer_class = ChangePasswordSerializers
    model = models.User
    permission_classes = [permissions.IsAuthenticated]
    
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
    """
    API endpoint to request a password reset.

    This endpoint sends an email containing a password reset link to the user.

    **Method:** POST  
    **Request Body:** Email address.  
    **Permissions:** Open to all users.  
    **Response:** A success message if the reset email is sent successfully.
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = models.User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
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
    """
    API endpoint to confirm a password reset.

    This endpoint allows a user to set a new password using a token and user ID 
    from the password reset link.

    **Method:** POST  
    **Request Body:** New password and confirm password.  
    **Permissions:** Open to users with a valid reset token.  
    **Response:** A success message upon resetting the password.
    """
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64=None, token=None, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = models.User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, models.User.DoesNotExist):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        if user and default_token_generator.check_token(user, token):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user)
            return Response({"detail": 'Password have been reset with the new pass'})
        else:
            return Response({"detail": 'Password have been reset'})
