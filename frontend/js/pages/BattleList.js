import React, { useEffect } from 'react';
import { connect } from 'react-redux';

import { getBattleList } from '../actions/getBattleList';
import { getCurrentUser } from '../actions/getUser';
import Urls from '../utils/urls';

function BattleList(props) {
  const { user } = props.user;
  const { battles } = props.battles;

  useEffect(() => {
    props.getCurrentUser();
    props.getBattleList();
  }, []);

  if (!battles) {
    return (
      <div className="body">
        <a className="button_next" href={Urls.home()}>
          Back
        </a>
        {!user ? <h1>You need to be logged</h1> : <h1>There are no battle in the database.</h1>}
      </div>
    );
  }
  return (
    <div className="body">
      <a className="button_next" href={Urls.home()}>
        Back
      </a>
      {!user ? <h1>You need to be logged</h1> : ''}
      <div>
        <h1>Ongoing Battles</h1>
        {battles.map((battle) =>
          !battle.winner ? (
            <li key={battle.id}>
              <a href={Urls.battle_detail_v2(battle.id)}>Battle ID {battle.id}</a>
            </li>
          ) : null
        )}
      </div>

      <div>
        <h1>Settled battles</h1>
        {battles.map((battle) =>
          battle.winner ? (
            <li key={battle.id}>
              <a className="battle_settled" href={Urls.battle_detail_v2(battle.id)}>
                Battle ID {battle.id}
              </a>
            </li>
          ) : null
        )}
      </div>
    </div>
  );
}

const mapStateToProps = (store) => ({
  battles: store.battle,
  user: store.currentUser,
});

const mapDispatchToProps = (dispatch) => {
  return {
    getCurrentUser: () => dispatch(getCurrentUser()),
    getBattleList: () => dispatch(getBattleList()),
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(BattleList);
