from django.db import models

from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.base_user import AbstractBaseUser

from .managers import CustomUserManager

from django.core.validators import RegexValidator


class CustomUser(AbstractBaseUser, PermissionsMixin):

    CITY_CHOICES = (

        ("Chennai", "Chennai"),

        ("Bangalore", "Bangalore"),

        ("Hyderabad", "Hyderabad"),

        ("Pune", "Pune"),

    )

    STATE_CHOICES = (

        ("Tamil Nadu", "Tamil Nadu"),

        ("Karnataka", "Karnataka"),

        ("Telangana", "Telangana"),

        ("Maharashtra", "Maharashtra"),

    )

    COUNTRY_CHOICES = (

        ("India", "India"),

    )

    # Primary Key

    user_id = models.PositiveIntegerField(
        primary_key=True
    )

    username = models.CharField(
        max_length=150,
        unique=True
    )

    address = models.TextField()

    city = models.CharField(
        max_length=20,
        choices=CITY_CHOICES
    )

    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES
    )

    country = models.CharField(
        max_length=20,
        choices=COUNTRY_CHOICES,
        default="India"
    )

    pin = models.CharField(
    max_length=6,
    validators=[
        RegexValidator(
            regex=r'^\d{6}$',
            message='PIN must contain exactly 6 digits.'
        )
    ]
    )

    full_address = models.TextField(
        blank=True
    )

    # Attachments
    aadhaar_file = models.FileField(
        upload_to='documents/aadhaar/',
        null=True,
        blank=True
    )

    eb_bill_file = models.FileField(
        upload_to='documents/eb_bill/',
        null=True,
        blank=True
    )
    
    
    
    
    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )


    

    objects = CustomUserManager()

    USERNAME_FIELD = "user_id"

    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):

        self.full_address = (
            f"{self.address}, "
            f"{self.city}, "
            f"{self.state}, "
            f"{self.country} - "
            f"{self.pin}"
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username