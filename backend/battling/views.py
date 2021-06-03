from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView

from battling.forms import CreateBattleForm, CreateTeamForm
from battling.models import Battle, PokemonTeam, Team
from services.battles import get_battle_winner


# from services.email import send_battle_invite, send_battle_result


class Home(TemplateView):
    template_name = "battling/home.html"


class CreateBattle(CreateView):
    model = Battle
    form_class = CreateBattleForm
    template_name = "battling/create_battle.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.status = "ONGOING"
        battle = form.save()

        team_creator = Team.objects.create(battle=battle, trainer=self.request.user)

        Team.objects.create(battle=battle, trainer=battle.opponent)

        # send_battle_invite(battle, team_opponent.id)

        return HttpResponseRedirect(reverse_lazy("create_team", args=(team_creator.id,)))

    def get_initial(self):
        return {"creator_id": self.request.user.id}


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

            # creator = Team.objects.filter(battle=battle, trainer=battle.creator.id)
            # creator_pokemon = PokemonTeam.objects.filter(team=creator[0])
            # creator_team = [pokemon.pokemon for pokemon in creator_pokemon]

            # opponent = Team.objects.filter(battle=battle, trainer=battle.opponent.id)
            # opponent_pokemon = PokemonTeam.objects.filter(team=opponent[0])
            # opponent_team = [pokemon.pokemon for pokemon in opponent_pokemon]

            get_battle_winner(battle)

            # send_battle_result(battle, creator_team, opponent_team)

        return super().form_valid(form)


class DeleteTeam(DeleteView):
    template_name = "battling/delete_team.html"
    success_url = reverse_lazy("home")
    queryset = Team.objects.all()

    def get_success_url(self):
        messages.success(self.request, "Battle refused!")

        return reverse_lazy("home")


class SettledBattles(ListView):  # pylint: disable=too-many-ancestors
    template_name = "battling/settled_battles.html"
    model = Battle

    queryset = Battle.objects.filter(status="SETTLED")


class OnGoingBattles(ListView):  # pylint: disable=too-many-ancestors
    template_name = "battling/ongoing_battles.html"
    model = Battle

    queryset = Battle.objects.filter(status="ONGOING")


class DetailBattle(DetailView):
    template_name = "battling/battle_detail.html"
    model = Battle

    def get_object(self, queryset=None):
        battle = get_object_or_404(Battle, id=self.kwargs["pk"])

        return battle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        battle = self.get_object()

        creator = Team.objects.filter(battle=battle, trainer=battle.creator.id)
        creator_pokemon = PokemonTeam.objects.filter(team=creator[0])

        if creator_pokemon:
            context["creator_team"] = [
                creator_pokemon[0].pokemon,
                creator_pokemon[1].pokemon,
                creator_pokemon[2].pokemon,
            ]

        opponent = Team.objects.filter(battle=battle, trainer=battle.opponent.id)
        opponent_pokemon = PokemonTeam.objects.filter(team=opponent[0])

        if opponent_pokemon:
            context["opponent_team"] = [
                opponent_pokemon[0].pokemon,
                opponent_pokemon[1].pokemon,
                opponent_pokemon[2].pokemon,
            ]

        return context
