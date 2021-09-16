import { includes, isNil } from 'lodash';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { useParams, Link } from 'react-router-dom';
import styled from 'styled-components';

import TeamCard from 'components/TeamCard';

import { fetchBattle } from '../actions/setBattle';
import { setCurrentUser } from '../actions/setUser';
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
    props.setCurrentUser();
    props.fetchBattle(id);
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
  const battle = battles[0];
  const teams = showTeams(battle, user);
  const currentUserTeam = teams[0];
  const otherUserTeam = teams[1];

  return (
    <Wrapper>
      {!includes([battle.creator.email, battle.opponent.email], user.email) ? (
        <Text>You do not have acess to this battle</Text>
      ) : (
        <div>
          <Title>Battle result!</Title>
          {battle.winner ? (
            <Text>The winner is {battle.winner ? battle.winner.email : ''}</Text>
          ) : (
            ''
          )}
          <div>
            <div>
              <p>Your team:</p>
              {currentUserTeam.pokemons.length === 0 ? (
                <div>
                  <p>You have not chosen your pokemon yet.</p>
                  <Link to={Urls.create_team(currentUserTeam.id)}>Edit your team</Link>
                </div>
              ) : (
                <TeamCard pokemons={currentUserTeam.pokemons} />
              )}
            </div>
            <div>
              <p>Your opponent team:</p>
              {battle.winner ? (
                <TeamCard pokemons={otherUserTeam.pokemons} />
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
  battles: state.battleState.battles,
  battleState: state.battleState,
  loading: state.battleState.loading,
  error: state.battleState.error,
  user: state.userState,
});

const mapDispatchToProps = (dispatch) => {
  return {
    setCurrentUser: () => dispatch(setCurrentUser()),
    fetchBattle: (battle) => dispatch(fetchBattle(battle)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetail);
