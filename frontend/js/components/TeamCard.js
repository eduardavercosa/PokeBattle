import React from 'react';

import PokemonCard from 'components/PokemonCard';

function TeamCard({ pokemons }) {
  return (
    <div>
      {pokemons.map((pokemon) => {
        return <PokemonCard key={pokemon.name} pokemon={pokemon} />;
      })}
    </div>
  );
}
export default TeamCard;
