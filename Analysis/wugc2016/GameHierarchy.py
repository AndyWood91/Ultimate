# TODO: writing this as data entry. Will need to be rewritten 

class Season(object):
    """Tournament season."""

    def __init__(self, **kwargs):
        """"""

        self.season = kwargs.get("season")
        self.season_start = kwargs.get("season_start")
        self.season_finish = kwargs.get("season_finish")
        # self.season_duration = self.finish - self.start
        self.age = kwargs.get("age")
        self.gender = kwargs.get("gender")
        self.tournaments = kwargs.get("tournaments")

        print("\nSeason.__init__() called.")

    def __str__(self):
        return self.season


class Tournament(Season):
    """Tournament."""

    def __init__(self, **kwargs):
        """"""

        self.season = kwargs.get("season")
        self.tournament = kwargs.get("tournament")
        # self.url = kwargs.get("url")
        self.tournament_start = kwargs.get("tournament_start")
        self.tournament_finish = kwargs.get("tournament_finish")
        # self.tournament_duration = self.tournament_finish - self.tournament_start
        self.location = kwargs.get("location")
        self.points_cap = kwargs.get("points_cap")
        self.time_cap = kwargs.get("time_cap")
        self.divisions = kwargs.get("divisions")
        self.games = []

        super(Tournament, self).__init__(**kwargs)

        print("\nTournament.__init__() called.")

    def extract_games(self):
        """Loop through each team in each division and extract the games."""
        self.games = [
            [
                [
                    game for game in team.games if game.score0 > game.score1
                ] for team in division.teams
            ] for division in self.divisions
        ]
        [print(game) for game in self.games]


    def __str__(self):
        return "{}, {}".format(self.season, self.tournament)


class Division(Tournament):
    """Division."""

    def __init__(self, **kwargs):
        """"""

        self.division = kwargs.get("division")
        self.tournament = kwargs.get("tournament")
        self.season = kwargs.get("season")
        self.age = kwargs.get("age")
        self.gender = kwargs.get("gender")
        self.teams = kwargs.get("teams")
        self.games = []

        super(Division, self).__init__(**kwargs)

        print("\nDivision.__init_() called.")

    def __str__(self):
        return "{}: {}".format(self.tournament, self.division)

    def extract_games(self):
        """Loop through each team in the division and extract the games."""

        self.games = [
            [
                game for game in team.games if game.score0 > game.score1
            ] for team in self.teams
        ]