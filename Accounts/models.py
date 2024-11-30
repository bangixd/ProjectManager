from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .validators import phone_validator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from ProjectManager.custom_validator import CustomPasswordValidator
from django.contrib.auth.hashers import is_password_usable
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('CEO', 'CEO'),
        ('Manager', 'Manager'),
        ('Expert', 'Expert'),
    )
    phone_number = models.CharField(max_length=11, unique=True, validators=[phone_validator])
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=7, choices=ROLE_CHOICES)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_vip = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role', 'email']

    objects = UserManager()

    def __str__(self):
        return f'{self.phone_number} - {self.role} {"(VIP)" if self.is_vip else ""}'


    def set_password(self, raw_password):
        try:
            validate_password(raw_password, self)
        except ValidationError as e:
            raise e
        self.password = make_password(raw_password)

    def save(self, *args, **kwargs):            
        if self.password and not is_password_usable(self.password) and self._password != self.password:
            self.set_password(self.password)
        
        super(User, self).save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='accounts/profile/', default='accounts/profile/defualt/default_avatar.jpg')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'