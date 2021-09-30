import { TEAM_CREATE, GET_POKEMONS_FROM_API } from '../constants';

export const teamReducer = (state = { pokemons: null, team: null }, action) => {
  switch (action.type) {
    case GET_POKEMONS_FROM_API:
      return { ...state, pokemons: action.payload };
    case TEAM_CREATE:
      if (action.payload.status !== 201) {
        return { ...state, team: null };
      }
      return { ...state, team: action.payload };
    default:
      return state;
  }
};
