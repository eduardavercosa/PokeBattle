import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import { getBattleList } from '../actions/getBattleList';
import { getCurrentUser } from '../actions/getUser';
import Urls from '../utils/urls';

function BattleList(props) {
  const { battles, user } = props;

  useEffect(() => {
    props.getCurrentUser();
    props.getBattleList();
  }, []);

  if (!battles) {
    return (
      <div className="body">
        <Link
          to={{
            pathname: Urls.home(),
          }}
        >
          Back
        </Link>
        {!user ? <h1>You need to be logged</h1> : <h1>There are no battles in the database.</h1>}
      </div>
    );
  }
  return (
    <div className="body">
      <Link
        to={{
          pathname: Urls.home(),
        }}
      >
        Back
      </Link>
      {!user ? <h1>You need to be logged</h1> : ''}
      <div>
        <h1>Ongoing Battles</h1>
        {Object.values(battles).map((battles) =>
          !battles.winner ? (
            <li key={battles.id}>
              <Link
                to={{
                  pathname: Urls.battle_detail_v2(battles.id),
                }}
              >
                Battle ID {battles.id}
              </Link>
            </li>
          ) : null
        )}
      </div>

      <div>
        <h1>Settled battles</h1>
        {Object.values(battles).map((battles) =>
          battles.winner ? (
            <li key={battles.id}>
              <Link
                to={{
                  pathname: Urls.battle_detail_v2(battles.id),
                }}
              >
                Battle ID {battles.id}
              </Link>
            </li>
          ) : null
        )}
      </div>
    </div>
  );
}

const mapStateToProps = (store) => ({
  battles: store.battle.battles,
  user: store.user,
});

const mapDispatchToProps = (dispatch) => {
  return {
    getCurrentUser: () => dispatch(getCurrentUser()),
    getBattleList: () => dispatch(getBattleList()),
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(BattleList);
