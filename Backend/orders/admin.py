from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_date', 'updated_date',)
    list_filter = ('status',)
    list_editable = ('status',)
    search_fields = ('user',)
    # prepopulated_fields = {'slug': ('name',)}
    ordering = ('user', 'status', 'total_price',)
    readonly_fields = ('created_date', 'updated_date', 'item_count',)
    fieldsets = [
        (
            None,
            {
                'fields': ('user',)
            }

        ),
        (
            'Details',
            {
                'fields':('status', )
            }
        ),
        (
            'Important time',
            {
                'classes': ('collapse',),
                'fields': ('created_date', 'updated_date'),
            }
        ),

    ]

    def item_count(self, obj):
        return obj.item_count

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'customization', 'display_custom_price', 'total_price', 'created_date', 'updated_date',)
    list_editable = ('product',)
    search_fields = ('product',)
    # prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'price',)
    readonly_fields = ('created_date', 'updated_date', )
    fieldsets = [
        (
            None,
            {
                'fields': ('order', 'product', )
            }
        ),
        (
            'Details',
            {
                'fields': ('customization', 'quantity', )
            }
        ),
        (
            'Important time',
            {
                'classes': ('collapse',),
                'fields': ('created_date', 'updated_date', ),
            }
        ),
    ]

    def display_custom_price(self, obj):
        return obj.price
    display_custom_price.short_description = "Custom Price"

admin.site.register(OrderItem, OrderItemAdmin)