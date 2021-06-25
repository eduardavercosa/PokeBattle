from battling.models import Battle, PokemonTeam, Team


def battle_round(creator_pokemon, opponent_pokemon):
    round_score = {"creator": 0, "opponent": 0}

    # Creator's pokemon attacks
    if creator_pokemon.attack > opponent_pokemon.defense:
        round_score["creator"] += 1
    else:
        round_score["opponent"] += 1

    # Opponents's pokemon attacks
    if opponent_pokemon.attack > creator_pokemon.defense:
        round_score["creator"] += 1
    else:
        round_score["opponent"] += 1

    #  In case of draw
    if round_score["creator"] == round_score["opponent"]:
        if creator_pokemon.hp > opponent_pokemon.hp:
            round_score["creator"] += 1
        else:
            round_score["opponent"] += 1

    # Final Round Score
    creator_won = {"creator": 1, "opponent": 0}
    opponent_won = {"creator": 0, "opponent": 1}

    if round_score["creator"] > round_score["opponent"]:
        return creator_won
    return opponent_won


def set_battle_winner(battle):
    battle_score = {"creator": 0, "opponent": 0}

    # get the team related to the battle and the trainers
    creator = Team.objects.get(battle=battle, trainer=battle.creator.id)
    opponent = Team.objects.get(battle=battle, trainer=battle.opponent.id)

    # get pokemon in the right order
    creator_pokemon_list = PokemonTeam.objects.filter(team=creator)
    opponent_pokemon_list = PokemonTeam.objects.filter(team=opponent)

    # get the pokemons data from each team
    creator_team = [pokemon.pokemon for pokemon in creator_pokemon_list]
    opponent_team = [pokemon.pokemon for pokemon in opponent_pokemon_list]

    for creator_pokemon, opponent_pokemon in zip(creator_team, opponent_team):
        score = battle_round(creator_pokemon, opponent_pokemon)

        battle_score["creator"] += score["creator"]
        battle_score["opponent"] += score["opponent"]

    winner = (
        battle.creator if battle_score["creator"] > battle_score["opponent"] else battle.opponent
    )

    battle.winner = winner

    battle.status = Battle.BattleStatus.SETTLED

    battle.save()

    return winner
