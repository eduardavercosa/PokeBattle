from django.conf import settings
from django.urls import reverse

from templated_email import send_templated_mail


def send_battle_invite(battle, team_opponent_id):
    battle_invite_path = reverse(
        "create_team",
        args=[team_opponent_id],
    )
    battle_invite_url = settings.HOST + battle_invite_path

    battle_delete_path = reverse(
        "delete_battle",
        args=[battle.id],
    )
    battle_delete_url = settings.HOST + battle_delete_path

    send_templated_mail(
        template_name="battle_invite",
        from_email=settings.FROM_EMAIL,
        recipient_list=[battle.opponent.email],
        context={
            "battle_creator": battle.creator.email.split("@")[0],
            "battle_opponent": battle.opponent.email.split("@")[0],
            "battle_invite_url": battle_invite_url,
            "battle_delete_url": battle_delete_url,
        },
    )


def send_battle_result(battle, creator_pokemon_qs, opponent_pokemon_qs):
    battle_detail_path = reverse("battle_detail", args=[battle.id])
    battle_details_url = settings.HOST + battle_detail_path
    send_templated_mail(
        template_name="battle_result",
        from_email=settings.FROM_EMAIL,
        recipient_list=[battle.creator.email, battle.opponent.email],
        context={
            "battle_creator": battle.creator.email.split("@")[0],
            "battle_opponent": battle.opponent.email.split("@")[0],
            "battle_winner": battle.winner.email.split("@")[0],
            "battle_id": battle.id,
            "creator_team": [pokemon.name for pokemon in creator_pokemon_qs],
            "opponent_team": [pokemon.name for pokemon in opponent_pokemon_qs],
            "battle_details_url": battle_details_url,
        },
    )
