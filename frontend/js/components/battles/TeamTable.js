import { get, map } from 'lodash';
import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';

const StyledTh = styled.th`
  padding: 5px;
`;

const TeamTable = ({ battleTrainer, battleTeam }) => {
  return (
    <div>
      <p>{battleTrainer.email} team:</p>
      <div>
        <table>
          <tbody>
            <tr>
              <StyledTh>Pokemon</StyledTh>
              <StyledTh>name</StyledTh>
              <StyledTh>attack</StyledTh>
              <StyledTh>defense</StyledTh>
              <StyledTh>hp</StyledTh>
            </tr>

            {map(battleTeam.pokemons, (pokemon) => {
              return (
                <tr key={pokemon.name}>
                  <StyledTh>
                    <img alt="pokemon img" height="90px" src={get(pokemon, 'img_url')} />
                  </StyledTh>
                  <StyledTh> {pokemon.name}</StyledTh>
                  <StyledTh> {pokemon.attack}</StyledTh>
                  <StyledTh> {pokemon.defense}</StyledTh>
                  <StyledTh> {pokemon.hp}</StyledTh>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

TeamTable.propTypes = {
  battleTrainer: PropTypes.object,
  battleTeam: PropTypes.object,
};

export default TeamTable;
