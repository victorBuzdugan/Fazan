from random import choice

from classes.WordDictionary import WordDictionary
from classes.Player import Player

class Game:
    """ Game class """

    def __init__(self) -> None:
        """ Initialize the game. """
        pass

    def play(self,
             players: list[Player], 
             dictionary: WordDictionary
             ) -> None:
        """ Play the game. """

        # Generate a start letter
        start_letter = choice("abcdefghijklmnopqrstuvwxyz")
        
        round_no = 1
        remaining_players = len(players)

        # Get word from players
        while remaining_players > 1:
            print(f"\nRound {round_no}")
            for player in players:
                if player.eliminated:
                    continue
                if (round_no == 1 and player == players[0]) or player_removed:
                    current_word = player.play(start_letter,
                                               dictionary,
                                               no_endgame_input=True)
                    player_removed = False
                else:
                    current_word = player.play(current_word[-2:], dictionary)
                
                if current_word == "remove_player":
                    print(f"\nPlayer '{player.name}' has been eliminated!")
                    player.eliminated = True
                    remaining_players -= 1
                    if remaining_players == 1:
                        break
                    else:
                        player_removed = True
                        start_letter = choice("abcdefghijklmnopqrstuvwxyz")
                else:
                    dictionary.discard_word(current_word)
            else:
                round_no += 1
        else:
            for player in players:
                if player.eliminated == False:
                    print(
                        f"\nPlayer '{player.name}' has won the game "
                        f"in {round_no} rounds!\n"
                        )
                    break
            dictionary.save_xml()
        


