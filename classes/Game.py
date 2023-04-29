from random import choice

from classes.WordDictionary import WordDictionary
from classes.Player import Player

class Game:
    """ Game class """

    round_no: int

    def __init__(self) -> None:
        """ Initialize the game. """

        self.round_no = 1

    def play(self, players: list[Player], dictionary: WordDictionary) -> None:
        """ Play the game. """

        # Generate a start letter
        start_letter = choice("abcdefghijklmnopqrstuvwxyz")

        # Get word from players
        while len(players) > 1:
            print(f"\nRound {self.round_no}")
            for player in players:
                if self.round_no == 1 and player == players[0]:
                    current_word = player.play(start_letter, dictionary, no_endgame=True)
                else:
                    current_word = player.play(current_word[-2:], dictionary)
                
                if current_word == "remove_player":
                    print(f"\nPlayer '{player.name}' has been eliminated!")
                    players.remove(player)
            else:
                self.round_no += 1
        else:
            print(f"\nPlayer '{players[0].name}' has won the game!\n")
            dictionary.save_xml()
        


