from rest_framework import serializers
from .models import Profile, User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from ProjectManager.custom_validator import CustomPasswordValidator
from django.contrib.auth import password_validation

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user creation and management.

    - Fields: Includes basic user information such as first name, last name, email, role, phone number, and password.
    - Password: Write-only field; validated using custom and Django validators.
    - VIP status: Read-only field.
    - Automatically hashes the password upon user creation.
    """
    
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
        
    

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        
        custom_validator = CustomPasswordValidator()
        try:
            custom_validator.validate(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    def create(self, validated_data):
        if "password" in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.

    - Fields: Includes the profile image of the user.
    """
    
    class Meta:
        model = Profile
        fields = ['image']
    

class UserProfileDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed user profile view.

    - Combines data from the user and profile models.
    - Fields: Includes user’s name, email, role, phone number, VIP status, and profile image.
    - Read-only for all fields.
    """
    
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
    """
    Serializer for user logout.

    - Validates and processes refresh tokens to blacklist them.
    - Raises an error if the token is invalid or already blacklisted.
    """
    
    refresh = serializers.CharField(required=True)

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()
        except Exception as e:
            raise serializers.ValidationError("Invalid token or token already blacklisted")
    

class ChangePasswordSerializers(serializers.Serializer):
    """
    Serializer for changing the user password.

    - Fields: Includes old password, new password, and confirm password.
    - Validations: Ensures the old password matches the user’s current password and new passwords are valid and match.
    """
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': "new password fields didn't match"})
        return attrs
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset.

    - Field: Includes user email to initiate the password reset process.
    - Sends a password reset link to the provided email.
    """
    
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming password reset.

    - Fields: Includes new password and confirm password.
    - Validations: Ensures new passwords are valid and match.
    - Saves the new password for the user upon successful validation.
    """
    
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': "New password and confirm password didn't match"})
        password_validation.validate_password(attrs['new_password'])
        return attrs

    def save(self, user):
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user