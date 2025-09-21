from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def item_count(self):
        """تعداد کل آیتم‌های سفارش"""
        return self.items.aggregate(total=Sum('quantity'))['total'] or 0
        # return sum(item.quantity for item in self.items.all())
    
    def save(self, *args, **kwargs):
        # بار اول فقط ذخیره کن، بعد آیتم‌ها اضافه می‌شن و total_price آپدیت میشه
        if not self.pk:  
            super().save(*args, **kwargs)
        else:
            self.update_total_price()

    # def save(self, *args, **kwargs):
    #     self.update_total_price()
    #     super().save(*args, **kwargs)
    #  Do It
    #  a field to change status of order

    # Cancel order in pending status after 15 min waiting for payment
    # وقتی صدا زده بشه عمل میکنه
    # def cancel_pending_order(self):
    #     if self.status == "pending" and self.created_date + timedelta(minutes=15) < timezone.now():
    #         self.status = "cancelled"
    #         self.save(update_fields=["status"])

    

    def update_total_price(self):
        # """محاسبه قیمت کل سفارش"""
        # total = sum(item.total_price for item in self.items.all())
        # self.total_price = total
        # # self.save(update_fields=["total_price"])

        """محاسبه قیمت کل سفارش بهینه با Aggregate"""
        total = self.items.aggregate(
            total=Sum(
                ExpressionWrapper(F("quantity") * F("price"), output_field=DecimalField())
            )
        )["total"] or 0
        self.total_price = total
        # self.save(update_fields=['total_price'])

    def __str__(self):
        return f"Order {self.id} by {self.user}"


class OrderItem(models.Model):  
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    customization = models.ForeignKey("customizations.Customization", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)  # تعداد محصول
    price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)  # قیمت واحد

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        """قیمت کل این آیتم (تعداد × قیمت واحد)"""
        return self.quantity * self.price


    def __str__(self):
        return f"{self.quantity} × {self.product} in Order {self.order.id}"
    

    def save(self, *args, **kwargs):
        # محاسبه قیمت بر اساس قیمت پایه محصول و سفارشی‌سازی
        base_price = self.product.base_price
        extra = self.customization.customization_price if self.customization else 0
        self.price = base_price + extra
        
        super().save(*args, **kwargs)
        # self.order.save()  # بعد از ذخیره، قیمت کل سفارش آپدیت بشه
        self.order.update_total_price()
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # self.order.save()  # بعد از حذف هم قیمت کل آپدیت بشه
        self.order.update_total_price()