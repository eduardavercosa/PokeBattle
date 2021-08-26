import { get, map } from 'lodash';
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';

import { getFromApi } from 'utils/api';

import Urls from '../utils/urls';

const Title = styled.h1`
  font-size: 3em;
  color: white;
`;

const Text = styled.h1`
  font-size: 1.5em;
  color: white;
`;

const Wrapper = styled.section`
  padding: 4em;
  background: linear-gradient(to right, rgb(197, 230, 236), rgb(239, 187, 230));
`;

function BattleDetail() {
  const { id } = useParams();
  const [battle, setBattle] = useState();

  const getTeamData = async () => {
    const data = await getFromApi(Urls['battle-detail'](id));
    setBattle(data);
    return data;
  };

  useEffect(() => {
    getTeamData();
  }, []);
  if (!battle) {
    return (
      <Wrapper>
        <Title>The battle you are looking for does not exist.</Title>
      </Wrapper>
    );
  }
  if (!battle.winner || !battle.teams) {
    return (
      <Wrapper>
        <Title>Battle result!</Title>
        <div>
          <Text>The battle is not over yet!</Text>
          <p>{battle.creator.email} team:</p>
          <div>
            <a href={Urls['battle-list']()}>Back</a>
          </div>
        </div>
      </Wrapper>
    );
  }
  return (
    <Wrapper>
      <Title>Battle result!</Title>
      <div>
        <Text>The winner is {battle.winner.email}!</Text>
        <p>{battle.creator.email} team:</p>
        <div>
          <table>
            <tbody>
              <tr>
                <th>Pokemon</th>
                <th>name</th>
                <th>attack</th>
                <th>defense</th>
                <th>hp</th>
              </tr>

              {map(battle.teams[0].pokemons, (pokemon) => {
                return (
                  <tr key={pokemon.name}>
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
            </tbody>
          </table>
        </div>
        <p>{battle.opponent.email} team:</p>
        <div>
          <table>
            <tbody>
              <tr>
                <th>Pokemon</th>
                <th>name</th>
                <th>attack</th>
                <th>defense</th>
                <th>hp</th>
              </tr>

              {map(battle.teams[1].pokemons, (pokemon) => {
                return (
                  <tr key={pokemon.name}>
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
            </tbody>
          </table>
        </div>
      </div>
      <a href={Urls['battle-list']()}>Back</a>
    </Wrapper>
  );
}

export default BattleDetail;
