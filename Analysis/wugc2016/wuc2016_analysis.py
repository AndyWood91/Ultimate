import sys
from GameHierarchy import Division, Season, Team, Tournament


def main():
    """Analysis."""

    # none_open_2016 = Season(season="None Open 2016", start="January 1, 2016", finish="May 1, 2016", age="None",
    #                         gender="Open", tournaments=["Gold Cup", "SMO", "Regionals", "BCI", "Nationals"])
    # print(none_open_2016)
    #
    # wuc_2016 = Tournament(season="None Open 2016", tournament="World Ultimate Championships 2016",
    #                       dates="June 18-25, 2016", location="London, England", points_cap=15, time_cap=100)
    # print(wuc_2016)

    none_open_wuc_2016 = Division(season="None Open 2016", tournament="World Ultimate Championships 2016",
                                  dates="June 18-25, 2016", location="London, England", points_cap=15, time_cap=100,
                                  division="None Open", age="None", gender="Open", teams=[], games=[])
    print(none_open_wuc_2016)

    none_open_wuc_AUS_men_2016 = Team(season="None Open 2016", tournament="World Ultimate Championships 2016",
                                      dates="June 18-25, 2016", location="London, England", points_cap=15, time_cap=100,
                                      division="None Open", age="None", gender="Open", teams=[], games=[], group="AUS",
                                      team="Men", captains=[], coaches=[], players=[])
    print(none_open_wuc_AUS_men_2016)

if __name__ == "__main__":
    sys.exit(main())
