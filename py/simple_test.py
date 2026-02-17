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
    "K AA1 R B Y ER0 EH2 T"
]

for item in check_list:
    map1, map2 = eng_parser.extract_syllables(item, True)

    print(map1)
    print(map2)
    print("\n")
