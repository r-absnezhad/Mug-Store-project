from django.contrib import admin
from .models import Customization, CustomizationSettings
# Register your models here.

class CustomizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'display_customization_price', 'custom_text', 'text_color', 'custom_image', 'placement_data')
    list_editable = ( 'custom_text', 'text_color', 'custom_image', 'placement_data')
    search_fields = ('product', 'user',)
    # prepopulated_fields = {'slug': ('name',)}
    ordering = ('user', 'product', '-created_date')
    readonly_fields = ('created_date', 'updated_date', 'display_customization_price', 'final_preview', 'text_price', 'image_price')
    # exclude = ('final_preview',)  # یا این گزینه برای کاملا مخفی کردن فیلد
    fieldsets = [
        (
            None,
            {
                'fields': ('product', 'user', 'custom_text', 'text_color', 'custom_image', 'placement_data')
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

    def display_customization_price(self, obj):
        return obj.customization_price
    display_customization_price.short_description = "Customization Price"

admin.site.register(Customization, CustomizationAdmin)

class CustomizationSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_price', 'image_price', 'created_date', 'updated_date')
    readonly_fields = ('created_date', 'updated_date')
    ordering = ('-created_date',)
    fieldsets = [
        (
            None,
            {
                'fields': ('text_price', 'image_price')
            },
        ),
        (
            'Timestamps',
            {
                'classes': ('collapse',),
                'fields': ('created_date', 'updated_date')
            }
        )
    ]
admin.site.register(CustomizationSettings, CustomizationSettingsAdmin)