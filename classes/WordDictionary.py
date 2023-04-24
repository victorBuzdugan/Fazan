import xml.etree.ElementTree as ET
from pathlib import Path
import re
import time

# 5_530

class WordDictionary:
    """ A dictionary of words used in the game. """
    
    __path: Path
    __tree: ET
    __root: ET.Element
    words: set[str]
    __words_start: set[str]
    __words_end: set[str]
    endgame_words: set[str]
    __words_to_add: list[str]
    __words_to_remove: list[str]

    def __init__(self, path: Path) -> None:
        """ Create a dictionary with filtered words imported from file path. 
        
        Path - 'path' to the input file including filename and extension
        """

        self.__path = path
        self.words = set()
        self.__words_start = set()
        self.__words_end = set()
        self.__words_to_add = []
        self.__words_to_remove = []
        self.__parse_xml(self.__path)
        self.__build_dictionary()

    # region: xml related methods
    def __parse_xml(self, path: Path) -> None:
        """ Parse the xml file. """
        
        print("... Loading xml file ...")
        self.__tree = ET.parse(path)
        self.__root = self.__tree.getroot()
    
    def save_xml(self):
        """ Write changes to xml file """

        if self.__words_to_remove or self.__words_to_add:
            print("... Saving dictionary to file ...")
            # Re-format the xml file
            ET.indent(self.__root)
            self.__tree.write(self.__path, "UTF-8", True)
    # endregion

    # region: build game dictionaries
    def __build_dictionary(self, words_to_remove: tuple =()) -> None:
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
        for index in range(len(self.__root)):
            
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
                        self.__words_to_remove.append(word_variation)
                    else:
                        self.words.add(word_variation)
                        self.__words_start.add(word_variation[:2])
                        self.__words_end.add(word_variation[-2:])
        else:
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
        
        # Re-check lengh in case is a variation
        if len(word) < 3:
            return False
        
        # Check if word characters are in the alphabet
        # Also check and exclude if the word contains big letters (name...)
        accepted_chars = {
            char for char in "abcdefghijklmnopqrstuvwxyz"
            }
        for char in word:
            if char not in accepted_chars:
                return False
        else:
            return True

    def __build_endgame_words(self) -> None:
        """ Create a set of words that can end the game. """

        self.endgame_words = {word for word in self.words if word[-2:] in self.__words_end.difference(self.__words_start)}
    # endregion

    # region: add/remove words
    def add_words(self, *words: tuple) -> None:
        """ Add new word(s) to dictionary. """

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
            
            self.__words_to_add.append(word)

            # Add new element to tree
            print(f"... Adding '{word}' to dictionary ...")
            self.__root.append(new_entry)

    def remove_words(self, *words) -> None:
        """ Pseudo-removes the 'word(s)' and rebuild the dictionary. """

        for word in words:
            print(f"... Removing '{word}' ...")
        self.__build_dictionary(words_to_remove= words)

    def __rename_word(self, index: int, word_to_remove: str) -> None:
        """ Pseudo-removes the 'word_to_remove' from dictionary
        by renaming it with '__' prefix.

        Preserve the initial description with diacritics and paranthesis.
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
    # endregion







    # region: file export
    def export_to_file(self, base_dir, type: str ="filtered") -> None:
        """ Export a filtered on unfiltered word list to txt file.
        
        'type' can be 'filtered' or 'unfiltered'.
        'base_dir' is the main.py directory
        Export to txt file in '{base_dir}/output' directory.
        If 'output' directory doesn't exist, it doesn't create it.

        Only used for testing.
        """

        if type.lower() == "filtered":
            filename = "words_filtered.txt"
        elif type.lower() == "unfiltered":
            filename = "words_unfiltered.txt"
        else:
            raise ValueError(f"Invalid type: {type}")

        file_path = Path(base_dir, 'output', filename)

        with open(file_path, "w", encoding="utf-8") as file:
            if filename == "words_filtered.txt":
                file.write('\n'.join(str(i) for i in self.words))
            elif filename == "words_unfiltered.txt":
                file.write('\n'.join(str(i) for i in self.__parse_words_unfiltered()))
    # endregion


    




    # region: testing
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


