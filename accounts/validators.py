import re
from datetime import date

from django.core.exceptions import ValidationError


def validate_username(username: str) -> None:
    if re.search(r'^[a-z_]*$', username) is None:
        raise ValidationError(f'{username} contains non-english letters or characters other than underscore')
    if username.startswith("_") or username.endswith("_"):
        raise ValidationError(f'{username} cannot start or end with an underscore')


def validate_name(name: str):
    if re.search(r'^[A-Za-z]*$', name) is None:
        raise ValidationError(f'{name} contains non-english letters')

