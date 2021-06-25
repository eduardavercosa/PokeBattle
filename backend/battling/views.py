from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView

from battling.forms import CreateBattleForm, CreateTeamForm
from battling.models import Battle, PokemonTeam, Team
from services.battles import set_battle_winner
from services.email import send_battle_invite, send_battle_result


class HomeView(TemplateView):
    template_name = "battling/home.html"


class CreateBattleView(LoginRequiredMixin, CreateView):
    model = Battle
    form_class = CreateBattleForm
    template_name = "battling/create_battle.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.status = Battle.BattleStatus.ONGOING

        battle = form.save()

        team_creator = Team.objects.create(battle=battle, trainer=self.request.user)

        team_opponent = Team.objects.create(battle=battle, trainer=battle.opponent)

        send_battle_invite(battle, team_opponent.id)

        return HttpResponseRedirect(reverse_lazy("create_team", args=(team_creator.id,)))

    def get_initial(self):
        return {"creator_id": self.request.user.id}


class CreateTeamView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = CreateTeamForm
    template_name = "battling/create_team.html"

    def form_valid(self, form):
        battle = self.get_object().battle
        form.save()

        creator = (
            Team.objects.filter(battle=battle, trainer=battle.creator)
            .prefetch_related("pokemons")
            .get()
        )
        creator_pokemons = creator.pokemons.all()

        opponent = (
            Team.objects.filter(battle=battle, trainer=battle.opponent)
            .prefetch_related("pokemons")
            .get()
        )
        opponent_pokemons = opponent.pokemons.all()

        if creator_pokemons and opponent_pokemons:
            set_battle_winner(battle)
            send_battle_result(battle, creator_pokemons, opponent_pokemons)
            messages.success(self.request, "Battle ended! Check your e-mail for results.")

        else:
            messages.success(self.request, "You'll receive an email when the battle is over.")

        return HttpResponseRedirect(reverse_lazy("home"))


class DeleteBattleView(LoginRequiredMixin, DeleteView):
    template_name = "battling/delete_battle.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        return Battle.objects.filter(Q(creator=self.request.user) | Q(opponent=self.request.user))

    def get_success_url(self):
        messages.success(self.request, "Battle refused!")

        return reverse_lazy("home")


class BattleListView(LoginRequiredMixin, ListView):  # pylint: disable=too-many-ancestors
    template_name = "battling/battle_list.html"
    model = Battle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settled_created_battles"] = Battle.objects.filter(
            status=Battle.BattleStatus.SETTLED
        ).filter(creator=self.request.user)
        context["settled_invited_battles"] = Battle.objects.filter(
            status=Battle.BattleStatus.SETTLED
        ).filter(opponent=self.request.user)
        context["ongoing_created_battles"] = Battle.objects.filter(
            status=Battle.BattleStatus.ONGOING
        ).filter(creator=self.request.user)
        context["ongoing_invited_battles"] = Battle.objects.filter(
            status=Battle.BattleStatus.ONGOING
        ).filter(opponent=self.request.user)
        return context


class DetailBattleView(LoginRequiredMixin, DetailView):
    template_name = "battling/battle_detail.html"
    model = Battle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        battle = self.get_object()

        creator = Team.objects.get(battle=battle, trainer=battle.creator.id)
        creator_pokemon_list = PokemonTeam.objects.filter(team=creator)
        context["creator_team"] = [pokemon.pokemon for pokemon in creator_pokemon_list]

        opponent = Team.objects.get(battle=battle, trainer=battle.opponent.id)
        opponent_pokemon_list = PokemonTeam.objects.filter(team=opponent)
        context["opponent_team"] = [pokemon.pokemon for pokemon in opponent_pokemon_list]

        context["settled"] = Battle.BattleStatus.SETTLED
        context["ongoing"] = Battle.BattleStatus.ONGOING

        return context
