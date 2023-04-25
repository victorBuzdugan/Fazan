from pathlib import Path, PurePosixPath

from classes.WordDictionary import WordDictionary


base_dir = PurePosixPath(__file__).parent
path = Path(base_dir, 'input', 'DEXOnline_small.xml')
dictionary = WordDictionary(path)


x = input("Options: ('q' for quit): ")

if x == "q":
    dictionary.save_xml()




