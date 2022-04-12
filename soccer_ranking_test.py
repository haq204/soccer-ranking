from click.testing import CliRunner

from soccer_ranking import Bracket, parse_line, Standing, print_standings, main

def test_parse_line():
    bracket = Bracket()
    first_game = "Tarantulas 1, FC Awesome 0"
    parse_line(bracket, first_game)
    assert bracket._bracket == { "Tarantulas": 3, "FC Awesome": 0}

    second_game = "Lions 2, FC Awesome 2"
    parse_line(bracket ,second_game)
    assert bracket._bracket == { "Tarantulas": 3, "FC Awesome": 1, "Lions": 1}

def test_bracket_get_sorted_teams():
    bracket = Bracket()
    bracket.update("Tottenham Spurs", 1)
    bracket.update("Lions", 6)
    bracket.update("Leopards", 3)

    standings = bracket.get_sorted_standings()
    assert standings == [Standing('Lions', 6), Standing('Leopards', 3), Standing('Tottenham Spurs', 1)]

def test_bracket_get_sorted_teams_with_ties():
    bracket = Bracket()
    bracket.update("Tottenham Spurs", 1)
    bracket.update("Lions", 3)
    bracket.update("Leopards", 3)

    standings = bracket.get_sorted_standings()
    assert standings == [Standing('Leopards', 3), Standing('Lions', 3), Standing('Tottenham Spurs', 1)]


def test_print_standings_no_ties():
    """Test output when there are no ties"""
    standings = [
        Standing("Tottenham Spurs", 9),
        Standing("Lions", 6),
        Standing("Leopards", 1),
        Standing("Grouches", 0),
    ]
    output = print_standings(standings)
    expected_str = "1. Tottenham Spurs, 9 pts\n2. Lions, 6 pts\n3. Leopards, 1 pt\n4. Grouches, 0 pts\n"
    assert output == expected_str


def test_print_standings_tie_at_end():
    """Test output when the last two teams are tied"""
    standings = [
        Standing("Tottenham Spurs", 9),
        Standing("Lions", 6),
        Standing("Leopards", 1),
        Standing("Grouches", 1),
    ]
    output = print_standings(standings)
    expected_str =(
        "1. Tottenham Spurs, 9 pts\n"
        "2. Lions, 6 pts\n"
        "3. Leopards, 1 pt\n"
        "3. Grouches, 1 pt\n"
    )
    assert output == expected_str

def test_print_standings_tie_in_middle():
    """Test output when the last two teams are tied"""
    standings = [
        Standing("Tottenham Spurs", 9),
        Standing("Lions", 3),
        Standing("Leopards", 3),
        Standing("Grouches", 0),
    ]
    output = print_standings(standings)
    expected_str = (
        "1. Tottenham Spurs, 9 pts\n"
        "2. Lions, 3 pts\n"
        "2. Leopards, 3 pts\n"
        "4. Grouches, 0 pts\n"
    )
    assert output == expected_str

def test_print_standings_tie_at_beginning():
    """Test output when the first two teams are tied"""
    standings = [
        Standing("Tottenham Spurs", 9),
        Standing("Lions", 9),
        Standing("Leopards", 3),
        Standing("Grouches", 0),
    ]
    output = print_standings(standings)
    expected_str = (
        "1. Tottenham Spurs, 9 pts\n"
        "1. Lions, 9 pts\n"
        "3. Leopards, 3 pts\n"
        "4. Grouches, 0 pts\n"
    )
    assert output == expected_str

def test_print_standings_multiple_ties():
    """Test output when there are multiple ties in the standings"""
    standings = [
        Standing("Tottenham Spurs", 9),
        Standing("Lions", 9),
        Standing("Leopards", 3),
        Standing("Grouches", 3),
    ]
    output = print_standings(standings)
    expected_str = (
        "1. Tottenham Spurs, 9 pts\n"
        "1. Lions, 9 pts\n"
        "3. Leopards, 3 pts\n"
        "3. Grouches, 3 pts\n"
    )
    assert output == expected_str

def test_cli():
    """Integration test that tests the CLI end to end"""
    runner = CliRunner()
    result = runner.invoke(main, ["-f", "samples/sample_input.txt"])
    assert result.exit_code == 0
    expected_output = (
        "1. Tarantulas, 6 pts\n"
        "2. Lions, 5 pts\n"
        "3. FC Awesome, 1 pt\n"
        "3. Snakes, 1 pt\n"
        "5. Grouches, 0 pts\n"
    )
    assert result.output == expected_output

def test_cli_with_second_sample():
    """Second end-to-end integration test"""
    runner = CliRunner()
    result = runner.invoke(main, ["-f", "samples/sample_input2.txt"])
    assert result.exit_code == 0
    expected_output = (
        "1. Spurs, 7 pts\n"
        "1. Tarantulas, 7 pts\n"
        "3. Lions, 5 pts\n"
        "4. Snakes, 4 pts\n"
        "5. FC Awesome, 1 pt\n"
        "6. Grouches, 0 pts\n"
    )
    assert result.output == expected_output
