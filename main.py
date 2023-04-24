from pathlib import Path, PurePosixPath

from classes.WordDictionary import WordDictionary


base_dir = PurePosixPath(__file__).parent
path = Path(base_dir, 'input', 'DEXOnline_xsmall.xml')
dictionary = WordDictionary(path)

# word_dictionary.export_to_file(base_dir)

# variables
# actions like "... Loading xml file ..."



x = input("Options: ('q' for quit): ")

if x == "q":
    dictionary.save_xml()




