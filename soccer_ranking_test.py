import pytest

from soccer_ranking import Bracket, parse_line

def test_parse_line():
    bracket = Bracket()
    first_game = "Tarantulas 1, FC Awesome 0"
    parse_line(bracket, first_game)
    assert bracket._bracket == { "Tarantulas": 3, "FC Awesome": 0}

    second_game = "Lions 2, FC Awesome 2"
    parse_line(bracket ,second_game)
    assert bracket._bracket == { "Tarantulas": 3, "FC Awesome": 1, "Lions": 1}


def test_get_rankings():
    bracket = Bracket()
    bracket.update("Tottenham Spurs", 1)
    bracket.update("Lions", 3)
    bracket.update("Leopards", 3)

    ranking = bracket.get_rankings()
    assert ranking == [('Leopards', 3), ('Lions', 3), ('Tottenham Spurs', 1)]

