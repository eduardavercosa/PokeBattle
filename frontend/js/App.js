import React from 'react';
import { hot } from 'react-hot-loader/root';

import BattleDetail from './pages/BattleDetail';
import SentryBoundary from './utils/SentryBoundary';

const App = () => (
  <SentryBoundary>
    <BattleDetail />
  </SentryBoundary>
);

export default hot(App);
