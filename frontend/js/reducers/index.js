import { combineReducers } from 'redux';

import { battleReducer } from './battleReducer';
import { userReducer } from './userReducer';

export const Reducers = combineReducers({
  battle: battleReducer,
  user: userReducer,
});
