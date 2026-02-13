import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), r'.\libs'))

from EngParser import EngParser

eng_parser = EngParser()
map1, map2 = eng_parser.extract_syllables("AE1 B IH0 L N", True)

print(map1)
print(map2)
