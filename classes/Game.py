from random import choice

from classes.Player import Player

class Game:
    """ Game class """

    round_no: int

    def __init__(self) -> None:
        """ Initialize the game. """

        self.round_no = 0

    def play(self, players: list[Player]) -> None:
        """ Play the game. """

        # Generate a start letter
        start_letter = choice("abcdefghijklmnopqrstuvwxyz")

        # TODO implement word start
        word_start = "xx"

        # while True:
        #     for player in players:
        #         player.play(self.round_no, word_start)
        #     else:
        #         self.round_no += 1

        for i in players:
            print(i.name)

        pass


    def __start_letter() -> str:
        """ Returns a letter to start the game. """

        return 