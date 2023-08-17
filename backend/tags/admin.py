from django.contrib import admin

from .models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'color'
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    filter_horizontal = ('recipes',)
