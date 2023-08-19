from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TagsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tags'
    verbose_name = _(u'тег')
    verbose_name_plural = _(u'теги')
