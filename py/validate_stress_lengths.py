import os
import sys
from collections import Counter

sys.path.append(os.path.join(os.path.dirname(__file__), r'.\libs'))
from EngParser import EngParser

filename = os.path.join(os.path.dirname(__file__), r'..\assets\cmudict-0.7b')

parser = EngParser()
stats = Counter()
mismatches = []
errors = []

with open(filename, 'r', encoding='latin-1') as file:
    for line_no, line in enumerate(file, 1):
        line = line.strip()
        if len(line) == 0:
            continue

        row = line.split(' ')
        if (len(row) == 0) or (len(row[0]) == 0) or (not row[0][0].isalpha()):
            continue

        word = row[0].strip().upper()
        marks = [p for p in row[1:] if len(p.strip()) > 0]
        if len(marks) == 0:
            continue

        stats['words'] += 1

        try:
            _, sound_map, stress_map, _ = parser.extract_syllables(' '.join(marks))
        except Exception as ex:
            stats['errors'] += 1
            if len(errors) < 10:
                errors.append((line_no, word, str(ex)))
            continue

        for key, phones in sound_map.items():
            stats['sound_entries'] += 1
            stress_list = stress_map.get(key)

            if stress_list is None:
                stats['missing_stress_key'] += 1
                if len(mismatches) < 20:
                    mismatches.append((line_no, word, key, phones, None, 'missing_key'))
                continue

            if len(stress_list) != len(phones):
                stats['length_mismatch'] += 1
                if len(mismatches) < 20:
                    mismatches.append((line_no, word, key, phones, stress_list, 'length_mismatch'))

print('RESULTS')
print('words=', stats['words'])
print('sound_entries=', stats['sound_entries'])
print('errors=', stats['errors'])
print('missing_stress_key=', stats['missing_stress_key'])
print('length_mismatch=', stats['length_mismatch'])
print('total_mismatch=', stats['missing_stress_key'] + stats['length_mismatch'])
print('sample_mismatches=', mismatches)
print('sample_errors=', errors)
