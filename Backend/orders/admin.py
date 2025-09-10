from django.contrib import admin
from models import Order, OrderItem
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_date', 'updated_date',)
    list_filter = ('status',)
    list_editable = ('status', 'total_price',)
    search_fields = ('user',)
    # prepopulated_fields = {'slug': ('name',)}
    ordering = ('user', 'status', 'total_price',)
    readonly_fields = ('created_date', 'updated_date')
    fieldsets = [
        (
            None,
            {
                'fields': ('user', 'total_price', 'item_count')
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

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'customization', 'price', 'created_date', 'updated_date',)
    list_editable = ('product', 'price',)
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
                'fields': ('customization', 'status', 'quantity', 'price', )
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

admin.site.register(OrderItem, OrderItemAdmin)