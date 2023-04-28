from random import choice

from classes.WordDictionary import WordDictionary

class Player:
    """ Player class. """

    name: str

    def __init__(self, name: str) -> None:
        """ Initialize the player."""

        self.name = name

    def play(self,
             word_start: str,
             dictionary: WordDictionary,
             no_endgame: bool =False) -> str:
        """ Get a verified word from player """

        raise NotImplementedError


class HumanPlayer(Player):
    """ Human player class. """

    def __init__(self, name: str) -> None:
        super().__init__(name)
    
    def play(self,
             word_start: str,
             dictionary: WordDictionary,
             no_endgame: bool = False) -> str:
        while True:
            word = input(f"Enter a word that starts with '{word_start}' :").lower()
            if word in dictionary


class AiPlayer(Player):
    """ AI player class. """

    ai_level: int

    def __init__(self, name: str, ai_level: int) -> None:
        super().__init__(name)
        self.ai_level = ai_level


