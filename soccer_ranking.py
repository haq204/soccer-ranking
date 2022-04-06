import sys
from typing import IO, List, Tuple

import click

class Bracket:
    def __init__(self):
        self._bracket = {}

    def update(self, team: str, points: int) -> None:
        """Add points for a team in the provided bracket"""
        if self._bracket.get(team):
            self._bracket[team] += points
        else:
            self._bracket[team] = points

    def get_rankings(self) -> List[Tuple[str, int]]:
        """Return the team rankings for the bracket"""
        standings = [(team, points) for team, points in self._bracket.items()]
        # Sort the bracket first by point value then by team alphabetical order
        # Here we'll do a little trick. We want sort by points from biggest to smallest but in
        # the case of a tie, sort in alphabetical order. Normally we could use reverse=True but
        # sorted() allows sorting in only one direction. So we will supply a comparator in which
        # we negate the points value and sort on that from smallest to larget which is effectiely
        # sorting from largest to smallest once we cancel the negation. This allows us to sort
        # the way we want it without sorting twice.
        standings = sorted(standings, key=lambda s: (-s[1], s[0]))
        return standings


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

    if home_score > away_score:
        bracket.update(home_team, 3)
        bracket.update(away_team, 0)
    elif away_score > home_score:
        bracket.update(away_team, 3)
        bracket.update(home_team, 0)
    else:
        bracket.update(home_team, 1)
        bracket.update(away_team, 1)


@click.command()
@click.option("-f", "--input-file", help="input file", type=click.File("r"), default=sys.stdin)
def main(input_file: IO) -> None:
    bracket = Bracket()
    for l in input_file:
        parse_line(bracket, l)
    
    rankings = bracket.get_rankings()
    output = ""
    for i, r in enumerate(rankings):
        rank = i + 1
        pts = "pt" if r[1] == 1 else "pts" 
        output  = output + f"{rank}. {r[0]}, {r[1]} {pts}\n"
    click.echo(output)

if __name__ == "__main__":
    main()

