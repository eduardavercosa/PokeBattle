import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import { getFromApi } from 'utils/api';

import MessageBanner from '../components/battles/MessageBanner';
import TeamTable from '../components/battles/TeamTable';
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
      <MessageBanner
        content={
          <div className="body">
            <div className="teste">
              <h1>The battle you are looking for does not exist.</h1>
            </div>
          </div>
        }
      />
    );
  }
  if (!battle.winner || !battle.teams) {
    return (
      <MessageBanner
        content={
          <div>
            <h1>Battle result!</h1>
            <div>
              <h1>The battle is not over yet!</h1>
              <p>{battle.creator.email} team:</p>
              <div>
                <a href={Urls['battle-list']()}>Back</a>
              </div>
            </div>
          </div>
        }
      />
    );
  }
  return (
    <div className="body">
      <div className="container1" id="home">
        <h1>Welcome to Poke Battle!</h1>
        <h2>Choose your pokemons and fight!</h2>
        <div className="container2">
          <img
            alt="pokemon_img"
            height="200px"
            src="https://static.tvtropes.org/pmwiki/pub/images/pokemon_350_210.png"
            width="400px"
          />

          <div className="teste">
            <h1>Result</h1>
            <div>
              <h3>{battle.winner.email} won!</h3>
              <TeamTable battleTeam={battle.teams[0]} battleTrainer={battle.creator} />
              <TeamTable battleTeam={battle.teams[1]} battleTrainer={battle.opponent} />
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
