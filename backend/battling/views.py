from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.generic.base import TemplateView

from battling.forms import CreatorForm, OpponentForm
from battling.models import Battle, Team
from services.battles import run_battle_and_send_email


class Home(TemplateView):
    template_name = "battling/home.html"


class CreateBattle(CreateView):
    model = Battle
    form_class = CreatorForm
    template_name = "battling/create_battle.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.save()

        Team.objects.create(battle=Battle.objects.last(), trainer=self.request.user)

        messages.success(self.request, "Your battle was created!")

        return super().form_valid(form)


class EnterBattle(CreateView):
    model = Battle
    form_class = OpponentForm
    template_name = "battling/enter_battle.html"
    success_url = reverse_lazy("home")

    def get_battle(self):
        id_ = Battle.objects.last().id
        return get_object_or_404(Battle, id=id_)

    def form_valid(self, form):
        pokemon = form.cleaned_data

        form.instance.pokemon_1 = pokemon["opponent_pokemon_1"]
        form.instance.pokemon_2 = pokemon["opponent_pokemon_2"]
        form.instance.pokemon_3 = pokemon["opponent_pokemon_3"]

        form.instance.save()

        form.instance.battle_id = self.get_battle().id
        run_battle_and_send_email(form.instance.battle_id)

        return super().form_valid(form)


class DetailBattle(DetailView):
    template_name = "battling/battle_details.html"
    model = Battle

    def get_battle(self):
        id_ = Battle.objects.last().id
        return get_object_or_404(Battle, pk=id_)

    context_object_name = "get_battle"


# def battle_details(request):
#     battle_id = Battle.objects.latest("id")
#     battle_info = Battle.objects.filter(id=battle_id.id).values()[0]

#     # get the pokemons ids from the battles
#     creator_pokemons_id = [battle_info["creator_pokemon_" + str(i) + "_id"] for i in range(1, 4)]
#   opponent_pokemons_id = [battle_info["opponent_pokemon_" + str(i) + "_id"] for i in range(1, 4)]

#     # get the pokemons from the DB
#     creator_pokemon_list = [Pokemon.objects.filter(id=j).values()[0] for j in creator_pokemons_id]
#   opponent_pokemon_list = [Pokemon.objects.filter(id=j).values()[0] for j in opponent_pokemons_id]

#     return render(
#         request,
#         "battling/battle_details.html",
#         {
#             "winner": "jaja",  # battle_id.winner.email.split("@")[0],
#             "creator": battle_id.creator.email.split("@")[0],
#             "opponent": battle_id.opponent.email.split("@")[0],
#             "creator_pkms": creator_pokemon_list,
#             "opponent_pkms": opponent_pokemon_list,
#         },
#     )
