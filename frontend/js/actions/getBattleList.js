import { getBattleListPage } from 'utils/api';

import { BATTLE_LIST } from '../constants';

function getBattleList() {
  return (dispatch) =>
    getBattleListPage().then((battlesData) => {
      return dispatch({ type: BATTLE_LIST, payload: battlesData });
    });
}

export { getBattleList };
