const showTeams = (battle, user) => {
  let currentUserTeam = null;
  let opponentUserTeam = null;
  currentUserTeam =
    battle.teams[0].trainer.email === user.email ? battle.teams[0] : battle.teams[1];
  opponentUserTeam = currentUserTeam === battle.teams[0] ? battle.teams[1] : battle.teams[0];

  return {
    currentUserTeam,
    opponentUserTeam,
  };
};

export { showTeams };
