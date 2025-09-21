from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class Customization(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="customizations")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    custom_text = models.CharField(max_length=200, blank=True, null=True)
    text_color = models.CharField(max_length=20, blank=True, null=True)  # مثل "black", "#FF0000"
    custom_image = models.ImageField(upload_to="customizations/images/", blank=True, null=True)
    placement_data = models.JSONField(blank=False, null=False)  
    # اینجا مختصات و تنظیمات دقیق ذخیره میشه:
    # {
    #   "text": {"x": 120, "y": 150, "fontSize": 20, "rotation": 0},
    #   "image": {"x": 100, "y": 200, "scale": 0.5, "rotation": 0}
    # }

    # placement = models.CharField(
    #     max_length=20,
    #     choices=[
    #         ("left", "Left Side"),
    #         ("right", "Right Side"),
    #         ("center", "Center"),
    #         ("wrap", "Wrap Around"),
    #     ],
    #     default="center"
    # )

    text_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    image_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    final_preview = models.ImageField(upload_to="customizations/final_previews/", blank=True, null=True)  
    # تصویر نهایی ساخته‌شده (برای چاپ)

    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def customization_price(self):
        """محاسبه هزینه‌ی شخصی‌سازی بر اساس انتخاب کاربر"""
        settings = CustomizationSettings.objects.first()  # فقط رکورد اول
        self.text_price = settings.text_price if settings else 0
        self.image_price = settings.image_price if settings else 0
        
        price = 0
        if self.custom_text:
            price += self.text_price
        if self.custom_image:
            price += self.image_price
        return price
    
    def save(self, *args, **kwargs):
        self.price = self.customization_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Customization for {self.product.name} by {self.user}"
    

class CustomizationSettings(models.Model):
    text_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Customization Setting"
        verbose_name_plural = "Customization Settings"

    def __str__(self):
        return "Global Customization Rates"