import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  background-color: #fcf7de;
  padding-bottom: 20px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  box-shadow: 1px 7px 20px -6px #18092b;
`;

const MessageBanner = ({ content }) => <Container>{content}</Container>;

MessageBanner.propTypes = {
  content: PropTypes.any,
};

export default MessageBanner;
