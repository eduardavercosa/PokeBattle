from django.db import models
from django.utils.translation import gettext_lazy as _

from pokemon.models import Pokemon
from users.models import User


class Battle(models.Model):
    class BattleStatus(models.TextChoices):
        ONGOING = "OG", _("Ongoing")
        SETTLED = "ST", _("Settled")

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator_battles")
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="opponent_battles")
    status = models.CharField(
        max_length=10, choices=BattleStatus.choices, default=BattleStatus.ONGOING, blank=True
    )
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="battle_win", null=True)

    def is_upperclass(self):
        return self.status in {
            self.BattleStatus.ONGOING,
            self.BattleStatus.SETTLED,
        }


class Team(models.Model):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, related_name="teams")
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teams")
    pokemons = models.ManyToManyField(Pokemon, related_name="teams", through="PokemonTeam")


class PokemonTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="teams")
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="+")
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
        unique_together = [("team", "pokemon")]
