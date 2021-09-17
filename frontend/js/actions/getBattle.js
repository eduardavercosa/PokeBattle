import { normalize } from 'normalizr';

import { getTeamData } from 'utils/api';

import { BATTLE_DETAIL_STARTED, BATTLE_DETAIL_SUCCESSED, BATTLE_DETAIL_FAILED } from '../constants';

import * as schema from './schema';

const getBattleDetailsStarted = () => ({
  type: BATTLE_DETAIL_STARTED,
});
const getBattleDetailsSuccess = (repoDetails) => ({
  type: BATTLE_DETAIL_SUCCESSED,
  payload: repoDetails,
});
const getBattleDetailsFailed = (error) => ({
  type: BATTLE_DETAIL_FAILED,
  error,
});

const getBattle = (battleId) => async (dispatch) => {
  dispatch(getBattleDetailsStarted());
  try {
    const battleDetails = await getTeamData(battleId);
    const normalizedBattle = normalize(battleDetails, schema.battleSchema);
    const battle = normalizedBattle.entities.battle[normalizedBattle.result];
    dispatch(getBattleDetailsSuccess(battle));
  } catch (err) {
    dispatch(getBattleDetailsFailed(err.toString()));
  }
};

export { getBattle };
