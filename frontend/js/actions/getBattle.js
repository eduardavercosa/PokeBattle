import { getTeamData } from 'utils/api';

import { BATTLE_DETAIL } from '../constants';

function getBattle(battle) {
  return (dispatch) =>
    getTeamData(battle).then((battleData) => {
      return dispatch({ type: BATTLE_DETAIL, payload: battleData });
    });
}

export { getBattle };
