import React from 'react';
import styled from 'styled-components';

const Title = styled.h1`
  font-size: 3em;
  color: white;
`;

const Wrapper = styled.section`
  padding: 4em;
  background: linear-gradient(to right, rgb(197, 230, 236), rgb(239, 187, 230));
`;

function BattleList() {
  return (
    <Wrapper>
      <Title>Battle List</Title>
    </Wrapper>
  );
}

export default BattleList;
