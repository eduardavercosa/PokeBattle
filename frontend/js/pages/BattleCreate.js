import { Formik, Field, Form } from 'formik';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';

import { createBattle } from '../actions/createBattle';
import { getCurrentUser } from '../actions/getUser';

function BattleCreate(props) {
  const { user } = props;

  const validate = (data) => {
    let error = null;
    if (!data) {
      error = 'This field is required.';
    } else if (data === user.email) {
      error = 'ERROR: You cannot challenge yourself.';
    } else if (!/^[\w%+.-]+@[\d.a-z-]+\.[a-z]{2,4}$/i.test(data)) {
      error = 'Enter a valid email address.';
    }
    return error;
  };
  useEffect(() => {
    if (!user) {
      props.getCurrentUser();
    }
  }, []);

  if (user) {
    return (
      <div>
        <Formik
          initialValues={{
            creator: user.email,
            creator_id: user.id,
            opponent: '',
            opponent_id: 10,
          }}
          onSubmit={(values) => {
            return props.createBattle(values);
          }}
        >
          {({ errors }) => (
            <Form>
              <div>
                <p>Opponent: </p>
                <Field
                  name="opponent"
                  placeholder="example@email.com"
                  type="email"
                  validate={validate}
                />
                {errors.opponent}
                <button type="submit">Next</button>
              </div>
            </Form>
          )}
        </Formik>
      </div>
    );
  }
  return 'loading';
}

const mapStateToProps = (store) => ({
  user: store.user.user,
  battle: store.battle.battle,
  errorMessage: store.battle.errorMessage,
});

const mapDispatchToProps = (dispatch) => {
  return {
    getCurrentUser: () => dispatch(getCurrentUser()),
    createBattle: (form) => dispatch(createBattle(form)),
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(BattleCreate);
