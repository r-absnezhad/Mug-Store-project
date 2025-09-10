from django.contrib import admin
from .models import Customization
# Register your models here.

class CustomizationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customization, CustomizationAdmin)