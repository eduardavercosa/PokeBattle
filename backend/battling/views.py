from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.base import TemplateView

from battling.forms import CreatorForm, TeamForm
from battling.models import Battle, Team


# from services.battles import run_battle_and_send_email


class Home(TemplateView):
    template_name = "battling/home.html"


class CreateBattle(CreateView):
    model = Battle
    form_class = CreatorForm
    template_name = "battling/create_battle.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        battle = form.save()

        team = Team.objects.create(battle=battle, trainer=self.request.user)

        return HttpResponseRedirect(reverse_lazy("create_team", args=(team.id,)))


class CreateTeam(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = "battling/create_team.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        battle = self.get_object().battle
        battle_creator = battle.creator

        # self.get_object().trainer will be replaced by self.request.user
        # when the login feature is implemented
        if self.get_object().trainer == battle_creator:
            messages.success(self.request, "Your battle was created!")

        else:
            messages.success(self.request, "Battle ended! Check e-mail for results.")

            # run_battle_and_send_email(battle)

        return super().form_valid(form)


class JoinBattle(UpdateView):
    model = Team
    form_class = CreatorForm
    template_name = "battling/join_battle.html"

    def get_battle(self):
        return get_object_or_404(Battle, id=self.kwargs["pk"])

    def form_valid(self, form):
        form.instance.creator = self.request.user
        battle = self.get_battle()

        team = Team.objects.create(battle=battle, trainer=self.request.user)

        return HttpResponseRedirect(reverse_lazy("create_team", args=(team.id,)))


class DetailBattle(DetailView):
    template_name = "battling/battle_details.html"
    model = Battle

    def get_battle(self):
        id_ = Battle.objects.last().id
        return get_object_or_404(Battle, pk=id_)

    context_object_name = "get_battle"
