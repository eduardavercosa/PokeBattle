import { includes, isNil } from 'lodash';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { useParams, Link } from 'react-router-dom';
import styled from 'styled-components';

import TeamCard from 'components/TeamCard';

import { getBattle } from '../actions/getBattle';
import { getCurrentUser } from '../actions/getUser';
import { showTeams } from '../utils/battle-detail';
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

const BattleDetail = (props) => {
  const { id } = useParams();
  const { battles, loading, error } = props;
  const { user } = props.user;
  useEffect(() => {
    if (battles.length === 0 || battles.battle[id]) {
      props.getCurrentUser();
      props.getBattle(id);
    }
  }, []);
  if (loading) {
    return (
      <img alt="loading" src="https://giphy.com/gifs/loop-loading-loader-xTk9ZvMnbIiIew7IpW" />
    );
  }
  if (error) {
    return 'Ocurred an error';
  }
  if (!user) {
    return (
      <Wrapper>
        <Title>The user is not logged in.</Title>
      </Wrapper>
    );
  }
  if (battles.length === 0 && !isNil(user)) {
    return (
      <Wrapper>
        <Title>The battle you are looking for does not exist.</Title>
      </Wrapper>
    );
  }
  const { battle, pokemon, users } = battles;
  const teams = showTeams(battle[id], user);
  const { currentUserTeam } = teams;
  const { opponentUserTeam } = teams;
  const { winner } = battle[id];

  if (teams.length < 2) {
    return (
      <Wrapper>
        <Title>The teams were not created.</Title>
      </Wrapper>
    );
  }

  return (
    <Wrapper>
      {!includes([currentUserTeam.trainer, opponentUserTeam.trainer], user.id) ? (
        <Text>You do not have acess to this battle</Text>
      ) : (
        <div>
          <Title>Battle result!</Title>
          {battle[id].winner ? (
            <Text>The winner is {battle[id].winner ? users[winner].email : ''}</Text>
          ) : (
            ''
          )}
          <div>
            <div>
              <p>Your team:</p>
              {currentUserTeam.pokemons.length === 0 ? (
                <div>
                  <p>You have not chosen your pokemon yet.</p>
                  <Link to={Urls.team_create_v2(currentUserTeam.id)}>Edit your team</Link>
                </div>
              ) : (
                <TeamCard
                  pokemons={currentUserTeam.pokemons.map((pokemonId) => pokemon[pokemonId])}
                />
              )}
            </div>
            <div>
              <p>Your opponent team:</p>
              {battle[id].winner ? (
                <TeamCard
                  pokemons={opponentUserTeam.pokemons.map((pokemonId) => pokemon[pokemonId])}
                />
              ) : (
                <p>The battle is not over yet.</p>
              )}
            </div>
          </div>
          <Link to={Urls.battle_list_v2()}>Back</Link>
        </div>
      )}
    </Wrapper>
  );
};

const mapStateToProps = (state) => ({
  battles: state.battle.entities,
  loading: state.battle.loading,
  error: state.battle.error,
  user: state.user,
});

const mapDispatchToProps = (dispatch) => {
  return {
    getCurrentUser: () => dispatch(getCurrentUser()),
    getBattle: (battle) => dispatch(getBattle(battle)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetail);
