from celery.utils.log import get_task_logger

from battling.models import Battle
from duda import celery_app
from services.battles import set_battle_winner
from services.email import send_battle_result


logger = get_task_logger(__name__)


@celery_app.task
def run_battle_and_send_result_email(battle_id):
    logger.info("About to solve Battle %d", battle_id)
    battle = Battle.objects.get(id=battle_id)
    set_battle_winner(battle)
    send_battle_result(battle)
    logger.info("Solved Battle %d", battle_id)
