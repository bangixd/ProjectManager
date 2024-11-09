from rest_framework import serializers
from .models import Profile, User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'role',
            'phone_number',
            'password',
            'is_vip',
        ]
        read_only_fields = ['is_vip']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if "password" in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']
    

class UserProfileDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    role = serializers.CharField(source='user.role')
    phone_number = serializers.CharField(source='user.phone_number')
    is_vip = serializers.BooleanField(source='user.is_vip')

    image = serializers.ImageField(source='user.profile.image')

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'role',
            'phone_number',
            'is_vip',
            'image',
        ]
        read_only_fields = ['is_vip', 'profile']


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()
        except Exception as e:
            raise ValidationError("Invalid token or token already blacklisted")