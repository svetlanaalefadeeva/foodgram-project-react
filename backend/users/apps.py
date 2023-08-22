from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = _(u'пользователь')
    verbose_name_plural = _(u'пользователи')
