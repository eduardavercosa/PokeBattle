import {
  BATTLE_DETAIL_STARTED,
  BATTLE_DETAIL_SUCCESSED,
  BATTLE_DETAIL_FAILED,
  BATTLE_LIST,
} from '../constants';

const initialState = {
  entities: [],
  loading: false,
  error: null,
};

export const battleReducer = (state = initialState, action) => {
  switch (action.type) {
    case BATTLE_DETAIL_STARTED:
      return { ...state, loading: true };
    case BATTLE_DETAIL_SUCCESSED:
      return { ...state, loading: false, entities: action.payload };
    case BATTLE_DETAIL_FAILED:
      return { ...state, loading: false, err: action.error };
    case BATTLE_LIST:
      return { ...state, entities: action.payload };
    default:
      return state;
  }
};
