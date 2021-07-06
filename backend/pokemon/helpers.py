import requests

from pokemon.constants import POKE_API_URL
from pokemon.models import Pokemon


def get_all_pokemon_from_api():
    url = POKE_API_URL + "?limit=802"
    response = requests.get(url)
    data = response.json()
    pokemon_list = []
    for pokemon in data["results"]:
        pokemon_list.append(pokemon)
    return pokemon_list


def get_pokemon_from_api(poke_name):
    url = POKE_API_URL + poke_name
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


def create_pokemon(pokemon_data):
    return Pokemon.objects.create(
        poke_id=pokemon_data["poke_id"],
        name=pokemon_data["name"],
        img_url=pokemon_data["img_url"],
        defense=pokemon_data["defense"],
        attack=pokemon_data["attack"],
        hp=pokemon_data["hp"],
    )


def pokemon_in_api(poke_name):
    url = POKE_API_URL + poke_name
    response = requests.head(url)
    return bool(response)


def is_team_valid(pokemon_data):
    points = 0
    for pokemon in pokemon_data:
        points += pokemon["attack"] + pokemon["defense"] + pokemon["hp"]

    return points <= 600


def get_or_create_pokemon(pokemon_data):
    pokemons = []
    for pokemon in pokemon_data:
        if Pokemon.objects.filter(poke_id=pokemon["poke_id"]).exists():
            pokemons.append(Pokemon.objects.get(poke_id=pokemon["poke_id"]))
        else:
            new_pokemon = create_pokemon(pokemon)
            pokemons.append(new_pokemon)
    return pokemons


def has_repeated_positions(pokemon_position_list):
    return len(pokemon_position_list) != len(set(pokemon_position_list))
