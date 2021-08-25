import React from 'react';

import PokemonCard from 'components/PokemonCard';

function TeamCard({ pokemons }) {
  return (
    <div className="content_card">
      <PokemonCard pokemon={pokemons[0]} />
      <PokemonCard pokemon={pokemons[1]} />
      <PokemonCard pokemon={pokemons[2]} />
    </div>
  );
}
export default TeamCard;
