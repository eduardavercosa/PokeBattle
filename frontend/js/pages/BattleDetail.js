import { get, map } from 'lodash';
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import { getFromApi } from 'utils/api';

import Urls from '../utils/urls';

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
      <div className="body">
        <div className="teste">
          <h1>The battle you are looking for does not exist.</h1>
        </div>
      </div>
    );
  }
  if (!battle.winner || !battle.teams) {
    return (
      <div className="container2">
        <h1>Battle result!</h1>
        <div>
          <h1>The battle is not over yet!</h1>
          <p>{battle.creator.email} team:</p>
          <div>
            <a href={Urls['battle-list']()}>Back</a>
          </div>
        </div>
      </div>
    );
  }
  return (
    <div className="body">
      <div className="container1" id="home">
        <h1>Welcome to Poke Battle!</h1>
        <h2>Choose your pokemons and fight!</h2>
        <div className="container2">
          <th>
            <img
              alt="pokemon_img"
              height="200px"
              src="https://static.tvtropes.org/pmwiki/pub/images/pokemon_350_210.png"
              width="400px"
            />
          </th>
          <div className="teste">
            <h1>Result</h1>
            <div>
              <h3>{battle.winner.email} won!</h3>
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
            <a className="button_next" href={Urls['battle-list']()}>
              Back
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default BattleDetail;
