from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def valid_phone_number(value):
    """
    This validator checks if the phone number contains only digits.
    """

    phone_number_pattern = r'^\d{11,12}$'

    if not re.match(phone_number_pattern, value):
        raise ValidationError(
            _("(Phone number must contain only digits and length of 11 digits."),
            code='invalid'
        )


def valid_username(value):
    """
    This validator checks if the username contains only letters, digits, underscores and hyphens.
    """

    username_pattern = r'^[a-zA-Z0-9_-]+$'

    if not re.match(username_pattern, value):
        raise ValidationError(
            _("(Username must contain only letters, digits, underscores and hyphens."),
            code='invalid'
        )
    

def valid_password(value):
    """
    This validator checks if the password contains at least one digit, one uppercase letter, one lowercase letter,
    and length of 10 or more characters.
    """

    password_pattern = r'^(?=.*[a-zA-Z])(?=.*\d).{10,}$'

    if not re.match(password_pattern, value):
        raise ValidationError(
            _("Password must contain at least one digit, one uppercase letter, one lowercase letter, and length of 10 or more characters."),
            code='invalid'
        )
