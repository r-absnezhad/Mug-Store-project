from django.contrib import admin
from .models import Review
# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ["id","profile","product","rating", "comment"]
    ordering = ["rating", "profile__last_name", "profile__first_name"]
    fieldsets = (
        ("Details", {"fields": ("profile", "product", "rating", "comment")}),
    )  
admin.site.register(Review, ReviewAdmin)