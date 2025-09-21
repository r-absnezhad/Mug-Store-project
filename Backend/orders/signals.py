from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def cancel_empty_orders(sender, instance, created, **kwargs):
    """
    اگه سفارش جدید ساخته شد ولی هیچ آیتمی نداره، خودکار کنسل بشه
    """
    if created and instance.items.count() == 0:
        instance.status ="cancelled"