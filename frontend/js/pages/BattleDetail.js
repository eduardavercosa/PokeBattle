import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';

import TeamCard from 'components/TeamCard';
import { getTeamUrl, getBattleListPage } from 'utils/api';

import { getBattle } from '../actions/getBattle';
import { getCurrentUser } from '../actions/getUser';
import { showTeams } from '../utils/battle-detail';

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

function BattleDetail(props) {
  const { id } = useParams();
  useEffect(() => {
    props.getCurrentUser();
    props.getBattle(id);
  }, []);
  const { battle } = props.battle;
  const { user } = props.user;
  if (!battle) {
    return (
      <Wrapper>
        <Title>The battle you are looking for does not exist.</Title>
      </Wrapper>
    );
  }

  const teams = showTeams(battle, user);
  const currentUserTeam = teams[0];
  const otherUserTeam = teams[1];

  return (
    <Wrapper>
      {user.email !== battle.creator.email && user !== battle.opponent.email ? (
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
                  <a href={getTeamUrl(currentUserTeam.id)} role="button">
                    Edit your team
                  </a>
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
          <a href={getTeamUrl(getBattleListPage)} role="button">
            Back
          </a>
        </div>
      )}
    </Wrapper>
  );
}

const mapStateToProps = (store) => ({
  battle: store.battleState,
  user: store.userState,
});

const mapDispatchToProps = (dispatch) => {
  return {
    getCurrentUser: () => dispatch(getCurrentUser()),
    getBattle: (battle) => dispatch(getBattle(battle)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetail);
