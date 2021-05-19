from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.base import TemplateView

from battling.forms import CreateBattleForm, CreateTeamForm
from battling.models import Battle, Team


# from services.battles import run_battle_and_send_email


class Home(TemplateView):
    template_name = "battling/home.html"


class CreateBattle(CreateView):
    model = Battle
    form_class = CreateBattleForm
    template_name = "battling/create_battle.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        battle = form.save()

        team_creator = Team.objects.create(battle=battle, trainer=self.request.user)

        Team.objects.create(battle=battle, trainer=battle.opponent)

        return HttpResponseRedirect(reverse_lazy("create_team", args=(team_creator.id,)))


class CreateTeam(UpdateView):
    model = Team
    form_class = CreateTeamForm
    template_name = "battling/create_team.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        battle = self.get_object().battle
        battle_creator = battle.creator

        if self.request.user == battle_creator:
            messages.success(self.request, "Your battle was created!")

        else:
            messages.success(self.request, "Battle ended! Check e-mail for results.")

            # run_battle_and_send_email(battle)

        return super().form_valid(form)


class EditBattle(UpdateView):
    model = Battle
    form_class = CreateBattleForm
    template_name = "battling/edit_battle.html"

    def get_battle(self):
        return get_object_or_404(Battle, id=self.kwargs["pk"])

    def form_valid(self, form):
        battle = self.get_battle()

        team = Team.objects.create(battle=battle, trainer=self.request.user)

        battle = form.save()

        return HttpResponseRedirect(reverse_lazy("create_team", args=(team.id,)))


class DetailBattle(DetailView):
    template_name = "battling/battle_details.html"
    model = Battle

    def get_battle(self):
        return get_object_or_404(Battle, id=self.kwargs["pk"])
