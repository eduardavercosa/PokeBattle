import { map } from 'lodash';
import React, { useState } from 'react';
import styled from 'styled-components';

import { apiUrls, getFromApi } from 'utils/api';

const Title = styled.h1`
  font-size: 1.5em;
  text-align: center;
  color: white;
`;

const Wrapper = styled.section`
  padding: 4em;
  background: linear-gradient(to right, rgb(197, 230, 236), rgb(239, 187, 230));
  text-align: center;
  align-items: center;
`;

const Container = styled.section`
  color: white;
  text-align: center;
`;

function BattleList() {
  const [battle, setBattle] = useState();
  const currentUrl = window.location.host;
  const url = `http://${currentUrl}`;

  const getBattleList = async () => {
    const data = await getFromApi(apiUrls.battleList);
    setBattle(data);
    return data;
  };
  getBattleList();
  return (
    <Wrapper>
      <Title>Welcome to Poke Battle!</Title>
      <Title>Choose your pokemons and fight!</Title>
      <Container>
        <th>Ongoing Battles</th>
        <th>Battles I created</th>
        {map(battle, (bt) => {
          return <th> Battle {bt.id}</th>;
        })}
        <th>Battles I was invited</th>
        {map(battle, (bt) => {
          return <th> Battle {bt.id}</th>;
        })}
      </Container>
      <Container>
        <th>Settled Battles</th>
        <th>Battles I created</th>
        {map(battle, (bt) => {
          return <th> Battle {bt.id}</th>;
        })}
        <th>Battles I was invited</th>
        {map(battle, (bt) => {
          return <th> Battle {bt.id}</th>;
        })}
      </Container>
      <a href={url}>Back</a>
    </Wrapper>
  );
}

export default BattleList;
