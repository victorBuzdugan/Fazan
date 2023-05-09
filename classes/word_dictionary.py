""" Word Dictionary class module. """

import xml.etree.ElementTree as ET
import os
import re
import time


class WordDictionary:
    """ A dictionary of words used in the game. """

    __path: str
    __tree: ET
    __root: ET.Element
    words: set[str]
    __words_start: set[str]
    __words_end: set[str]
    endgame_words: set[str]
    __words_to_add: bool
    __words_to_remove: list[str]
    played_words: set[str]

    def __init__(self, path: str) -> None:
        """ Create a dictionary with filtered words imported from file path.

        Path - 'path' to the input file including filename and extension
        """

        self.__path = path
        self.words = set()
        self.__words_start = set()
        self.__words_end = set()
        self.__words_to_add = False
        self.__words_to_remove = []
        self.played_words = set()
        self.__parse_xml(self.__path)
        self.__build_dictionary()

    # region: xml related methods
    def __parse_xml(self, path: str) -> None:
        """ Parse the xml file. """

        print("... Loading xml file ...")
        self.__tree = ET.parse(path)
        self.__root = self.__tree.getroot()

    def save_xml(self):
        """ Write changes to xml file. """

        if self.__words_to_remove or self.__words_to_add:
            if self.__words_to_remove:
                self.remove_words(*self.__words_to_remove)
            print("... Saving dictionary to file ...")
            # Re-format the xml file
            ET.indent(self.__root)
            self.__tree.write(self.__path, "UTF-8", True)
    # endregion

    # region: build game dictionaries
    def __build_dictionary(self, words_to_remove: tuple = ()) -> None:
        """ Build a game word dictionary.

        Build a filtered set of game words and a set of words
        that can end the game.
        Also used for ~removing word(s).
        """

        if words_to_remove:
            print('... Rebuilding dictionary ...')
        else:
            print('... Building dictionary ...')

        # Use 'range' to get the 'index' for ~removing word(s)
        xml_len = len(self.__root)
        for index in range(xml_len):

            if index == int(xml_len / 2):
                print("... Halfway there ...")

            # Not with 'lower()' method to auto-exclude names
            current_word: str = self.__root[index][1].text

            # Strip of '(...)' using regex
            current_word = re.sub(
                pattern=r" \(.+?\)",
                repl="",
                string=current_word
                )

            # Pre-check length
            if len(current_word) < 3:
                continue

            current_word = self.__replace_diacritics(current_word)

            # Check for word variations
            for word_variation in current_word.split(" / "):
                if self.__word_check(word_variation):
                    if word_variation in words_to_remove:
                        self.__rename_word(index, word_variation)
                    else:
                        self.words.add(word_variation)
                        self.__words_start.add(word_variation[:2])
                        self.__words_end.add(word_variation[-2:])

        self.__build_endgame_words()

    def __replace_diacritics(self, word: str) -> str:
        """ Replace diacritics with 'normalized' characters. """

        diacritics = {
                "ă": "a",
                "â": "a",
                "î": "i",
                "ș": "s",
                "ț": "t"
            }
        for diacritic, replacement in diacritics.items():
            if diacritic in word:
                word = word.replace(diacritic, replacement)
        return word

    def __word_check(self, word: str) -> bool:
        """ Check if a word is ok to be inserted in dictionary. """

        # Re-check length in case is a variation
        if len(word) < 3:
            return False

        # Check if word characters are in the alphabet
        # Also check and exclude if the word contains big letters (name...)
        accepted_chars = set("abcdefghijklmnopqrstuvwxyz")
        for char in word:
            if char not in accepted_chars:
                return False
        else:
            return True

    def __build_endgame_words(self) -> None:
        """ Create a set of words that can end the game. """

        self.endgame_words = {
            word for word in self.words
            if word[-2:] in self.__words_end.difference(self.__words_start)}
    # endregion

    # region: add/remove words
    def add_words(self, *words: tuple[str]) -> None:
        """ Add new word(s) to dictionary. """

        # Add word(s) to game
        for word in words:
            self.played_words.add(word)

        # Find the last element 'id'
        last_id = int(self.__root[len(self.__root) - 1].attrib["id"])

        timestamp = str(int(time.time()))

        for word in words:
            # Build new element
            new_entry = ET.Element("Entry", {"id": str(last_id + 1)})
            entry_timestamp = ET.SubElement(new_entry, "Timestamp")
            entry_timestamp.text = timestamp
            entry_description = ET.SubElement(new_entry, "Description")
            entry_description.text = word + " (added by fazan)"
            last_id += 1

            self.__words_to_add = True

            # Add new element to tree
            print(f"... Adding '{word}' to dictionary ...")
            self.__root.append(new_entry)

    def remove_words(self, *words) -> None:
        """ Pseudo-removes the 'word(s)' and rebuild the dictionary. """

        for word in words:
            print(f"... Removing '{word}' ...")
        self.__build_dictionary(words_to_remove=words)

    def __rename_word(self, index: int, word_to_remove: str) -> None:
        """ Pseudo-removes the 'word_to_remove' from dictionary
        by renaming it with '__' prefix.

        Preserve the initial description with diacritics and parenthesis.
        """

        word_split = self.__root[index][1].text.split(" / ")
        for pos, word in enumerate(word_split):
            word_parsed = re.sub(
                pattern=r" \(.+?\)",
                repl="",
                string=word
                )
            word_parsed = self.__replace_diacritics(word_parsed)
            if word_parsed == word_to_remove:
                word_split[pos] = "__" + word
        else:
            self.__root[index][1].text = " / ".join(
                [str(word) for word in word_split]
                )

    def discard_word(self, word: str, remove: bool = False):
        """ Remove a word from current game. """

        self.played_words.add(word)
        self.words.discard(word)
        self.endgame_words.discard(word)
        if remove:
            self.__words_to_remove.append(word)
            print(f"... Removed '{word}' from game ...")
    # endregion

    # region: get game words
    def get_word(self,
                 word_start: str,
                 no_endgame: bool = True,
                 smart_ai: bool = False
                 ) -> str:
        """Get a random word from dictionary that starts with 'word_start'."""

        # All the words that start with 'word_start'
        words = {word for word in self.words if word.startswith(word_start)}
        # Words with endings which doesn't remove next player
        not_endgame_words = words.difference(self.endgame_words)
        # Words with endings which removes next player
        endgame_words = words.intersection(self.endgame_words)
        # Words with endings which doesn't remove next player,
        # but also leaves no endgame words to him
        if smart_ai:
            found_word = False
            for not_endgame_word in not_endgame_words:
                if found_word is True:
                    break
                for endgame_word in self.endgame_words:
                    if not_endgame_word[-2:] == endgame_word[:2]:
                        break
                else:
                    smart_ai_word = not_endgame_word
                    break
            else:
                smart_ai_word = ""

        if words:
            if no_endgame:
                # Try to get a word that doesn't end the game
                if smart_ai and smart_ai_word:
                    return smart_ai_word
                if not_endgame_words:
                    return not_endgame_words.pop()
                else:
                    return words.pop()
            else:
                # Try to get a word that ends the game
                if endgame_words:
                    return endgame_words.pop()
                else:
                    if smart_ai and smart_ai_word:
                        return smart_ai_word
                    else:
                        return words.pop()
        else:
            return ""
    # endregion

    # region: testing
    def __export_to_file(self, export_type: str = "filtered") -> None:
        """ Export a filtered on unfiltered word list to txt file.

        'type' can be 'filtered' or 'unfiltered'.
        'base_dir' is the 'main.py' directory
        Export to txt file in '{base_dir}/output' directory.
        If 'output' directory doesn't exist, it doesn't create it!

        Used for testing.
        """

        if export_type.lower() == "filtered":
            filename = "words_filtered.txt"
        elif export_type.lower() == "unfiltered":
            filename = "words_unfiltered.txt"
        else:
            raise ValueError(f"Invalid type: '{export_type}'")

        file_path = os.path.join('output', filename)
        file_path = os.path.join('output', filename)

        print(f"... Exporting to '/output/{filename}' ...")
        with open(file_path, "w", encoding="utf-8") as file:
            if filename == "words_filtered.txt":
                file.write('\n'.join(str(i) for i in self.words))
            elif filename == "words_unfiltered.txt":
                file.write('\n'.join(str(i) for i in self.__parse_words_unfiltered()))

    def __parse_words_unfiltered(self) -> set:
        """ Build an unfiltered set of all words from the input file.

        Only used for testing.
        """

        words_unfiltered = {
            self.__root[index][1].text.lower()
            for index in range(len(self.__root))
            if len(self.__root[index][1].text) > 2
            }
        return words_unfiltered
    # endregion
