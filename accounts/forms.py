from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields["username"].widget.attrs["placeholder"] = "Enter username"
        self.fields["email"].widget.attrs["placeholder"] = "Enter email"
        self.fields["password1"].widget.attrs["placeholder"] = "Enter password"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm password"


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "profile_picture",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Username",
            }
        )

        self.fields["profile_picture"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )
