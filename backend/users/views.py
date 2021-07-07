from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render  # noqa
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from services.email import send_user_invite

from .forms import InviteUserForm, LoginForm, SignUpForm


class LoginView(DjangoLoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy("home")


class SignupView(FormView):
    template_name = "auth/signup.html"
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignupView, self).form_valid(form)


class InviteUserView(LoginRequiredMixin, FormView):
    template_name = "battling/invite_user.html"
    form_class = InviteUserForm

    def form_valid(self, form):
        creator = self.request.user
        opponent = form.cleaned_data["email"]

        send_user_invite(creator.email, opponent)
        messages.success(self.request, opponent + " was invited to join Pokebattle!")

        return HttpResponseRedirect(reverse_lazy("home"))
