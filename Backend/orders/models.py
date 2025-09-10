from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    
    
    #  Do It
    #  a field to change status of order



    # Cancel order in pending status after 15 min waiting for payment
    def cancel_pending_order(self):
        if self.status == "pending" and self.created_date + timedelta(minutes=15) < timezone.now():
            self.status = "cancelled"
            self.save(update_fields=["status"])

    @property
    def item_count(self):
        """تعداد کل آیتم‌های سفارش"""
        return sum(item.quantity for item in self.items.all())
    def __str__(self):
        return f"Order {self.id} by {self.user}"
    

    def update_total_price(self):
        """محاسبه قیمت کل سفارش"""
        total = sum(item.total_price for item in self.items.all())
        self.total_price = total
        self.save(update_fields=["total_price"])


class OrderItem(models.Model):  
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    customization = models.ForeignKey("customizers.Customization", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)  # تعداد محصول
    price = models.DecimalField(max_digits=12, decimal_places=2)  # قیمت واحد

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        """قیمت کل این آیتم (تعداد × قیمت واحد)"""
        return self.quantity * self.price


    def __str__(self):
        return f"{self.quantity} of {self.product} in Order {self.order.id} wi"
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.update_total_price()  # بعد از ذخیره، قیمت کل سفارش آپدیت بشه

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.order.update_total_price()  # بعد از حذف هم قیمت کل آپدیت بشه