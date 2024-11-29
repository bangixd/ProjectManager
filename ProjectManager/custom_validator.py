import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if user:
            if password == user.phone_number:
                raise ValidationError(_('The password must not be the same as the phone number'))

        common_passwords = ["123456", "password", "qwe", "qwerty", "111111"]
        if password in common_passwords:
            raise ValidationError(_('password is not valid from common_passwords'))

        regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d\W]{8,}$'
        if not re.match(regex, password):
            raise ValidationError(_('password is not valid from regex'))

    def get_help_text(self):
        return _("Your password must pass the custom validation checks.")