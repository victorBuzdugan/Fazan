from random import random

from classes.WordDictionary import WordDictionary

PROB_SUGGEST_WORD = 0.7
SMART_AI_TRESHOLD = 0.6

class Player:
    """ Player class. """

    name: str
    eliminated: bool

    def __init__(self, name: str) -> None:
        """ Initialize the player."""

        self.name = name
        self.eliminated = False

    def play(self,
             word_start: str,
             dictionary: WordDictionary,
             no_endgame_input: bool =False) -> str:
        """ Get a verified word from player. """

        raise NotImplementedError


class HumanPlayer(Player):
    """ Human player class. """

    def __init__(self, name: str) -> None:
        super().__init__(name)
    
    def play(self,
             word_start: str,
             dictionary: WordDictionary,
             no_endgame_input: bool = False
             ) -> str:
        while True:
            word = input(
                f"\n'{self.name}' enter a word that starts with '{word_start}'"
                f" ('qq' if you don't know; 'h' for help): "
                ).lower()
            if word == "qq":
                return "remove_player"
            if word == "h":
                if dictionary.get_word(word_start):
                    print(f"There are words that start with '{word_start}'")
                else:
                    print(f"There are no words that start with '{word_start}'")
            elif len(word) < 3:
                print(f"'{word}' has less than 3 letters!")
                continue
            elif not word.startswith(word_start):
                print(f"'{word}' doesn't starts with '{word_start}'")
                continue
            elif word in dictionary.played_words:
                print(f"'{word}' has allready been played this game!")
                continue
            elif no_endgame_input and word in dictionary.endgame_words:
                print("You can't eliminate a player with the first word!)")
                continue
            elif word not in dictionary.words:
                print(f"'{word}' is not in the dictionary!")
                add_word_prompt = input(
                    f"Would you like to add '{word}' to the dictionary "
                    f"('yes' for yes)?: "
                    ).lower()
                if add_word_prompt == "yes":
                    dictionary.add_words(word)
                    return word
            else:
                # Randomly suggest an endgame word
                if random() > PROB_SUGGEST_WORD and not no_endgame_input:
                    suggest_word = dictionary.get_word(word_start, False)
                    if (suggest_word and
                        suggest_word in dictionary.endgame_words):
                        print(
                            f"... You could have eliminated next player "
                            f"with '{suggest_word}'"
                            )
                return word

class AiPlayer(Player):
    """ AI player class. """

    ai_level: float

    def __init__(self, name: str, ai_level: float) -> None:
        super().__init__(name)
        self.ai_level = ai_level
        if self.ai_level >= SMART_AI_TRESHOLD:
            self.smart = True
        else:
            self.smart = False

    def play(self,
             word_start: str,
             dictionary: WordDictionary,
             no_endgame_input: bool = False
             ) -> str:

        # Randomly try to end the game
        if no_endgame_input or random() > self.ai_level:
            no_endgame = True
        else:
            no_endgame = False

        while True:
            word = dictionary.get_word(word_start, no_endgame, self.smart)
            if (word == "" or
                (no_endgame_input == True and word in dictionary.endgame_words)
                ):
                print(f"\n'{self.name}' enter a word that starts "
                        f"with '{word_start}': qq")
                if word != "":
                    print("I can't find a word that doesn't end the game!")
                return "remove_player"
            else:
                print(f"\n'{self.name}' enter a word that starts "
                        f"with '{word_start}': {word}")
                if word in dictionary.endgame_words:
                    print(
                        f"There are no words in dictionary with {word[-2:]}!")
                remove_word = input(
                    f"Type 'remove' to remove '{word}' from dictionary: ").lower()
                if remove_word == "remove":
                    dictionary.discard_word(word, remove=True)
                    continue
                else:
                    return word