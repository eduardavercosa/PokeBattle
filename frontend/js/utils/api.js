import axios from 'axios';
import _ from 'lodash';

import Urls from './urls';

const baseUrl = window.location.host;

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
        opponent_id: battleData.opponent_id,
        creator_id: battleData.creator_id,
      },
      { headers: { 'X-CSRFToken': token } }
    )
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
  return response;
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
    opponent_id: _.get(battle, 'opponent_id', null),
    creator_id: _.get(battle, 'creator_id', null),
  };
  const data = await postOnApi(Urls['create-battle'](), battleData);
  return data;
};

export { getFromApi, getCurrentUserData, getTeamData, getBattleListPage, battleCreate };
