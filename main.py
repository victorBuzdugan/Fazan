import os
from random import shuffle, choice

from classes.WordDictionary import WordDictionary
from classes.Game import Game
from classes.Player import HumanPlayer, AiPlayer


INPUT_FILE = "DEXOnline.xml"
# INPUT_FILE = "DEXOnline_small.xml"
# INPUT_FILE = "DEXOnline_xsmall.xml"

# Create words dictionary
path = os.path.join("input", INPUT_FILE)
dictionary = WordDictionary(path)


players = []

# AI player
if input("Play vs computer ('y' for yes)?: ").lower() == "y":
    ai_name = choice(("shaquille.oatmeal", "fast_and_curious",
                "casanova", "YellowSnowman", "unfinished_sentenc",
                "tinfoilhat", "anonymouse", "crazy_cat_lady",
                "fluffycookie", "Babushka", "FartinLutherKing",
                "fatBatman", "ima.robot", "fartoolong"))
    while True:
        ai_level = input("Enter computer level -> 1(easy) ... 10(hard): ")
        try:
            ai_level = float(ai_level)
            if ai_level not in range(1, 11):
                raise ValueError
        except ValueError:
            print(f"'{ai_level}' is not in range of 1...10!")
        else:
            break
    players.append(AiPlayer(name = ai_name, ai_level = ai_level))

# Human player(s)
while True:
    human_players_no = input("Enter how many 'human' players: ")
    try:
        human_players_no = int(human_players_no)
        if not players and human_players_no < 2:
            print("Expected at least 2 'human' players!")
            continue
        elif players and human_players_no < 1:
            print("Expected at least 1 'human' player!")
            continue
    except ValueError:
        print(f"'{human_players_no}' is not a number!")
    else:
        for player in range(human_players_no):
            name = input(f"Player {player + 1} name: ")
            players.append(HumanPlayer(name))
        break

game = Game()

shuffle(players)
game.play(players, dictionary)