import React from 'react';

function PokemonCard({ pokemon }) {
  return (
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
          <tr>
            <th>
              <img alt="pokemon" className="img_pokemon_card" src={pokemon.img_url} />
            </th>
            <th> {pokemon.name}</th>
            <th> {pokemon.attack}</th>
            <th> {pokemon.defense}</th>
            <th> {pokemon.hp}</th>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
export default PokemonCard;
