from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView

from battling.forms import CreateBattleForm, CreateTeamForm
from battling.models import Battle, PokemonTeam, Team
from battling.tasks import run_battle_and_send_result_email
from pokemon.helpers import get_all_pokemon_from_api
from users.models import User


class HomeView(TemplateView):
    template_name = "battling/home.html"


class CreateBattleView(LoginRequiredMixin, CreateView):
    model = Battle
    form_class = CreateBattleForm
    template_name = "battling/create_battle.html"

    def get_initial(self):
        obj_creator = self.request.user
        self.initial = {"creator": obj_creator}
        return self.initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all()
        context["users"] = users
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.status = Battle.BattleStatus.ONGOING

        battle = form.save()

        creator_team_id = Team.objects.only("id").get(battle=battle, trainer=self.request.user).id

        return HttpResponseRedirect(reverse_lazy("create_team", args=(creator_team_id,)))


class CreateTeamView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = CreateTeamForm
    template_name = "battling/create_team.html"

    def get_initial(self):
        obj_user = self.request.user.email
        obj_trainer = self.get_object().trainer.email
        self.initial = {"user": obj_user, "trainer": obj_trainer}
        return self.initial

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
            run_battle_and_send_result_email.delay(battle.id)
            messages.success(self.request, "Battle ended! Check your e-mail for results.")

        else:
            messages.success(self.request, "You'll receive an email when the battle is over.")

        return HttpResponseRedirect(reverse_lazy("home"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pokemons = get_all_pokemon_from_api()
        context["pokemons"] = pokemons
        return context


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

    def get_queryset(self):
        return Battle.objects.select_related("winner", "creator", "opponent")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        battle = context["object"]

        creator_pokemon_qs = PokemonTeam.objects.filter(
            team__battle=battle, team__trainer=battle.creator
        ).select_related("pokemon")
        creator_pokemon_qs = creator_pokemon_qs.order_by("order")
        context["creator_team"] = [pokemon.pokemon for pokemon in creator_pokemon_qs]

        opponent_pokemon_qs = PokemonTeam.objects.filter(
            team__battle=battle, team__trainer=battle.opponent
        ).select_related("pokemon")
        opponent_pokemon_qs = opponent_pokemon_qs.order_by("order")
        context["opponent_team"] = [pokemon.pokemon for pokemon in opponent_pokemon_qs]

        context["settled"] = Battle.BattleStatus.SETTLED
        context["ongoing"] = Battle.BattleStatus.ONGOING

        return context
