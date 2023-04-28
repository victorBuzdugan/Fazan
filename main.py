import os
from random import shuffle, choice

from classes.WordDictionary import WordDictionary
from classes.Game import Game
from classes.Player import Player, HumanPlayer, AiPlayer


# INPUT_FILE = "DEXOnline.xml"
# INPUT_FILE = "DEXOnline_small.xml"
INPUT_FILE = "DEXOnline_xsmall.xml"

path = os.path.join("input", INPUT_FILE)
dictionary = WordDictionary(path)


# Get players list from input
players = []
# TODO implement dificulty
# AI player
if input("Play vs computer ('y' for yes)?: ").lower() == "y":
    ai_name = choice(("shaquille.oatmeal", "fast_and_curious",
                "casanova", "YellowSnowman", "unfinished_sentenc",
                "tinfoilhat", "anonymouse", "crazy_cat_lady",
                "fluffycookie", "Babushka", "FartinLutherKing",
                "fatBatman", "ima.robot", "fartoolong"))
    dificulty = 1
    players.append(AiPlayer(ai_name, dificulty))

# Human player(s)
while True:
    no_human_players = input("Enter how many 'human' players: ")
    try:
        no_human_players = int(no_human_players)
        if not players and no_human_players < 2:
            print("Expected at least 2 'human' players!")
            continue
        elif players and no_human_players < 1:
            print("Expected at least 1 'human' player!")
            continue
    except ValueError:
        print(f"'{no_human_players}' is not a number!")
    else:
        for player in range(no_human_players):
            name = input(f"Player {player + 1} name: ")
            players.append(HumanPlayer(name))
        break


game = Game()


shuffle(players)
game.play(players)


x = input("Options: ('q' for quit): ")

if x == "q":
    dictionary.save_xml()


