from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView

from battling.forms import CreateBattleForm, CreateTeamForm
from battling.models import Battle, Team
from services.battles import get_battle_winner


class Home(TemplateView):
    template_name = "battling/home.html"


class CreateBattle(CreateView):
    model = Battle
    form_class = CreateBattleForm
    template_name = "battling/create_battle.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.status = Battle.BattleStatus.ONGOING
        battle = form.save()

        team_creator = Team.objects.create(battle=battle, trainer=self.request.user)

        Team.objects.create(battle=battle, trainer=battle.opponent)

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

            get_battle_winner(battle)

        return super().form_valid(form)


class DeleteBattle(DeleteView):
    template_name = "battling/delete_battle.html"
    success_url = reverse_lazy("home")
    queryset = Battle.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["created_battles"] = Battle.objects.filter(creator=self.request.user)
        context["invited_battles"] = Battle.objects.filter(opponent=self.request.user)

        return context

    def get_success_url(self):
        messages.success(self.request, "Battle refused!")

        return reverse_lazy("home")


class BattleList(ListView):  # pylint: disable=too-many-ancestors
    template_name = "battling/battle_list.html"
    model = Battle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settled_created_battles"] = Battle.objects.filter(status="ST").filter(
            creator=self.request.user
        )
        context["settled_invited_battles"] = Battle.objects.filter(status="ST").filter(
            opponent=self.request.user
        )
        context["ongoing_created_battles"] = Battle.objects.filter(status="OG").filter(
            creator=self.request.user
        )
        context["ongoing_invited_battles"] = Battle.objects.filter(status="OG").filter(
            opponent=self.request.user
        )
        return context


class DetailBattle(DetailView):
    template_name = "battling/battle_detail.html"
    model = Battle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        battle = self.get_object()

        creator = Team.objects.filter(battle=battle, trainer=battle.creator.id)
        context["creator_team"] = creator[0].pokemons.all()

        opponent = Team.objects.filter(battle=battle, trainer=battle.opponent.id)
        context["opponent_team"] = opponent[0].pokemons.all()

        return context
