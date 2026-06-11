from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    display_name = forms.CharField(max_length=80)
    bio = forms.CharField(
        max_length=160,
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    class Meta:
        model = User
        fields = ("email", "username", "display_name", "bio", "password1", "password2")


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")