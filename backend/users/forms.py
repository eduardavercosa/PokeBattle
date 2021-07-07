from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ["email", "password1", "password2"]:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    error_messages = {"invalid_login": ("Email or password is incorrect.")}


class InviteUserForm(forms.Form):
    email = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data
