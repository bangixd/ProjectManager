from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

class UserAdminForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Password", help_text=(
        "Passwords are stored as hashed values. You can change the password "
        "using <a href=\"../password/\">this form</a>."
    ))
    # password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['phone_number', 'password', 'first_name', 'last_name', 'role', 'email', 'is_active', 'is_staff']

    def clean_password(self):
        # If password field is empty, return the initial password (no change)
        if not self.cleaned_data['password']:
            return self.initial.get("password")
        return self.cleaned_data['password']
