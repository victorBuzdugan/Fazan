

class Player:
    """ Player class. """

    name: str

    def __init__(self, name: str) -> None:
        """ Initialize the player."""

        self.name = name

    def play(self, round_no: int, word_start: str) -> str:
        pass


class HumanPlayer(Player):
    """ Human player class. """

    def __init__(self, name: str) -> None:
        super().__init__(name)


class AiPlayer(Player):
    """ AI player class. """

    dificulty: int

    def __init__(self, name: str, dificulty: int) -> None:
        super().__init__(name)
        self.dificulty = dificulty


