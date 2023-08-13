from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email',
                    'first_name', 'last_name',
                    'is_active', 'password')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ()
    list_display = ('id', 'email', 'username')
    list_filter = ('email', 'username')
    search_fields = ('username', 'email')
    ordering = ('username',)
    empty_value_display = '-пусто-'
