from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.admin import UserAdmin

from users.models import (
    CustomUser,
    Subscription
)


@register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
    )
    list_filter = (
        'username',
        'email',
        'is_active',
    )
    fieldsets = (
        (None, {
            'fields':(
                'username',
                'password'
            )
        }),
        ('Personal Info', {'fields': (
            'first_name',
            'last_name',
            'email'
        )}),
        ('Permissions', {'fields': (
            'is_staff',
            'is_superuser',
            'is_active'
        )}),
        ('Important dates', {'fields': (
            'last_login',
            'date_joined'
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': (
                'wide',
            ),
            'fields': (
                'username',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'email'
            ),
        }),
    )
    ordering = (
        'username',
    )


@register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    list_display = (
        'user',
        'author'
    )
