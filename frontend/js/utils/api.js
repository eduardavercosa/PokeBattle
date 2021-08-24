import axios from 'axios';

const baseUrl = window.location.host;

const getFromApi = (apiUrls) => {
  const url = `http://${baseUrl}/${apiUrls}`;
  const response = axios.get(url).then((res) => {
    return res.data;
  });
  return response;
};

export { getFromApi };
