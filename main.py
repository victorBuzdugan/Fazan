""" Main game file. """

import os
from random import shuffle, choice

from classes.word_dictionary import WordDictionary
from classes.game import Game
from classes.player import HumanPlayer, AiPlayer

INPUT_FILE = "DEXOnline.xml"

AI_NAMES = ("shaquille.oatmeal", "fast_and_curious", "casanova",
            "YellowSnowman", "unfinished_sentenc", "tinfoilhat",
            "anonymouse", "crazy_cat_lady", "fluffycookie", "Babushka",
            "FartinLutherKing", "fatBatman", "ima.robot", "fartoolong")


# region: AI Player functions
def get_ai_level() -> int:
    """ Get input from user how 'smart' should de computer player be. """

    level = input("Enter computer level -> 1(easy) ... 10(hard): ")
    try:
        level = int(float(level))
        if level not in range(1, 11):
            raise ValueError
    except ValueError:
        print(f"'{level}' is not in range of 1...10!")
        return 0
    else:
        return level


def create_ai_player(level: int) -> AiPlayer:
    """ Create a computer player. """

    name = choice(AI_NAMES)
    return AiPlayer(name=name, ai_level=float(level))
# endregion


# region: Human player(s) functions
def check_players_no(players_no: str, ai_player: bool) -> int:
    """ Get input from user on how many 'human' players play the game.

    If there is a computer player then minimum number is one human player.
    Otherwise the game should have at least two human players.
    """

    try:
        players_no = int(float(players_no))
    except ValueError:
        print(f"'{players_no}' is not a number!")
        return False
    else:
        if not ai_player and players_no < 2:
            print("Expected at least 2 'human' players!")
        elif ai_player and players_no < 1:
            print("Expected at least 1 'human' player!")
        else:
            return players_no
        return 0
# endregion


def main():
    """ Main function. """

    # Create words dictionary
    path = os.path.join("input", INPUT_FILE)
    try:
        dictionary = WordDictionary(path)
    except Exception as err:
        print("There was a problem creating the dictionary!")
        print(f"Check that '{INPUT_FILE}' exists and is a valid xml file")
        print(err)
        return 1

    # AI Player
    if input("Play vs computer ('y' for yes)?: ").lower() == "y":
        while True:
            level = get_ai_level()
            if level != 0:
                break
        players = [create_ai_player(level)]
    else:
        players = []

    # Human player(s)
    while True:
        human_players = input("Enter how many 'human' players: ")
        if human_players := check_players_no(human_players, bool(players)):
            break
    for player in range(human_players):
        name = input(f"Player {player + 1} name: ")
        players.append(HumanPlayer(name))

    game = Game()
    shuffle(players)
    game.play(players, dictionary)
    return 0


if __name__ == "__main__":
    main()
