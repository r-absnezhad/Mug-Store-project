from django.contrib import admin
from .models import Customization
# Register your models here.

class CustomizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user',)
    list_editable = ( 'custom_text', 'text_color', 'custom_image', 'placement')
    search_fields = ('product', 'user',)
    # prepopulated_fields = {'slug': ('name',)}
    ordering = ('user', 'product', '-created_at')
    readonly_fields = ('created_date', 'updated_date')
    fieldsets = [
        (
            None,
            {
                'fields': ('product', 'user', 'custom_text', 'text_color', 'custom_image', 'placement')
            },
        ),
        (
            'Advanced Options',
            {
                'classes': ('collapse',),
                'fields': ('created_date', 'updated_date')
            }
        )
    ]

admin.site.register(Customization, CustomizationAdmin)