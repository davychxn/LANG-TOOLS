# LANG-TOOLS / Python - English Syllable Extractor

[English](./README.md) | [中文](./README_CN.md)

A Python toolkit for extracting and cataloging all unique English syllable patterns from the [CMU Pronouncing Dictionary](http://www.speech.at.cs.cmu.edu/cgi-bin/cmudict).

## Overview

This tool parses ARPAbet phoneme sequences from the CMU dictionary and splits them into syllable units using a rule-based algorithm. The core design principle is **"double usage"** -- certain phonemes (nasals M/N/NG, liquids R/L, and glide Y) serve as both the coda of one syllable and the onset of the next, reflecting how these sounds behave in natural English speech.

## Project Structure

```
py/
  libs/
    EngParser.py         # Core syllable extraction engine
  scan_syllables2.py     # Batch scanner - processes entire CMU dictionary
  example.py             # Usage example for a single word
  syllables_data.json    # Output - all extracted syllable patterns
```

## Phoneme Classification

The algorithm classifies ARPAbet phonemes into three groups:

| Group | Phonemes | Role in Syllable |
|-------|----------|-----------------|
| **Vowels** (15) | AH, EY, ER, AO, UW, IH, AA, IY, EH, AE, OW, AW, AY, UH, OY | Syllable nucleus |
| **Consonants** (18) | W, Z, F, T, P, B, G, K, S, TH, D, V, SH, ZH, HH, JH, CH, DH | Syllable onset only |
| **Double-usage** (6) | M, N, NG, R, L, Y | Both onset and coda |

Additionally, consonant clusters **TR**, **DR**, **TS**, **DS** are treated as valid double-consonant onsets.

## Algorithm

1. Iterate through the phoneme sequence left-to-right
2. When a vowel is followed by a regular consonant, the consonant starts a **new** syllable (maximum onset principle)
3. When a vowel is followed by a double-usage phoneme (M, N, NG, R, L), that phoneme is appended to the **current** syllable as coda, then also starts the **next** syllable as onset
4. Special vowel-to-vowel transitions:
   - UW/OW/AW + vowel: inserts a bridging **W** (e.g., "swear")
   - ER + vowel: inserts a bridging **R** (e.g., "history")
   - Other vowel pairs: split directly

## Output Format

`syllables_data.json` contains:

```json
{
  "syllables_all": {
    "K_AE": ["K", "AE"],
    "T_R_IY": ["T", "R", "IY"],
    "R_AH_N": ["R", "AH", "N"],
    ...
  },
  "syllables_maps_list": [
    { /* 1-phoneme syllables (34 entries) */ },
    { /* 2-phoneme syllables (436 entries) */ },
    { /* 3-phoneme syllables (1387 entries) */ },
    { /* 4-phoneme syllables (213 entries) */ },
    {}, {}, {}
  ]
}
```

Total unique syllable patterns: **2,070**

## Usage

### Single word

```python
from libs.EngParser import EngParser

eng_parser = EngParser()
syllables_map, sound_map = eng_parser.extract_syllables("K AH0 M Y UW2 N AH0 K EY1 SH AH0 N")

print(sound_map.keys())
# dict_keys(['K_AH', 'M', 'Y_UW', 'N_AH', 'K_EY', 'SH_AH', 'N'])
```

### Batch scan (full dictionary)

```bash
python scan_syllables2.py
```

This reads the CMU dictionary file, extracts all syllable patterns, and exports `syllables_data.json`.

**Running result:**

```
D:\...\LANG-TOOLS\py>python scan_syllables2.py
2070
Json exported.
```

## Requirements

- Python 3.8+
- CMU Pronouncing Dictionary file (`cmudict-0.7b`)
- No external dependencies
