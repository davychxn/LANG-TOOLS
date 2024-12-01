import re

class EngParser:
    def __init__(self):
        self.VOWELS = ['AH', 'EY', 'ER', 'AO', 'UW', 'IH', 'AA', 'IY', 'EH', 'AE', 'OW', 'AW', 'AY', 'UH', 'OY']
        self.CONSONANTS = ['W', 'Z', 'F', 'T', 'P', 'B', 'G', 'K', 'S', 'TH', 'D', 'V', 'SH', 'ZH', 'HH', 'JH', 'CH', 'DH']

        self.NASAL_STOPS = ['M', 'N', 'NG']
        self.R_COLORED = ['R']
        self.L_COLORED = ['L']
        self.DOUBLE_CONNECTIVE = ['Y']

        self.DOUBLE_USAGES = self.NASAL_STOPS + self.R_COLORED + self.L_COLORED + self.DOUBLE_CONNECTIVE

        self.SHUT_VOWELS = ['UW']
        self.DOUBLE_CONNECTIVE_VOWELS = ['ER']

        self.DOUBLE_CONSONANTS = {
            "T": "R",
            "D": "R",
            "T": "S",
            "D": "S"
        }

    def extract_syllables(self, phonems):
        syllables_map = {}
        
        line = phonems.strip()
        if len(line) == 0:
            # Skip empty line
            return syllables_map
            
        row = line.split(" ")
        if len(row) == 0:
            # Skip useless lines
            return syllables_map
            
        syllable = []
        for i in range(len(row)):
            # Filter tones
            col = re.sub('[^a-zA-Z]+', '', row[i])
            if len(col) == 0:
                continue
            
            next_col = None
            if i < (len(row) - 1):
                # Has next col
                next_col = re.sub('[^a-zA-Z]+', '', row[i + 1])
            
            if len(syllable) == 0:
                syllable.append(col)
                continue
            
            # TAG001
            if self.is_prev_vowel(syllable):
                if self.is_consonant(col):
                    syl_name = "_".join(syllable)
                    syllables_map[syl_name] = syllable
                    syllable = [col]
                
                elif self.is_vowel(col):
                    if self.is_prev_UW(syllable):
                        syl_name = "_".join(syllable)
                        syllables_map[syl_name] = syllable
                        syllable = [col]
                        
                    elif self.is_prev_ER(syllable):
                        syl_name = "_".join(syllable)
                        syllables_map[syl_name] = syllable
                        syllable = [col]
                        
                    else:
                        # Unconnectable vowels
                        # print("Unconnectable vowels", syllable[-1], col)
                        syl_name = "_".join(syllable)
                        syllables_map[syl_name] = syllable
                        syllable = [col]
                
                # TAG002
                elif self.is_nasal(col):
                    syllable.append(col)
                    syl_name = "_".join(syllable)
                    syllables_map[syl_name] = syllable
                    syllable = [col]
                
                # TAG003
                elif self.is_R(col):
                    syllable.append(col)
                    syl_name = "_".join(syllable)
                    syllables_map[syl_name] = syllable
                    syllable = [col]
                
                # TAG006
                elif self.is_L(col):
                    if next_col is not None:
                        if self.is_vowel(next_col):
                            syl_name = "_".join(syllable)
                            syllables_map[syl_name] = syllable
                            syllable = [col]
                            
                        else:
                            # ZUELKE, ZUHLKE
                            syllable.append(col)
                            syl_name = "_".join(syllable)
                            syllables_map[syl_name] = syllable
                            syllable = []
                        
                    else:
                        syllable.append(col)
                        syl_name = "_".join(syllable)
                        syllables_map[syl_name] = syllable
                        syllable = []
                
                # TAG004
                elif self.is_Y(col):
                    syl_name = "_".join(syllable)
                    syllables_map[syl_name] = syllable
                    syllable = [col]
                    
                else:
                    raise ValueError("Unexpected crossing.")
                    pass
                    
            elif self.is_prev_consonant(syllable):
                if self.is_vowel(col):
                    syllable.append(col)
                    
                elif self.is_consonant(col):
                    if self.is_double_consonants(syllable[-1], col):
                        syllable.append(col)
                    
                    else:
                        syllable = [col]
                    
                else:
                    # TAG005
                    if self.is_Y(col):
                        syllable.append(col)
                        syl_name = "_".join(syllable)
                        syllables_map[syl_name] = syllable
                        syllable = [col]
                    
                    elif self.is_R(col):
                        if self.is_double_consonants(syllable[-1], col):
                            syllable.append(col)
                            
                        else:
                            syllable = [col]
                    
                    else:
                        syllable = [col]
            
            else:
                # Previous phonem other than vowels and consonants, treat like consonants
                # Special handlings are done in TAG002, TAG003, TAG004, TAG005, TAG006, here is no need
                if self.is_vowel(col):
                    syllable.append(col)
                    
                elif self.is_consonant(col):
                    syllable = [col]
                    
                else:
                    if self.is_Y(col):
                        if not self.is_prev_Y(syllable):
                            syllable.append(col)
                            syl_name = "_".join(syllable)
                            syllables_map[syl_name] = syllable
                            syllable = [col]
                            
                        else:
                            syllable = [col]
                        
                    else:
                        syllable = [col]
                            
        if len(syllable) > 0:
            if len(syllable) == 1:
                if self.is_prev_vowel(syllable):
                    syl_name = "_".join(syllable)
                    syllables_map[syl_name] = syllable
                    syllable = []
                    
            else:
                # syllable length > 1
                if self.is_prev_consonant(syllable):
                    if not self.is_double_consonants(syllable[-2], syllable[-1]):
                        raise ValueError("Unexpected entry", syllable)
                    
                else:
                    syl_name = "_".join(syllable)
                    syllables_map[syl_name] = syllable
                    syllable = []

        return syllables_map

    def verify_list(self, phonems):
        if not isinstance(phonems, list):
            raise ValueError("Phonems sequence should be a list.")
        if len(phonems) == 0:
            raise ValueError("Empty phonems sequence.")

    def verify_str(self, phonem):
        if not isinstance(phonem, str):
            raise ValueError("Phonem should be a str.")
        if len(phonem) == 0:
            raise ValueError("Empty phonem name.")

    def is_prev_vowel(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] in self.VOWELS
            
    def is_prev_consonant(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] in self.CONSONANTS

    def is_prev_W(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] in self.SEMI_VOWELS

    def is_prev_nasal(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] in self.NASAL_STOPS

    def is_prev_R(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] in self.R_COLORED

    def is_prev_L(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] in self.L_COLORED

    def is_prev_Y(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] in self.DOUBLE_CONNECTIVE

    def is_prev_UW(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] in self.SHUT_VOWELS

    def is_prev_ER(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] in self.DOUBLE_CONNECTIVE_VOWELS

    def is_vowel(self, phonem):
        self.verify_str(phonem)
        return phonem in self.VOWELS
            
    def is_consonant(self, phonem):
        self.verify_str(phonem)
        return phonem in self.CONSONANTS

    def is_W(self, phonem):
        self.verify_str(phonem)
        return phonem in self.SEMI_VOWELS

    def is_nasal(self, phonem):
        self.verify_str(phonem)
        return phonem in self.NASAL_STOPS

    def is_R(self, phonem):
        self.verify_str(phonem)
        return phonem in self.R_COLORED

    def is_L(self, phonem):
        self.verify_str(phonem)
        return phonem in self.L_COLORED

    def is_Y(self, phonem):
        self.verify_str(phonem)
        return phonem in self.DOUBLE_CONNECTIVE

    def is_UW(self, phonem):
        self.verify_str(phonem)
        return phonem in self.SHUT_VOWELS

    def is_ER(self, phonem):
        self.verify_str(phonem)
        return phonem in self.DOUBLE_CONNECTIVE_VOWELS

    def is_double_consonants(self, prev, cur):
        self.verify_str(prev)
        self.verify_str(cur)
        return prev in self.DOUBLE_CONSONANTS and self.DOUBLE_CONSONANTS[prev] == cur
