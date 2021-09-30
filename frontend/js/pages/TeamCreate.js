import { Formik, Field, Form } from 'formik';
import _ from 'lodash';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { useParams } from 'react-router-dom';

import { createTeamAction, getPokemonsFromApiAction } from '../actions/createTeam';
import { getCurrentUser } from '../actions/getUser';
import { getPokemonFromApi } from '../utils/api';

function TeamCreate(props) {
  const { user, pokemons } = props;
  const { id } = useParams();

  const validate = (value) => {
    let error = null;
    return getPokemonFromApi(value)
      .then(() => {
        return error;
      })
      .catch((response) => {
        if (!value) {
          error = 'You must choose your Pokemon.';
        } else if (response.response.status === 404) {
          error = 'Type a valid Pokemon.';
        }
        return error;
      });
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
            pokemon1: '',
            pokemon2: '',
            pokemon3: '',
          }}
          onSubmit={async (values) => {
            props.getPokemonsFromApiAction(values);
          }}
        >
          {({ errors }) => (
            <Form>
              <div>
                <p>Choose your pokemons!</p>
                <div>
                  <div>
                    <p>Pokemon 1:</p>
                    <Field name="pokemon1" type="text" validate={validate} />
                  </div>
                  <div>{errors.pokemon1 && <div>{errors.pokemon1}</div>}</div>
                </div>
                <div>
                  <div>
                    <p>Pokemon 2:</p>
                    <Field name="pokemon2" type="text" validate={validate} />
                  </div>
                  <div>{errors.pokemon2 && <div>{errors.pokemon2}</div>}</div>
                </div>
                <div>
                  <div>
                    <p>Pokemon 3:</p>
                    <Field name="pokemon3" type="text" validate={validate} />
                  </div>
                  <div>{errors.pokemon3 && <div>{errors.pokemon3}</div>}</div>
                </div>
                <button
                  type="submit"
                  onClick={() =>
                    props.createTeamAction({ pokemons, id, user }).then((r) => {
                      window.location.replace(`http://${window.location.host}/`);
                      return r;
                    })
                  }
                >
                  Next
                </button>
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
  user: _.get(store, 'user.user', null),
  team: _.get(store, 'team.team', null),
  pokemons: _.get(store, 'team.pokemons', null),
});

const mapDispatchToProps = (dispatch) => {
  return {
    getCurrentUser: () => dispatch(getCurrentUser()),
    getPokemonsFromApiAction: (pokemons) => dispatch(getPokemonsFromApiAction(pokemons)),
    createTeamAction: (team) => dispatch(createTeamAction(team)),
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(TeamCreate);
