from django import template

from ..models import Team


register = template.Library()


@register.filter()
def get_team_id(battle, user):
    team_id = Team.objects.get(battle=battle, trainer=user).id
    return team_id
