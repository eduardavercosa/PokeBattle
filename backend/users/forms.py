from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email"]


class LoginForm(AuthenticationForm):
    error_messages = {"invalid_login": ("Email or password is incorrect.")}
