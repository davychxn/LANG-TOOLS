import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), r'.\libs'))

from EngParser import EngParser


# csv file name
filename = r"..\assets\cmudict-0.7b"

syllables_all= {}

syllables_count_map = {}

syllables_maps_list = [{}, {}, {}, {}, {}, {}, {}]


# reading csv file
with open(filename, 'r', encoding='latin-1') as file:
    while line := file.readline():
        line = line.strip()
        if len(line) == 0:
            # Skip empty line
            continue
            
        row = line.split(" ")
        if (len(row) > 0) and (len(row[0]) > 0) and row[0][0].isalpha():
            word1 = row[0].strip().upper()
            
            marks = row[1:]
            marks_str = " ".join(marks)
            
            if len(marks_str) == 0:
                continue
            
            eng_parser = EngParser()
            map1, map2, map3, map4 = eng_parser.extract_syllables(marks_str)
            
            use_map = map2
            
            for key in use_map:
                if (key in syllables_all) and (use_map[key] != syllables_all[key]):
                    raise ValueError("Phonetics not consistent.")
                    
                if key not in syllables_all:                
                    count1 = len(use_map[key])
                    
                    syllables_maps_list[count1 - 1][key] = use_map[key]
                    
                syllables_all[key] = use_map[key]

p_id = 0

print(len(syllables_all))
#print(sorted(syllables_maps_list[p_id].keys()), len(syllables_maps_list[p_id]))
#print(syllables_maps_list)

json_obj = {}
# json_obj["syllables_all"] = syllables_all
json_obj["syllables_maps_list"] = syllables_maps_list

json_str = json.dumps(json_obj)

with open("../output/syllables_data.json", "w") as f:
    f.write(json_str)

print("Json exported.")


