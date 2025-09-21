from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile
# Register your models here.


class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the Custom User model.
    - Customizes how Users records are displayed, filtered, searched, and ordered in the admin panel.
    """
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active", "is_superuser", "is_verified")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        ("Authentication", {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_verified")}),
        ("Group Permissions", {"fields": ("groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login",)}),
    )  
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff", "is_active", "is_superuser", "is_verified")
            }
        ),
    ) 


admin.site.register(CustomUser, CustomUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Profile model.
    - Customizes how Profile records are displayed, filtered, searched, and ordered in the admin panel.
    """

    model = Profile
    list_display = ["get_fullname", "get_email", "phone_number", "gender", "image"]
    list_filter = ["gender"]
    search_fields = ["user__email", "first_name", "last_name"]
    ordering = ["last_name", "first_name", "user__email"]
    fieldsets = (
        ("Authentication", {"fields": ("first_name", "last_name", "phone_number", "gender")}),
        ("Important Dates", {"fields": ("birth_date", )}),
    )  

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = "Email"

    def get_fullname(self, obj):
        return (
            obj.first_name + " " + obj.last_name
            if (obj.first_name and obj.last_name)
            else "---"
        )

    get_fullname.short_description = "Fullname"


admin.site.register(Profile, ProfileAdmin)