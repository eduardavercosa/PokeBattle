import { normalize } from 'normalizr';

import { getBattleListPage } from 'utils/api';

import { BATTLE_LIST } from '../constants';

import * as schema from './schema';

function getBattleList() {
  return (dispatch) =>
    getBattleListPage().then((battlesData) => {
      const normalizedBattleList = normalize(battlesData, schema.battleList);
      const { battle } = normalizedBattleList.entities;
      return dispatch({ type: BATTLE_LIST, payload: battle });
    });
}

export { getBattleList };
