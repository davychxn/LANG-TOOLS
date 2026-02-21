from libs.EngParser import EngParser

word_phonetics = {
    "communication": "K AH0 M Y UW2 N AH0 K EY1 SH AH0 N"
}

eng_parser = EngParser()
syllables_map, sound_map, stress_map, syllable_stress = eng_parser.extract_syllables(
    word_phonetics["communication"],
    return_stress=True
)

print("Word 'communication' has following syllables: ", syllables_map.keys())
print("sound_map:", sound_map)
print("stress_map:", stress_map)
print("syllable_stress:", syllable_stress)
