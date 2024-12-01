from libs.EngParser import EngParser

word_phonetics = {
    "communication": "K AH0 M Y UW2 N AH0 K EY1 SH AH0 N"
}

eng_parser = EngParser()
syllables_map = eng_parser.extract_syllables(word_phonetics["communication"])

print("Word 'communication' has following syllables: ", syllables_map.keys())
