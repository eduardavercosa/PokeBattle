import { get, map } from 'lodash';
import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
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

function BattleDetail() {
  const { id } = useParams();
  const [battle, setBattle] = useState();
  const currentUrl = window.location.host;
  const url = `http://${currentUrl}/react/battles/list`;

  const getTeamData = async () => {
    const data = await getFromApi(apiUrls.battleDetail(id));
    setBattle(data);
    return data;
  };
  getTeamData();
  if (!battle) {
    return `The battle you're looking for doesn't exist`;
  }
  return (
    <Wrapper>
      <Title>Welcome to Poke Battle!</Title>
      <Title>Choose your pokemons and fight!</Title>
      <div>
        <p>{battle.winner.email} won!</p>
        <p>{battle.creator.email} team:</p>
        <div>
          <table>
            <tr>
              <th>Pokemon</th>
              <th>name</th>
              <th>attack</th>
              <th>defense</th>
              <th>hp</th>
            </tr>

            {map(battle.teams[0].pokemons, (pokemon) => {
              return (
                <tr>
                  <th>
                    <img alt="pokemon img" height="90px" src={get(pokemon, 'img_url')} />
                  </th>
                  <th> {pokemon.name}</th>
                  <th> {pokemon.attack}</th>
                  <th> {pokemon.defense}</th>
                  <th> {pokemon.hp}</th>
                </tr>
              );
            })}
          </table>
        </div>
        <p>{battle.opponent.email} team:</p>
        <div>
          <table>
            <tr>
              <th>Pokemon</th>
              <th>name</th>
              <th>attack</th>
              <th>defense</th>
              <th>hp</th>
            </tr>

            {map(battle.teams[1].pokemons, (pokemon) => {
              return (
                <tr>
                  <th>
                    <img alt="pokemon img" height="90px" src={get(pokemon, 'img_url')} />
                  </th>
                  <th> {pokemon.name}</th>
                  <th> {pokemon.attack}</th>
                  <th> {pokemon.defense}</th>
                  <th> {pokemon.hp}</th>
                </tr>
              );
            })}
          </table>
        </div>
      </div>
      <a href={url}>Back</a>
    </Wrapper>
  );
}

export default BattleDetail;
