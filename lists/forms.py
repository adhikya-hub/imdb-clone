from django import forms

from .models import List


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = [
            "name",
            "description",
            "is_public",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
