from django import forms

from .models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 3,
                    "maxlength": 280,
                    "placeholder": "What's happening?",
                }
            )
        }