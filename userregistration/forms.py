from django import forms
import re
from .models import CustomUser


class UserRegistrationForm(forms.Form):

    CITY_CHOICES = [
        ("", "Select City"),
        ("Chennai", "Chennai"),
        ("Bangalore", "Bangalore"),
        ("Hyderabad", "Hyderabad"),
        ("Pune", "Pune"),
    ]

    COUNTRY_CHOICES = [
        ("India", "India"),
    ]

    user_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Enter User ID"
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Username"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Password"
        })
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Enter Address"
        })
    )

    city = forms.ChoiceField(
        choices=CITY_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "city"
        })
    )

    state = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "state",
            "readonly": True
        })
    )          

    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        initial="India",
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    pin = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "maxlength": "6",
            "placeholder": "Enter PIN"
        })
    )

    aadhaar_file = forms.FileField(
                label="Aadhaar Attachment",
                widget=forms.FileInput(attrs={
                    "class": "form-control",
                    "accept": ".pdf,.jpg,.jpeg,.png"
                })
    )

    eb_bill_file = forms.FileField(
            label="EB Bill Attachment",
            widget=forms.FileInput(attrs={
                "class": "form-control",
                "accept": ".pdf,.jpg,.jpeg,.png"
            })
    )




    # -------------------------
    # Validation
    # -------------------------

    def clean_user_id(self):

        user_id = self.cleaned_data["user_id"]

        if len(str(user_id)) > 6:
            raise forms.ValidationError(
                "User ID cannot exceed 6 digits."
            )

        return user_id

    def clean_pin(self):

        pin = self.cleaned_data["pin"]

        if not re.fullmatch(r"\d{6}", pin):
            raise forms.ValidationError(
                "PIN must contain exactly 6 digits."
            )

        return pin
    

    def clean_user_id(self):

        user_id = self.cleaned_data["user_id"]

        if len(str(user_id)) > 6:
            raise forms.ValidationError(
                "User ID should not exceed 6 digits."
            )

        if CustomUser.objects.filter(user_id=user_id).exists():
            raise forms.ValidationError(
                "User ID already exists."
            )

        return user_id


    def clean_username(self):

        username = self.cleaned_data["username"]

        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Username already exists."
            )

        return username