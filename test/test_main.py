import pytest

import main
from classes.player import AiPlayer, SMART_AI_THRESHOLD


@pytest.mark.parametrize(
    "user_input, level_return",
    [
        ("1", 1),
        ("8", 8),
        ("1.7", 1),
        ("0", 0),
        ("11", 0),
        ("", 0),
        ("z", 0),
    ]
)
def test_input_from_user_for_ai_level(
        monkeypatch: pytest.MonkeyPatch, user_input: str, level_return: int):
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    assert main.get_ai_level() == level_return

@pytest.mark.parametrize(
    "ai_level_arg, ai_player_level, ai_player_eliminated, ai_player_smart",
    [
        (1, 0.1, False, False),
        (SMART_AI_THRESHOLD - 1, (SMART_AI_THRESHOLD -1) / 10, False, False),
        (SMART_AI_THRESHOLD, SMART_AI_THRESHOLD /10, False, True),
        (10, 1, False, True),
    ]
)
def test_creation_of_ai_player(
        ai_level_arg: int, 
        ai_player_level: float,
        ai_player_eliminated: bool,
        ai_player_smart: bool):
    ai_player = main.create_ai_player(ai_level_arg)
    assert ai_player.ai_level == ai_player_level
    assert ai_player.eliminated == ai_player_eliminated
    assert ai_player.smart == ai_player_smart

@pytest.mark.parametrize(
    "human_players_number_input, \
     ai_player_exists, \
     human_players_number_returned",
    [
        (1.8, True, 1),
        (2.6, False, 2),
        (7.3, True, 7),
        (1, False, 0),
        (-6, False, 0),
        ("string", False, 0),
        ("", False, 0),
    ]
)
def test_input_from_user_for_number_of_human_players(
        human_players_number_input: int | float | str, 
        ai_player_exists: bool,
        human_players_number_returned: int):
    assert main.check_players_no(
            human_players_number_input, ai_player_exists
        ) == human_players_number_returned
