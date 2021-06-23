from django.contrib.auth import login
from django.shortcuts import render  # noqa
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import SignUpForm


class Signup(FormView):
    template_name = "auth/signup.html"
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Signup, self).form_valid(form)
