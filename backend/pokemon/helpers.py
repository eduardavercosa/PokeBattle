from urllib.parse import urljoin

import requests

from pokemon.constants import POKE_API_URL
from pokemon.models import Pokemon


def get_pokemon_from_api(poke_name):
    url = urljoin(POKE_API_URL, poke_name)
    response = requests.get(url)
    data = response.json()
    return {
        "poke_id": data["id"],
        "name": data["name"],
        "img_url": data["sprites"]["front_default"],
        "defense": data["stats"][3]["base_stat"],
        "attack": data["stats"][4]["base_stat"],
        "hp": data["stats"][5]["base_stat"],
    }


def save_pokemon(poke_name):
    pokemon = get_pokemon_from_api(poke_name)

    if Pokemon.objects.filter(poke_id=pokemon["poke_id"]).exists():
        return Pokemon.objects.get(poke_id=pokemon["poke_id"])
    return Pokemon.objects.create(
        poke_id=pokemon["poke_id"],
        name=pokemon["name"],
        img_url=pokemon["img_url"],
        defense=pokemon["defense"],
        attack=pokemon["attack"],
        hp=pokemon["hp"],
    )


def valid_team(pokemon_names):
    points = 0
    for pokemon_name in pokemon_names:
        pokemon = Pokemon.objects.filter(name=pokemon_name).first()

        points += pokemon.attack + pokemon.defense + pokemon.hp

    return points <= 600
