import { battleCreate } from 'utils/api';

import { BATTLE_CREATE } from '../constants';

function createBattle(data) {
  return (dispatch) =>
    battleCreate(data).then((response) => {
      return dispatch({ type: BATTLE_CREATE, payload: response });
    });
}

export { createBattle };
