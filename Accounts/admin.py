from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile
from .forms import UserAdminForm

class CustomUserAdmin(BaseUserAdmin):
    form = UserAdminForm
    list_display = ('phone_number', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'role')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        ('Create User', {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()

def save_model(self, request, obj, form, change):
    # Only hash the password if it has been changed
    if change:  # Check if the object is being updated
        old_password = obj.password  # Get the existing hashed password
        new_password = form.cleaned_data.get('password')
        
        # If password field is empty, keep the old password
        if not new_password:
            obj.password = old_password
        elif not new_password.startswith('argon2'):
            # Hash only if the new password is not already hashed
            obj.set_password(new_password)
    else:
        # For new objects, hash the password as usual
        obj.set_password(form.cleaned_data.get('password'))
    
    super().save_model(request, obj, form, change)
    
    
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
