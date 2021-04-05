from urllib.parse import urljoin

from django.conf import settings
from django.shortcuts import redirect, render

import requests

from .battles.battle import battle
from .forms import RoundForm, RoundForm2
from .models import Battle


def home(request):
    gamer = Battle.objects.all()
    return render(request, "battling/home.html", {"gamer": gamer})


def get_pokemon_from_api(poke_name):
    url = urljoin(settings.POKE_API_URL, poke_name.lower())
    response = requests.get(url)
    data = response.json()
    info = {
        "poke_id": data["id"],
        "name": data["name"],
        "defense": data["stats"][3]["base_stat"],
        "attack": data["stats"][4]["base_stat"],
        "hp": data["stats"][5]["base_stat"],
    }
    return info


def sumValid(pokemon):
    sum_result = pokemon["attack"] + pokemon["defense"] + pokemon["hp"]
    return sum_result


def check_valid_team(curr_form):
    pokemon1 = get_pokemon_from_api(curr_form.creator_pokemon_1)
    pokemon2 = get_pokemon_from_api(curr_form.creator_pokemon_2)
    pokemon3 = get_pokemon_from_api(curr_form.creator_pokemon_3)
    pokemon1_points = sumValid(pokemon1)
    pokemon2_points = sumValid(pokemon2)
    pokemon3_points = sumValid(pokemon3)
    sum_pokemons_points = pokemon1_points + pokemon2_points + pokemon3_points
    if sum_pokemons_points <= 600:
        return True
    return False


def battle_new(request):
    if request.method == "POST":
        form = RoundForm(request.POST)
        if form.is_valid():
            round_battle = form.save(commit=False)
            valid_team = check_valid_team(round_battle)
            if valid_team:
                form.save(commit=False).save()
                return redirect("invite")
            message = "ERROR: your PKNs sum more than 600 points"
            return render(request, "battling/battle_new.html", {"form": form, "message": message})
    else:
        form = RoundForm()
    return render(request, "battling/battle_new.html", {"form": form})


def invite(request):
    return render(request, "battling/invite.html")


def opponent(request):
    return render(request, "battling/opponent.html")


def round_new2(request):
    battle_info = Battle.objects.latest("id")
    if request.method == "POST":
        form_round2 = RoundForm2(request.POST, instance=battle_info)
        if form_round2.is_valid():
            round_battle = form_round2.save(commit=False)
            valid_team = check_valid_team(round_battle)
            if valid_team:
                form_round2.save()
                return redirect("home")
            message = "ERROR: your PKNs sum more than 600 points"
            return render(
                request,
                "battling/round_new2.html",
                {"form_round2": form_round2, "battle": battle_info, "message": message},
            )
    else:
        form_round2 = RoundForm2()
    return render(
        request, "battling/round_new2.html", {"form_round2": form_round2, "battle": battle_info}
    )


def fights(request):
    battle_id = Battle.objects.latest("id").id
    battle_info = Battle.objects.filter(id=battle_id).values()[0]

    creator_pkms = [get_pokemon_from_api(battle_info["pk1" + str(i)]) for i in range(1, 4)]
    opponent_pkms = [get_pokemon_from_api(battle_info["pk2" + str(i)]) for i in range(1, 4)]

    score = battle(creator_pkms, opponent_pkms)

    winner = "Player1" if score["creator"] > score["opponent"] else "Player2"

    return render(
        request,
        "battling/fights.html",
        {
            "winner": winner,
            "creator_pkms": creator_pkms,
            "opponent_pkms": opponent_pkms,
        },
    )
