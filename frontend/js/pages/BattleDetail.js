import { get, map } from 'lodash';
import React, { useState } from 'react';
import { useParams } from 'react-router-dom';

import { apiUrls, getFromApi } from 'utils/api';

function BattleDetail() {
  const { id } = useParams();
  const [battle, setBattle] = useState();
  const getTeamData = async () => {
    const data = await getFromApi(apiUrls.battleDetail(id));
    setBattle(data);
    return data;
  };
  getTeamData();
  if (!battle) {
    return `loading`;
  }
  return (
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
  );
}

export default BattleDetail;
