from click.testing import CliRunner

from soccer_ranking import Bracket, parse_line, Standing, print_standings, main

def test_parse_line():
    """Test parsing a single line from an input file"""
    bracket = Bracket()
    first_game = "Tarantulas 1, FC Awesome 0"
    parse_line(bracket, first_game)
    assert bracket._points == { "Tarantulas": 3, "FC Awesome": 0}
    assert bracket._gd == { "Tarantulas": 1, "FC Awesome": -1}

    second_game = "Lions 2, FC Awesome 2"
    parse_line(bracket ,second_game)
    assert bracket._points == { "Tarantulas": 3, "FC Awesome": 1, "Lions": 1}
    assert bracket._gd == { "Tarantulas": 1, "FC Awesome": -1, "Lions": 0}

def test_bracket_get_sorted_teams():
    """Test sorting the teams in a bracket"""
    bracket = Bracket()
    bracket.update("Tottenham Spurs", 1, 3)
    bracket.update("Lions", 6, 2)
    bracket.update("Leopards", 3, 1)

    standings = bracket.get_sorted_standings()
    assert standings == [
        Standing('Lions', 6, 2), Standing('Leopards', 3, 1), Standing('Tottenham Spurs', 1, 3)
    ]

def test_bracket_get_sorted_teams_with_points_ties():
    """Test sorting the teams in a bracket when multiple teams have the same number of points"""
    bracket = Bracket()
    bracket.update("Tottenham Spurs", 1, 1)
    bracket.update("Lions", 3, 3)
    bracket.update("Leopards", 3, 2)

    standings = bracket.get_sorted_standings()
    assert standings == [
        Standing('Lions', 3, 3),
        Standing('Leopards', 3, 2),
        Standing('Tottenham Spurs', 1, 1)
    ]

def test_bracket_get_sorted_items_with_points_and_gd_ties():
    """Test sorting the teams in a bracket when multiple teams have the same number of points and gd"""
    bracket = Bracket()
    bracket.update("Tottenham Spurs", 1, 1)
    bracket.update("Lions", 3, 3)
    bracket.update("Leopards", 3, 3)

    standings = bracket.get_sorted_standings()
    assert standings == [
        Standing('Leopards', 3, 3),
        Standing('Lions', 3, 3),
        Standing('Tottenham Spurs', 1, 1)
    ]

def test_print_standings_no_ties():
    """Test output when there are no ties"""
    standings = [
        Standing("Tottenham Spurs", 9, 3),
        Standing("Lions", 6, 2),
        Standing("Leopards", 1, 1),
        Standing("Grouches", 0, 0),
    ]
    output = print_standings(standings)
    expected_str = (
        "1. Tottenham Spurs, 9 pts, gd: 3\n"
        "2. Lions, 6 pts, gd: 2\n"
        "3. Leopards, 1 pt, gd: 1\n"
        "4. Grouches, 0 pts, gd: 0\n"
    )
    assert output == expected_str


def test_print_standings_tie_at_end():
    """Test output when the last two teams are tied"""
    standings = [
        Standing("Tottenham Spurs", 9, 3),
        Standing("Lions", 6, 2),
        Standing("Grouches", 1, 1),
        Standing("Leopards", 1, 1),
    ]
    output = print_standings(standings)
    expected_str =(
        "1. Tottenham Spurs, 9 pts, gd: 3\n"
        "2. Lions, 6 pts, gd: 2\n"
        "3. Grouches, 1 pt, gd: 1\n"
        "3. Leopards, 1 pt, gd: 1\n"
    )
    assert output == expected_str

def test_print_standings_tie_in_middle():
    """Test output when the last two teams are tied"""
    standings = [
        Standing("Tottenham Spurs", 9, 3),
        Standing("Leopards", 3, 2),
        Standing("Lions", 3, 2),
        Standing("Grouches", 0, 1),
    ]
    output = print_standings(standings)
    expected_str = (
        "1. Tottenham Spurs, 9 pts, gd: 3\n"
        "2. Leopards, 3 pts, gd: 2\n"
        "2. Lions, 3 pts, gd: 2\n"
        "4. Grouches, 0 pts, gd: 1\n"
    )
    assert output == expected_str

def test_print_standings_tie_at_beginning():
    """Test output when the first two teams are tied"""
    standings = [
        Standing("Lions", 9, 3),
        Standing("Tottenham Spurs", 9, 3),
        Standing("Leopards", 3, 2),
        Standing("Grouches", 0, 1),
    ]
    output = print_standings(standings)
    expected_str = (
        "1. Lions, 9 pts, gd: 3\n"
        "1. Tottenham Spurs, 9 pts, gd: 3\n"
        "3. Leopards, 3 pts, gd: 2\n"
        "4. Grouches, 0 pts, gd: 1\n"
    )
    assert output == expected_str

def test_print_standings_multiple_ties():
    """Test output when there are multiple ties in the standings"""
    standings = [
        Standing("Lions", 9, 2),
        Standing("Tottenham Spurs", 9, 2),
        Standing("Grouches", 3, 1),
        Standing("Leopards", 3, 1),
    ]
    output = print_standings(standings)
    expected_str = (
        "1. Lions, 9 pts, gd: 2\n"
        "1. Tottenham Spurs, 9 pts, gd: 2\n"
        "3. Grouches, 3 pts, gd: 1\n"
        "3. Leopards, 3 pts, gd: 1\n"
    )
    assert output == expected_str

def test_cli():
    """Integration test that tests the CLI end to end"""
    runner = CliRunner()
    result = runner.invoke(main, ["-f", "samples/sample_input.txt"])
    assert result.exit_code == 0
    expected_output = (
        "1. Tarantulas, 6 pts, gd: 3\n"
        "2. Lions, 5 pts, gd: 4\n"
        "3. FC Awesome, 1 pt, gd: -1\n"
        "4. Snakes, 1 pt, gd: -2\n"
        "5. Grouches, 0 pts, gd: -4\n"
    )
    print(result.output)
    assert result.output == expected_output

def test_cli_with_second_sample():
    """Second end-to-end integration test"""
    runner = CliRunner()
    result = runner.invoke(main, ["-f", "samples/sample_input2.txt"])
    assert result.exit_code == 0
    expected_output = (
        "1. Spurs, 7 pts, gd: 5\n"
        "2. Tarantulas, 7 pts, gd: 3\n"
        "3. Lions, 5 pts, gd: 2\n"
        "4. Snakes, 4 pts, gd: -1\n"
        "5. FC Awesome, 1 pt, gd: -1\n"
        "6. Grouches, 0 pts, gd: -8\n"
    )
    assert result.output == expected_output
