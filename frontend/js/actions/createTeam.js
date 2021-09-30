import { TEAM_CREATE, GET_POKEMONS_FROM_API } from '../constants';
import { createTeam, getPokemonsFromApi } from '../utils/api';

function getPokemonsFromApiAction(data) {
  return (dispatch) =>
    getPokemonsFromApi(data).then((response) => {
      return dispatch({ type: GET_POKEMONS_FROM_API, payload: response });
    });
}

function createTeamAction(data) {
  return (dispatch) =>
    createTeam(data).then((response) => {
      return dispatch({ type: TEAM_CREATE, payload: response });
    });
}

export { createTeamAction, getPokemonsFromApiAction };
