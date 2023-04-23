from pathlib import Path, PurePosixPath

from classes.WordDictionary import WordDictionary


base_dir = PurePosixPath(__file__).parent
path = Path(base_dir, 'input', 'DEXOnline_small.xml')
word_dictionary = WordDictionary(path)

word_dictionary.export_to_file(base_dir)

# variables
# actions like '--- Saving dictionary to file ---'