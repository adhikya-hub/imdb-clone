from django import forms

from .models import MovieRating


class MovieRatingForm(forms.ModelForm):
    class Meta:
        model = MovieRating
        fields = ["rating"]

        widgets = {
            "rating": forms.Select(
                choices=[(i, i) for i in range(1, 11)],
                attrs={
                    "class": "form-select",
                },
            )
        }
