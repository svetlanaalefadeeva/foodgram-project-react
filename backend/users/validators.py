from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Нельзя создать пользователя с именем "me"!'
        )
    return value
