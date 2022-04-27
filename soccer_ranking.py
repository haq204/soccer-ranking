from collections import namedtuple
import sys
from typing import IO, List

import click

Standing = namedtuple('Standing', ["team", "points", "gd"])

class Bracket:
    def __init__(self):
        self._points = {}
        self._gd = {}

    def update(self, team: str, points: int, gd: int) -> None:
        """Add points and goal differentials for a team in the provided bracket"""
        if self._points.get(team) is not None:
            self._points[team] += points
            self._gd[team] += gd
        else:
            self._points[team] = points
            self._gd[team] = gd

    def get_sorted_standings(self) -> List[Standing]:
        """Return the team rankings for the bracket"""
        standings = []
        for team, points in self._points.items():
            gd = self._gd[team]
            standing = Standing(team, points, gd)
            standings.append(standing)

        # Sort the bracket first by point value, goal differential, then by team alphabetical order
        # Here we'll do a little trick. We want sort by points and goal differential from biggest 
        # to smallest but in the case of a tie, sort in alphabetical order. Normally we could use 
        # reverse=True but sorted() allows sorting in only one direction. So we will supply a 
        # comparator in which we negate the points value and sort on that from smallest to larget 
        # which is effectiely sorting from largest to smallest once we cancel the negation. 
        # This allows us to sort the way we want it without sorting twice.
        standings = sorted(standings, key=lambda s: (-s.points, -s.gd, s.team))
        return standings

def print_standings(standings: List[Standing]) -> str:
    """Print the team placements given a list of Standings.
    
    Teams are ranked according to standard competition (1224) ranking 
    https://en.wikipedia.org/wiki/Ranking#Standard_competition_ranking_(%221224%22_ranking)
    """
    output = ""
    prev_team_points = None
    prev_team_gd = None
    rank = None
    for i, team in enumerate(standings):
        pts_str = "pt" if team.points == 1 else "pts"
        if team.points != prev_team_points or team.gd != prev_team_gd:
            rank = i + 1 # since index starts at 0
        output = output + f"{rank}. {team.team}, {team.points} {pts_str}, gd: {team.gd}\n"
        prev_team_points = team.points
        prev_team_gd = team.gd
    return output

def parse_line(bracket: Bracket, line: str) -> None:
    """Parse a result line from the input and update bracket, which keeps tracks 
    of total standings
    """
    # Doesn't really mention which team is home or away from the input so I'm just going to
    # define that the first team is the Home team, and the second is the Away team
    home, away = line.split(",")
    home_arr = home.strip().split()
    away_arr = away.strip().split()
    
    home_score = int(home_arr.pop())
    home_team = " ".join(home_arr)
    away_score = int(away_arr.pop())
    away_team = " ".join(away_arr)
    home_gd = home_score - away_score
    away_gd = away_score - home_score

    if home_score > away_score:
        bracket.update(home_team, 3, home_gd)
        bracket.update(away_team, 0, away_gd)
    elif away_score > home_score:
        bracket.update(away_team, 3, away_gd)
        bracket.update(home_team, 0, home_gd)
    else:
        bracket.update(home_team, 1, home_gd)
        bracket.update(away_team, 1, away_gd)


@click.command()
@click.option("-f", "--input-file", help="input file", type=click.File("r"), default=sys.stdin)
def main(input_file: IO) -> None:
    bracket = Bracket()
    for l in input_file:
        parse_line(bracket, l)
    
    standings = bracket.get_sorted_standings()
    # Write the string directly to stdout since it already includes newlines.
    # Note that teams in standings are already sorted in alphabetical order in the event of a tie
    sys.stdout.write(
        print_standings(standings)
    )

if __name__ == "__main__":
    main()

