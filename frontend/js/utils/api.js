import axios from 'axios';
import _ from 'lodash';

import Urls from './urls';

const baseUrl = window.location.host;

const getAllPokemon = () => {
  const url = `https://pokeapi.co/api/v2/pokemon/`;
  const response = axios.get(url).then((res) => {
    return res.data;
  });
  return response;
};

const getFromApi = (urlApi) => {
  const url = `http://${baseUrl}${urlApi}`;
  const response = axios.get(url).then((res) => {
    return res.data;
  });
  return response;
};

const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (const element of cookies) {
      const cookie = element.trim();
      if (cookie.slice(0, Math.max(0, name.length + 1)) === `${name}=`) {
        cookieValue = decodeURIComponent(cookie.slice(Math.max(0, name.length + 1)));
        break;
      }
    }
  }
  return cookieValue;
};

const postOnApi = (urlApi, battleData) => {
  const url = `http://${baseUrl}${urlApi}`;
  const token = getCookie('csrftoken');
  const response = axios
    .post(
      url,
      {
        creator: battleData.creator,
        opponent: battleData.opponent,
        /* eslint-disable-next-line babel/camelcase */
        opponent_email: battleData.opponent,
      },
      { headers: { 'X-CSRFToken': token } }
    )
    .then((response) => {
      return response;
    })
    .catch((error) => {
      /* eslint-disable-next-line no-console */
      console.log(error);
    });
  return response;
};

const putOnApi = (urlApi, data) => {
  const tokenCSRF = getCookie('csrftoken');

  if (tokenCSRF) {
    const urlBattle = `http://${baseUrl}${urlApi}`;

    const response = axios
      .put(urlBattle, data, { headers: { 'X-CSRFToken': tokenCSRF } })
      .then((response) => {
        return response;
      });
    return response;
  }
  return null;
};

const getCurrentUserData = async () => {
  const user = await getFromApi(Urls['current-user']());
  return user;
};

const getTeamData = async (id) => {
  const data = await getFromApi(Urls['battle-detail'](id));
  return data;
};

const getBattleListPage = async () => {
  const data = await getFromApi(Urls['battle-list']());
  return data;
};

const battleCreate = async (battle) => {
  const battleData = {
    creator: _.get(battle, 'creator', null),
    opponent: _.get(battle, 'opponent', null),
    /* eslint-disable-next-line babel/camelcase */
    opponent_email: _.get(battle, 'opponent', null),
  };
  const data = await postOnApi(Urls['create-battle'](), battleData);
  return data;
};

const getPokemonFromApi = (pokemon) => {
  const url = `https://pokeapi.co/api/v2/pokemon/${pokemon}`;
  const response = axios.get(url).then((res) => {
    const pokemonData = {
      pokemonId: _.get(res, 'data.id', null),
      name: _.get(res, 'data.name', null),
      imgUrl: _.get(res, 'data.sprites.front_default', null),
      attack: _.get(res, 'data.stats[1].base_stat', null),
      defense: _.get(res, 'data.stats[2].base_stat', null),
      hp: _.get(res, 'data.stats[0].base_stat', null),
    };
    return pokemonData;
  });
  return response;
};

const getPokemonsFromApi = async (pokemons) => {
  const pokemonsNames = Object.values(pokemons);
  const pokemon1 = await getPokemonFromApi(pokemonsNames[0]);
  const pokemon2 = await getPokemonFromApi(pokemonsNames[1]);
  const pokemon3 = await getPokemonFromApi(pokemonsNames[2]);

  return { pokemon1, pokemon2, pokemon3 };
};

const createTeam = async (team) => {
  let teamArray = team.pokemons;
  const validateObject = _.get(team, 'pokemons.pokemon3.name', null);
  if (validateObject) {
    teamArray = Object.values(team.pokemons);
  }
  const teamData = {
    /* eslint-disable-next-line babel/camelcase */
    pokemons_ids: [
      _.get(teamArray, '[0].pokemonId', null),
      _.get(teamArray, '[1].pokemonId', null),
      _.get(teamArray, '[2].pokemonId', null),
    ],
  };
  const data = await putOnApi(Urls.team_create(_.get(team, 'id', null)), teamData);
  return data;
};

export {
  getFromApi,
  getCurrentUserData,
  getTeamData,
  getBattleListPage,
  battleCreate,
  getPokemonFromApi,
  getPokemonsFromApi,
  createTeam,
  getAllPokemon,
};
