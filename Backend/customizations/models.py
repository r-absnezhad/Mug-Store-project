from django.db import models

# Create your models here.
class Customization(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="customizations")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)  # یا settings.AUTH_USER_MODEL
    custom_text = models.CharField(max_length=200, blank=True, null=True)
    text_color = models.CharField(max_length=20, blank=True, null=True)  # مثل "black", "#FF0000"
    custom_image = models.ImageField(upload_to="customizations/images/", blank=True, null=True)
    placement = models.CharField(
        max_length=20,
        choices=[
            ("left", "Left Side"),
            ("right", "Right Side"),
            ("center", "Center"),
            ("wrap", "Wrap Around"),
        ],
        default="center"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Customization for {self.product.name} by {self.user.username}"