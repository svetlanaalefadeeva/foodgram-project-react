from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CookbookConfig(AppConfig):
    name = 'cookbook'
    verbose_name = _(u'книга рецептов')
