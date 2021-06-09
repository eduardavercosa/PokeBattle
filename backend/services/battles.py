from battling.models import PokemonTeam, Team


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


def get_battle_winner(battle):
    battle_score = {"creator": 0, "opponent": 0}

    # get the team related to the battle and the trainers
    creator = Team.objects.get(battle=battle, trainer=battle.creator.id)
    opponent = Team.objects.get(battle=battle, trainer=battle.opponent.id)

    # get the pokemons names from each team
    creator_team = creator.pokemons.all()
    opponent_team = opponent.pokemons.all()

    for creator_pokemon, opponent_pokemon in zip(creator_team, opponent_team):
        score = battle_round(creator_pokemon, opponent_pokemon)

        battle_score["creator"] += score["creator"]
        battle_score["opponent"] += score["opponent"]

    winner = (
        battle.creator if battle_score["creator"] > battle_score["opponent"] else battle.opponent
    )

    battle.winner = winner
    battle.status = "SETTLED"
    battle.save()

    return winner
