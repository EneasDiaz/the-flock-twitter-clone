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

    def clean_content(self):
        content = self.cleaned_data["content"].strip()

        if not content:
            raise forms.ValidationError("Tweet content cannot be empty.")

        if len(content) > 280:
            raise forms.ValidationError("Tweet content cannot exceed 280 characters.")

        return content