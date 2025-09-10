from django.contrib import admin
from .models import Product
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'size', 'color', 'base_price', 'stock', 'is_available',)
    list_filter = ('is_available', 'color', 'size',)
    list_editable = ('base_price', 'stock', 'is_available')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name', 'size', 'base_price', 'stock',)
    readonly_fields = ('created_date', 'updated_date')
    fieldsets = [
        (
            None,
            {
                'fields': ('name', 'description', 'size', 'color', 'image', 'base_price', 'stock', 'is_available')
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


admin.site.register(Product, ProductAdmin)