import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), r'.\libs'))

from EngParser import EngParser

eng_parser = EngParser()

check_list = [
    "K AH0 M P Y UW1 T ER0",
    "IH0 K S P IH1 R IY0 AH0 N S",
    "IH2 N F AO2 R M EY1 SH AH0 N",
    "K AA1 R B Y ER0 EH2 T",
    "IH0 K S P AE1 N SH AH0 N Z",
    "M AY K R OW S AO F T",
    "T EH1 S T",
    "EY2 V IY0 EY1 SH AH0 N",
    "R EY1 N JH IH0 NG"
]

for item in check_list:
    map1, map2, stress_map, syllable_stress_map = eng_parser.extract_syllables(item, True)

    print(map1)
    print(map2)
    print(stress_map)
    print(syllable_stress_map)
    print("\n")
