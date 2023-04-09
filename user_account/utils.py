import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_bd_number(value):
    """Validates given phone number on bd format"""
    
    bd_number_pattern_regex = "^01[13-9]\d{8}$"
    if re.match(bd_number_pattern_regex, value) is None:
        raise ValidationError(
            _('%(value)s is not a valid number'),
            params={'value': value},
        )