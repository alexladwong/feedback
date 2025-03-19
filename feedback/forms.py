from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Enter your email"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add placeholders
        self.fields["username"].widget.attrs["placeholder"] = "Enter your username"
        self.fields["password1"].widget.attrs["placeholder"] = "Enter your password"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm your password"
