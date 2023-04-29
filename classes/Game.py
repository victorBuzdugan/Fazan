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

        remaining_players = len(players)

        # Get word from players
        while remaining_players > 1:
            print(f"\nRound {self.round_no}")
            for player in players:
                if player.eliminated:
                    continue
                if (self.round_no == 1 and player == players[0]) or player_removed :
                    current_word = player.play(start_letter, dictionary, no_endgame=True)
                    dictionary.played_words.add(current_word)
                    dictionary.words.discard(current_word)
                    dictionary.endgame_words.discard(current_word)
                    player_removed = False
                else:
                    current_word = player.play(current_word[-2:], dictionary)
                    dictionary.played_words.add(current_word)
                    dictionary.words.discard(current_word)
                    dictionary.endgame_words.discard(current_word)
                
                if current_word == "remove_player":
                    print(f"\nPlayer '{player.name}' has been eliminated!")
                    player.eliminated = True
                    remaining_players -= 1
                    player_removed = True
                    if remaining_players == 1:
                        break
            else:
                self.round_no += 1
        else:
            for player in players:
                if player.eliminated == True:
                    continue
                else:
                    print(f"\nPlayer '{player.name}' has won the game!\n")
                    break
            dictionary.save_xml()
        


