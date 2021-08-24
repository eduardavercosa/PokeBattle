import axios from 'axios';

import Urls from './urls';

const baseUrl = window.location.host;

const urlApi = Urls['battle-detail'](':id');

const getFromApi = () => {
  const url = `http://${baseUrl}/${urlApi}`;
  const response = axios.get(url).then((res) => {
    return res.data;
  });
  return response;
};

export { getFromApi };
