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

        # TODO implement word start

        while True:
            print(f"\nRound {self.round_no}")
            for player in players:
                if self.round_no == 1 and player == player[0]:
                    current_word = player.play(start_letter, dictionary, no_endgame=True)
                


                    while True:
                        current_word = player.play(start_letter, no_endgame=True)
                        if current_word not in dictionary.words:
                            print(f"'{current_word}' is not in the dictionary!")
                            add_word = input(
                                f"Would you like to add '{current_word}' to the dictionary ('yes' for yes)?: ")

                player.play(self.round_no, word_start)
            else:
                self.round_no += 1
                if not players:
                    break

