import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def phone_validator(phone: str):
    if re.search(r'\D+', phone):
        raise ValidationError(_('%(phone)s must consist of digits.'
                                ' Please, check your phone number and try again'),
                              params={'phone': phone})
