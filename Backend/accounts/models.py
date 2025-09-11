from django.db import models
import string, random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_active", True)


        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    This model represents a Custom User Model.
    """
    email = models.EmailField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # is_verified = models.BooleanField(default=False)
    
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

 
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    


class Profile(models.Model):
    """
    This Model represents a User Profile.
    It is linked to the CustomUser model through a OneToOneField.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='profile_images/', default='defaults/none.png')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    birth_date = models.DateField(blank=True, null=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)


    def set_default_profile_image(self): 
        if self.gender == 'F':
            self.image = 'defaults/female.png' 
        elif self.gender == 'M':
            self.image = 'defaults/male.png' 
        else:
            self.image = 'defaults/none.png'

    def save(self, *args, **kwargs):
        self.set_default_profile_image()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name + ' ' + self.last_name}"


@receiver(post_save, sender= CustomUser)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    if hasattr(instance, "profile"):
        instance.profile.save()