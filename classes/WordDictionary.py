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
    __words_start: set[str]
    __words_end: set[str]
    words: set[str]

    def __init__(self, path: Path) -> None:
        """ Create a dictionary with filtered words imported from file path. 
        
        Path - 'path' to the input file including filename and extension
        """

        self.__path = path
        self.words = set()
        self.__words_start = set()
        self.__words_end = set()
        self.__parse_xml(self.__path)
        self.__parse_words()

        # ! remove after testing
        
        
    # region: xml related methods
    def __parse_xml(self, path: Path) -> None:
        """ Parse the xml file. """
        
        print("... Loading xml file ...")
        self.__tree = ET.parse(path)
        self.__root = self.__tree.getroot()
    
    def __save_xml(self):
        """ Write changes to xml file """

        print("... Saving dictionary to file ...")
        # Re-format the xml file
        ET.indent(self.__root)
        
        self.__tree.write(self.__path, "UTF-8", True)
    # endregion

    def __word_check(self, word: str, index: int, words_to_remove: tuple) -> bool:
        """ Check if a word is ok to be inserted in list
        or if it needs to be removed. 
        
        If it's ok add the first and last two letters of the word
        to separate sets.
        """
        
        if word in words_to_remove:
            self.__rename_word(index, word)
            return False

        if len(word) < 3:
            return False
        accepted_chars = {
            char for char in "abcdefghijklmnopqrstuvwxyz"
            }
        for char in word:
            if char not in accepted_chars:
                return False
        else:
            self.__words_start.add(word[:2])
            self.__words_end.add(word[-2:])
            return True
        
    def __parse_words(self, words_to_remove: tuple =()) -> None:
        """ Build and filter a set of all words from the input file. """

        if words_to_remove:
            print('Rebuilding dictionary...')
        else:
            print('Building dictionary...')


        # self.words = set()

        for index in range(len(self.__root)):
            
            # Not with 'lower()' to exclude names
            current_word: str = self.__root[index][1].text

            # Strip of '(...)' using regex
            current_word = re.sub(
                pattern=r" \(.+?\)",
                repl="",
                string=current_word
                )

            # Check length
            if len(current_word) < 3:
                continue

            # Replace diacritics
            current_word = self.__normalize_word(current_word)

            # If the word contains variations
            if " / " in current_word:
                for variation in current_word.split(" / "):
                    if self.__word_check(variation, index, words_to_remove):
                        self.words.add(variation)
            else:
                if self.__word_check(current_word, index, words_to_remove):
                    self.words.add(current_word)
        else:
            self.__endgame_words()

    def __normalize_word(self, word: str) -> str:
        """ Replace diacritics with normalized characters. """
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

    def remove_word(self, *words) -> None:
        """ Pseudo-removes the 'word' and rebuild the dictionary. """

        for word in words:
            print(f"Removing '{word}'...")
        self.__parse_words(words_to_remove= words)

        self.__save_xml()

    def __rename_word(self, index: int, word_to_remove: str) -> None:
        """ Pseudo-removes the 'word_to_remove' from dictionary
        by renaming it with '__' prefix.
        """

        if " / " in self.__root[index][1].text:
            word_split = self.__root[index][1].text.split(" / ")
            for pos, word in enumerate(word_split):
                word_normalized = self.__normalize_word(word)
                if (
                    word_normalized == word_to_remove or
                    (" (" in word and
                    word_normalized.startswith(word_to_remove + " ")
                    )
                    ):
                        word_split[pos] = "__" + word
            text_to_write = " / ".join([str(word) for word in word_split])
        else:
            if "__" not in self.__root[index][1].text:
                text_to_write = "__" + self.__root[index][1].text

        self.__root[index][1].text = text_to_write

    def add_word(self, word: str) -> None:
        """ Add new word to dictionary. """

        # Find the last element 'id'
        elements = self.__root.findall("Entry")
        last_el_id = int(elements[-1].attrib["id"])

        # Build new element
        new_entry = ET.Element("Entry", {"id": str(last_el_id + 1)})
        new_timestamp = ET.SubElement(new_entry, "Timestamp")
        new_timestamp.text = str(int(time.time()))
        new_description = ET.SubElement(new_entry, "Description")
        new_description.text = word + " (user added)"

        # Add new element to xml
        print(f"Adding {word} to dictionary...")
        if (
            ET.iselement(new_entry) &
            ET.iselement(new_timestamp) &
            ET.iselement(new_description)
            ):
            self.__root.append(new_entry)
        else:
            print(f"Error adding '{word}' to dictionary!!!")

        self.__save_xml()

        self.__parse_xml(self.__path)
        self.__parse_words(words_to_remove= " ")

    def __endgame_words(self) -> None:
        """ Create a set of words that can end the game. """

        self.endgame_words = {word for word in self.words if word[-2:] in self.__words_end.difference(self.__words_start)}

    