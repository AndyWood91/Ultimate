import numpy as np
import scipy.stats as ss
import pickle
import re

# TODO: add timing


class SpiritMatrix(object):
    """Array of scores for each WFDF spirit category."""

    scores = [[0, "Poor"], [1, "Not Good"], [2, "Good"], [3, "Very Good"], [4, "Excellent"]]

    def __init__(self, rules, fouls, fair, positive, communication):
        """Score for each category."""
        self.rules = rules
        self.fouls = fouls
        self.fair = fair
        self.positive = positive
        self.communication = communication

    # def __str__(self):
    #     return "rules: {}\nfouls: {}\nfair: {}\npositive: {}\ncommunication: {}".format(
    #         self.rules, self.fouls, self.fair, self.positive, self.communication)
    #     # TODO: this will just print the array, not sure what analysis is appropriate for categorical variables


class ScoreMatrix(object):
    """Matrix of [score0, score1, points difference, and points played] and the level of analysis."""

    def __init__(self, scores, level):
        """scores is an arrays of game scores, level is the analysis group."""

        self.scores0 = scores[:, 0]
        self.scores1 = scores[:, 1]
        self.points_difference = self.scores0 - self.scores1  # if this throws a bug, use package for array maths
        self.point_played = self.scores0 - self.scores1
        self.level = level
        self.matrix = np.array([self.scores0,
                                self.scores1,
                                self.points_difference,
                                self.point_played])

        print(self.matrix)

    # def __str__(self):
    #     return self.level

    def run_analysis(self):
        """Returns array descriptive statistics (n, range, mode, median) and the first four moments."""
        list_arrays = [self.scores0, self.scores1, self.points_difference, self.point_played]
        names_array = ["Score0", "Score1", "Points Difference", "Points Played"]

        for a in range (0, len(names_array)):
            print("\n{}".format(names_array[a]).upper())
            print("Descriptive Statistics: n = {}, range = {} to {}, mode = {}, median = {}".format(
                len(list_arrays[a]),
                min(list_arrays[a]),
                max(list_arrays[a]),
                ss.mode(list_arrays[a]),
                np.median(list_arrays[a])
            ))
            print("Moments: mean = {0:.3g}, std. dev. = {0:.3g}, skew = {0:.3g}, kurtosis = {0:.3g}".format(
                np.mean(list_arrays[a]),
                np.std(list_arrays[a]),
                ss.skew(list_arrays[a], 0, False),
                ss.kurtosis(list_arrays[a], 0, False)
            ))


class Tournament(object):
    """Details and a list of divisions."""

    def __init__(self, tournament, url, date_range, location, points_cap, time_cap, divisions):
        self.tournament = tournament
        self.url = url
        self.date_range = date_range
        self.location = location
        self.points_cap = points_cap
        self.time_cap = time_cap
        self.divisions = divisions
        self.games = []
        # TODO: timeouts

    def extract_games(self):
        self.games = [[[game for game in team.games] for team in division.teams] for division in self.divisions]

        # print("Tournament.__init__() called")

    # def __str__(self):
    #     return self.tournament


class Division(Tournament):
    """Division restrictions, list of teams, list of games."""

    def __init__(self, **kwargs):
        self.gender = kwargs.pop("gender")
        self.age = kwargs.pop("age")
        self.teams = kwargs.pop("teams")
        self.games = []
        super(Division, self).__init__(**kwargs)

        # print("Division.__init__() called")

    # def __str__(self):
    #     return "{} {}".format(self.age, self.gender)

    def extract_games(self):
        self.games = [[game for game in team.games if game.score0_game > game.score1_game] for team in self.games]


class Group(object):
    """Group of teams."""

    def __init__(self, group):
        self.group = group

        # print("Group.__init__() called")

    # def __str__(self):
    #     return "{}".format(self.group)


class Team(Group):
    """Team information, list of players, list of games"""

    def __init__(self, **kwargs):
        self.group = kwargs.pop("group")
        self.team = kwargs.pop("team")
        self.coaches = kwargs.pop("coaches")
        self.captains = kwargs.pop("captains")
        self.players = kwargs.pop("players")
        self.games = []
        super(Team, self).__init__(**kwargs)

        # print("Team.__init__() called")

    # def __str__(self):
    #     return "{} {}\ncoaches: {}\ncaptains: {}".format(self.group, self.team, self.coaches, self.captains)

    def append_games(self, team_games):
        self.games = team_games


class Player(Team):

    def __init__(self, **kwargs):
        self.group = kwargs.pop("group")
        self.team = kwargs.pop("team")
        self.number = kwargs.pop("number")
        self.player = kwargs.pop("player")
        self.games = 0
        self.assists = 0
        self.goals = 0
        # self.blocks = 0

        super(Player, self).__init__(**kwargs)

        print("Player.__init__(group: {}, team: {}, number: {}, player: {}) called".format(
            self.group, self.team, self.number, self.player
        ))

    def append_statistics(self, statistics):
        self.games = statistics[0]
        self.assists = statistics[1]
        self.goals = statistics[2]
        # self.blocks = statistics[3]


        # def __str__(self):
        #     return "{#{} {}".format(self.number, self.player)


class Game(Division):
    """Game information, teams and scores"""

    def __init__(self, **kwargs):
        self.game = kwargs.pop("date")
        self.stage = kwargs.pop("stage")
        self.time = kwargs.pop("time")
        self.field = kwargs.pop("field")
        self.team0 = kwargs.pop("team0")
        self.team1 = kwargs.pop("team1")
        self.points = []
        self.spirit = []
        self.score0_game = 0
        self.score1_game = 0
        self.timeouts0 = 0
        self.timeouts1 = 0
        # TODO: I'm actually going to have data on timeouts.
        super().__init__(**kwargs)

        # print("Game.__init__() called")

    # def __str__(self):
    #     return "{} {} - {} {}".format(self.team0[0], self.team0[1], self.team1[0], self.team1[1])

    # __repr__ = __str__
    # TODO: learn what this does

    def append_points(self, points):
        """Append points, then return the final score from the last point."""

        self.points = points
        self.score0_game = self.points[-1].score0_point
        self.score1_game = self.points[-1].score1_point

    def append_spirit(self, spirit):
        self.spirit = spirit

    # def record_game(self):
    #     """Enter play by play recording."""


class Point(Game):
    """Sequence from pull to goal"""

    def __init__(self, **kwargs):
        """"""

        self.team0 = kwargs.pop("team0")
        self.team1 = kwargs.pop("team1")
        self.start = kwargs.pop("start")
        self.pull = kwargs.pop("pull")
        self.possessions = []
        self.scoring_team = ""
        self.score0_initial = kwargs.pop("score0")
        self.score1_initial = kwargs.pop("score1")
        self.finish = 0.00
        self.duration = 0.00
        self.score0_point = self.score0_initial
        self.score1_point = self.score1_initial
        super(Point, self).__init__(**kwargs)

        print("Point.__init__() called")

    # def __str__(self):
    #     return "start: {}, finish: {}, duration: {}".format(self.start, self.finish, self.duration)

    def append_possessions(self, possessions):
        self.possessions = possessions

        self.scoring_team = self.possessions[-1].team

        if self.scoring_team == self.team0:
            self.score0_point += 1
        elif self.scoring_team == self.team1[0]:
            self.score1_point += 1

    def append_finish(self, finish):
        self.finish = finish
        self.duration = self.finish - self.duration


class Pull(Point):
    """Puller, position."""

    def __init__(self, **kwargs):
        """Return puller and where the pull was fielded."""
        self.puller = kwargs.pop("puller")
        self.team = self.puller.team
        self.location = kwargs.pop("location")
        super(Point, self).__init__(**kwargs)

        # TODO: consider turning this into the same player/action/outcome as stalls

        # print("Pull.__init__() called")

    # def __str__(self):
    #     return "{}, {}".format(self.puller, self.location)


class Possession(Point):
    """Team possession."""

    def __init__(self, **kwargs):
        """Offensive stalls"""

        self.team = kwargs.pop("team")
        self.stalls = []
        super(Possession, self).__init__(**kwargs)

        print("Possession.__init__() called")

    def append_stalls(self, stalls):
        self.stalls = stalls

    # def __str__(self):
    #     return "{}, stalls: {}".format(self.team, [stall for stall in self.stalls])

    def team_possession(self):
        # print('print buildevent')
        # teamlist[0] is always starting on offence, teamlist[1] is always starting on defence
        # protect our input, make sure our data makes sense
        print("select player (use index): ")
        player = input(self.teamlist[self.offence])  # this will provide list of first team
        while player not in ['0', '1', '2', '3', '4', '5', '6']:
            player = input(str(self.teamlist[self.offence]))

        print("select action (first letter only): ")
        action = input("pass, stall, turf, outbounds, goal, brick ")
        while action not in ['p', 's', 't', 'o', 'g', 'b']:
            action = input("pass, stall, turf, outbounds, goal, brick ")

        if action in ['g', 't', 's', 'o', 'h']:
            # actions that cause who's on offence to change
            #print("offense switches")
            self.offence = 1 - self.offence  # pretty! #goals

        self.stalls.append([int(player), action])
        # print(self.sequence)
        return self.offence


class Stall(Possession):
    """Player possession."""

    def __init__(self, **kwargs):
        """Player, action, outcome."""

        self.team = kwargs.pop("team")
        # self.start = kwargs.pop("start")
        self.player = kwargs.pop("player")
        self.action = ""
        self.outcome = ""
        # self.finish = 0.00
        # self.duration = 0.00
        super(Stall, self).__init__(**kwargs)

        print("Stall.__init() called")

    # def __str__(self):
    #     return "{} - {}: {}".format(self.player, self.action, self.outcome)
    # this is maybe duplicate, same exists for game

    # def append_finish(self, finish):
    #     self.finish = finish
    #     self.duration = self.finish - self.start

    def append_sequence(self, action, outcome):
        """Return the specific action."""

        # stall_actions = ("throw", "stall", "timeout", "handover", "violation", "catch", "touch")
        # self.action = input("Select action: {}".format([a for a in stall_actions]))
        # TODO: data validation
        self.action = action
        self.outcome = outcome


def team_dictionary(team_string_csv):
    """Return a dictionary of player names and numbers."""

    return {re.search("\d+", a): re.search("[a-zA-Z][\w|\s]+", a) for a in team_string_csv.split(",")}


def newStatsLoop():
    gameName = input('Name of game: ')
    nameTeamA = input('enter teamA (starting offence) name: ')
    playersTeamA = input('enter player names comma separated for Team A: ')
    dictTeamA = team_dictionary(playersTeamA)

    nameTeamB = input('enter teamB (starting defence) name: ')
    playersTeamB = input('enter player names comma separated for Team B: ')
    dictTeamB = team_dictionary(playersTeamB)

    testgame = Game(dictTeamA, dictTeamB)  # initialise our game, setting initial variables

    while testgame.pointcap not in testgame.score and testgame.gameover != "y":
        # Team A is teamlist[0] is offence first
        print(dictTeamA)
        # print dict, show what keys are what
        thisLineA = input("who is on this offence line, comma separated !keys!")
        thisLineListA = [x.strip() for x in thisLineA.split(',')]
        thisLineDictA = {}
        for i in thisLineListA:
            thisLineDictA[int(i)] = dictTeamA.get(int(i))

        # Team B is teamlist[1] is defence first
        print(dictTeamB)
        # print dict, show what keys are what
        thisLineB = input("who is on this defence line, comma separated !keys!")
        thisLineListB = [x.strip() for x in thisLineB.split(',')]
        thisLineDictB = {}
        for i in thisLineListB:
            thisLineDictB[int(i)] = dictTeamB.get(int(i))

        bothLines = [thisLineDictA, thisLineDictB]
        # print(bothLines)
        # get list of keys, put in dict[keys] as argument to Point()
        # offence variable needs to be defined before here but it's not
        # where to put it - must be outside loops

        offence = 0  #teamA is bothLines[0], and is starting on offence
        thispoint = Point(0, bothLines, offence)  # start a point, passing the time and players on each line
        offence = thispoint.buildevent()
        print(thispoint.sequence)
        while thispoint.sequence[-1][1] != "g":
            offence = thispoint.buildevent()

        testgame.score[offence] += 1
        #print(thispoint.sequence[-1][1])

        # print(thispoint.sequence)
        thispoint.offence = offence
        testgame.gameover = input("was that goal the game winner? y/n ")
        # score++


        testgame.playbyplay.append(thispoint)  # attach our (now-finished) point to the playbyplay list

    gamefile = open((gameName + '.stats'), 'wb')

    pickle.dump(testgame, gamefile)
