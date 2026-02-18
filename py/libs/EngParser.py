import re
import inspect

class EngParser:
    def __init__(self):
        self.VOWELS = ['AH', 'EY', 'ER', 'AO', 'UW', 'IH', 'AA', 'IY', 'EH', 'AE', 'OW', 'AW', 'AY', 'UH', 'OY']
        self.CONSONANTS = ['W', 'Z', 'F', 'T', 'P', 'B', 'G', 'K', 'S', 'TH', 'D', 'V', 'SH', 'ZH', 'HH', 'JH', 'CH', 'DH']

        self.NASAL_STOPS = ['M', 'N', 'NG']
        self.R_COLORED = ['R']
        self.L_COLORED = ['L']
        self.DOUBLE_CONNECTIVE = ['Y']

        self.DOUBLE_USAGES = self.NASAL_STOPS + self.R_COLORED + self.L_COLORED + self.DOUBLE_CONNECTIVE

        self.W_COLORED = ['W']
        self.SEMI_VOWELS = ['W']
        self.SHUT_VOWELS = ['UW']
        self.DOUBLE_CONNECTIVE_VOWELS = ['ER']

        self.DOUBLE_CONSONANTS = {
            "T": ["R", "S"],
            "D": ["R", "S"]
        }
        
        self.parse_path = []

    def extract_syllables(self, phonems, is_print=False):
        syllables_map = {}
        sound_map = {}
        self.parse_path = []
        
        line = phonems.strip()
        if len(line) == 0:
            # Skip empty line
            self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
            return syllables_map, sound_map
            
        row = line.split(" ")
        if len(row) == 0:
            # Skip useless lines
            self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
            return syllables_map, sound_map
            
        syllable = []
        for i in range(len(row)):
            # Filter tones
            col = re.sub('[^a-zA-Z]+', '', row[i])
            if len(col) == 0:
                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                continue
            
            next_col = None
            if (i + 1) < len(row):
                # Has next col
                next_col = re.sub('[^a-zA-Z]+', '', row[i + 1])
                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
            
            next_col2 = None
            if (i + 2) < len(row):
                # Has next second col
                next_col2 = re.sub('[^a-zA-Z]+', '', row[i + 2])
                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
            
            if len(syllable) == 0:
                syllable.append(col)
                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                continue
            
            # TAG001
            if self.is_prev_vowel(syllable):
                if self.is_consonant(col):
                    if self.is_K(col) and next_col is not None and self.is_S(next_col):
                        syllable.append(col)
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                    
                    elif next_col is None:
                        syllable.append(col)
                        syl_name = "_".join(syllable)
                        syllables_map[syl_name] = syllable
                        sound_map[syl_name] = syllable
                        syllable = []
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                    
                    else:
                        syl_name = "_".join(syllable)
                        syllables_map[syl_name] = syllable
                        sound_map[syl_name] = syllable
                        syllable = [col]
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                
                elif self.is_vowel(col):
                    if (
                            self.is_prev_UW(syllable) or
                            self.is_prev_OW(syllable) or
                            self.is_prev_AW(syllable)
                       ):
                        # Example swear, vowel
                        syl_name = "_".join(syllable)
                        syllables_map[syl_name] = syllable
                        sound_map[syl_name] = syllable
                        phonem_W = self.get_W()
                        syllable = [phonem_W, col]
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                        
                    elif self.is_prev_ER(syllable):
                        # Example history
                        syl_name = "_".join(syllable)
                        syllables_map[syl_name] = syllable
                        sound_map[syl_name] = syllable
                        phonem_R = self.get_R()
                        syllable = [phonem_R, col]
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                        
                    else:
                        # Unconnectable vowels
                        # print("Unconnectable vowels", syllable[-1], col)
                        syl_name = "_".join(syllable)
                        syllables_map[syl_name] = syllable
                        sound_map[syl_name] = syllable
                        syllable = [col]
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                
                else:
                    # Other than vowels and consonants
                    if self.is_L(col) and (next_col is not None) and self.is_N(next_col) and (next_col2 is None):
                        # Example abeln
                        syl_name = "_".join(syllable)
                        syllables_map[syl_name] = syllable
                        sound_map[syl_name] = syllable
                        syllable = [col]
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                    
                    elif self.is_L(col) and (next_col is not None) and self.is_N(next_col) and (next_col2 is not None) and self.is_consonant(next_col2):
                        # Example kilnz
                        syl_name = "_".join(syllable)
                        syllables_map[syl_name] = syllable
                        sound_map[syl_name] = syllable
                        syllable = [col]
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                    
                    elif (
                            (not self.is_NG(col)) and
                            (next_col is not None) and
                            self.is_nasal(next_col) and
                            ((next_col2 is None) or self.is_consonant(next_col2))
                       ):
                        # Example Arm, Armstrong, ABELN, exclude MONTAGNE
                        syllable.append(col)
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                        
                    else:
                        # TAG002
                        if self.is_nasal(col):
                            if next_col is not None and (self.is_S(next_col) or self.is_Z(next_col) or self.is_T(next_col)) and next_col2 is None:
                                syllable.append(col)
                                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                                
                            else:
                                syllable.append(col)
                                syl_name = "_".join(syllable)
                                syllables_map[syl_name] = syllable
                                sound_map[syl_name] = syllable
                                syllable = [col]
                                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                        
                        # TAG003
                        elif self.is_R(col):
                            syllable.append(col)
                            syl_name = "_".join(syllable)
                            syllables_map[syl_name] = syllable
                            sound_map[syl_name] = syllable
                            syllable = [col]
                            self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                        
                        # TAG006
                        elif self.is_L(col):
                            if next_col is not None:
                                if self.is_vowel(next_col):
                                    syl_name = "_".join(syllable)
                                    syllables_map[syl_name] = syllable
                                    sound_map[syl_name] = syllable
                                    syllable = [col]
                                    self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                                    
                                else:
                                    # ZUELKE, ZUHLKE
                                    syllable.append(col)
                                    syl_name = "_".join(syllable)
                                    syllables_map[syl_name] = syllable
                                    sound_map[syl_name] = syllable
                                    syllable = []
                                    self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                                
                            else:
                                syllable.append(col)
                                syl_name = "_".join(syllable)
                                syllables_map[syl_name] = syllable
                                sound_map[syl_name] = syllable
                                syllable = []
                                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                        
                        # TAG004
                        elif self.is_Y(col):
                            syl_name = "_".join(syllable)
                            syllables_map[syl_name] = syllable
                            sound_map[syl_name] = syllable
                            syllable = [col]
                            self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                            
                        else:
                            raise ValueError("Unexpected crossing.")
                            pass
                    
            elif self.is_prev_consonant(syllable):
                if self.is_vowel(col):
                    syllable.append(col)
                    self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                    
                elif self.is_consonant(col):
                    if self.is_prev_K(syllable) and self.is_S(col) and ((next_col is not None and self.is_consonant(next_col)) or next_col is None):
                        syllable.append(col)
                        syl_name = "_".join(syllable)
                        sound_map[syl_name] = syllable
                        syllable = []
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                    
                    elif self.is_double_consonants(syllable[-1], col):
                        syllable.append(col)
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                    
                    else:
                        # Save stand-alone consonant
                        syl_name = "_".join(syllable)
                        sound_map[syl_name] = syllable
                        syllable = [col]
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                    
                else:
                    # TAG005
                    if self.is_Y(col):
                        if self.is_vowel(next_col):
                            # Cosonant + Y + Vowel + (, M, N, NG, L, R) syllable
                            syllable.append(col)
                            self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))

                        else:
                            syllable.append(col)
                            syl_name = "_".join(syllable)
                            syllables_map[syl_name] = syllable
                            sound_map[syl_name] = syllable
                            syllable = [col]
                            self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                    
                    elif self.is_R(col):
                        if self.is_double_consonants(syllable[-1], col):
                            syllable.append(col)
                            self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                            
                        else:
                            # Save stand-alone consonant
                            syl_name = "_".join(syllable)
                            sound_map[syl_name] = syllable
                            syllable = [col]
                            self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                    
                    else:
                        # Save stand-alone consonant
                        syl_name = "_".join(syllable)
                        sound_map[syl_name] = syllable
                        syllable = [col]
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
            
            else:
                # Previous phonem other than vowels and consonants, treat like consonants
                # Special handlings are done in TAG002, TAG003, TAG004, TAG005, TAG006, here is no need
                if self.is_vowel(col):
                    syllable.append(col)
                    self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                    
                elif self.is_consonant(col):
                    if len(syllable) == 1:
                        # Discard
                        syllable = [col]
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                        
                    elif (self.is_prev_N(syllable) or self.is_prev_NG(syllable)) and (self.is_S(col) or self.is_Z(col) or self.is_T(col)) and next_col is None:
                        syllable.append(col)
                        syl_name = "_".join(syllable)
                        syllables_map[syl_name] = syllable
                        sound_map[syl_name] = syllable
                        syllable = []
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                        
                    else:
                        # Save stand-alone phonem other than vowel and consonant
                        # Example NVidia
                        syl_name = "_".join(syllable)
                        syllables_map[syl_name] = syllable
                        sound_map[syl_name] = syllable
                        syllable = [col]
                        self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                    
                else:
                    if len(syllable) == 1:
                        if next_col is None:
                            if self.is_prev_L(syllable) and self.is_N(col):
                                # Example abeln
                                syllable.append(col)
                                syl_name = "_".join(syllable)
                                sound_map[syl_name] = syllable
                                syllable = []
                                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                            
                            elif self.is_Y(col):
                                # Example MONTAGNE
                                syllable.append(col)
                                syl_name = "_".join(syllable)
                                sound_map[syl_name] = syllable
                                syllable = []
                                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                                
                            else:
                                # Discard previous
                                syllable = [col]
                                syl_name = "_".join(syllable)
                                sound_map[syl_name] = syllable
                                syllable = []
                                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                            
                        elif (next_col is not None) and self.is_consonant(next_col):
                            if self.is_prev_L(syllable) and self.is_N(col):
                                # Example abeln
                                syllable.append(col)
                                syl_name = "_".join(syllable)
                                sound_map[syl_name] = syllable
                                syllable = []
                                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                            
                            elif self.is_Y(col):
                                syllable.append(col)
                                syl_name = "_".join(syllable)
                                sound_map[syl_name] = syllable
                                syllable = []
                                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                                
                            else:
                                # Example LANGLOIS
                                # Discard previous
                                syllable = [col]
                                syl_name = "_".join(syllable)
                                sound_map[syl_name] = syllable
                                syllable = []
                                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                            
                        else:
                            # Next is none consonant
                            syllable = [col]
                            self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                        
                    else:
                        if self.is_Y(col):
                            if not self.is_prev_Y(syllable):
                                syllable.append(col)
                                syl_name = "_".join(syllable)
                                syllables_map[syl_name] = syllable
                                sound_map[syl_name] = syllable
                                syllable = [col]
                                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                                
                            else:
                                # Double Y, discard
                                syllable = [col]
                                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                            
                        else:
                            if syllable[-1] != col:
                                if (next_col is None) or self.is_consonant(next_col):
                                    syllable.append(col)
                                    self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                                    
                                else:
                                    # Example carnation
                                    syllable = [col]
                                    self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                                
                            else:
                                # Double stand-alone phonem other than vowel and consonant, when the both are the same, discard
                                syllable = [col]
                                self.set_path("LN{}-{}".format(inspect.currentframe().f_lineno, syllable))
                            
        if len(syllable) > 0:
            if len(syllable) == 1:
                if self.is_prev_vowel(syllable):
                    syl_name = "_".join(syllable)
                    syllables_map[syl_name] = syllable
                    sound_map[syl_name] = syllable
                    syllable = []
                    
                elif self.is_prev_consonant(syllable):
                    # Save stand-alone consonant
                    syl_name = "_".join(syllable)
                    sound_map[syl_name] = syllable
                    
                else:
                    # If other than vowel or consonant left
                    if syllable[-1] != col:
                        # Save stand-alone phonem other than vowel or consonant
                        syl_name = "_".join(syllable)
                        sound_map[syl_name] = syllable
                    
            else:
                # syllable length > 1
                if self.is_prev_consonant(syllable):
                    if not self.is_double_consonants(syllable[-2], syllable[-1]):
                        raise ValueError("Unexpected entry", syllable)
                    
                else:
                    syl_name = "_".join(syllable)
                    syllables_map[syl_name] = syllable
                    sound_map[syl_name] = syllable
                    syllable = []

        if is_print:
            print("Parse path: ", self.parse_path)
            
        return syllables_map, sound_map

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
        
    def is_prev_none_vowel_consonant(self, phonems):
        self.verify_list(phonems)
        return not ((phonems[-1] in self.VOWELS) or (phonems[-1] in self.CONSONANTS))

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
        
    def is_prev_K(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] == 'K'
        
    def is_prev_S(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] == 'S'
        
    def is_prev_M(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] == self.NASAL_STOPS[0]
        
    def is_prev_N(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] == self.NASAL_STOPS[1]
        
    def is_prev_NG(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] == self.NASAL_STOPS[2]

    def is_prev_UW(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] in self.SHUT_VOWELS

    def is_prev_AW(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] == self.VOWELS[11]

    def is_prev_OW(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] == self.VOWELS[10]

    def is_prev_ER(self, phonems):
        self.verify_list(phonems)
        return phonems[-1] in self.DOUBLE_CONNECTIVE_VOWELS

    def is_vowel(self, phonem):
        self.verify_str(phonem)
        return phonem in self.VOWELS
            
    def is_consonant(self, phonem):
        self.verify_str(phonem)
        return phonem in self.CONSONANTS

    def is_none_vowel_consonant(self, phonem):
        self.verify_str(phonem)
        return not ((phonem in self.VOWELS) or (phonem in self.CONSONANTS))

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

    def is_NG(self, phonem):
        self.verify_str(phonem)
        return phonem == self.NASAL_STOPS[2]
        
    def is_N(self, phonem):
        self.verify_str(phonem)
        return phonem == self.NASAL_STOPS[1]
        
    def is_K(self, phonem):
        self.verify_str(phonem)
        return phonem == 'K'
        
    def is_S(self, phonem):
        self.verify_str(phonem)
        return phonem == 'S'
        
    def is_Z(self, phonem):
        self.verify_str(phonem)
        return phonem == 'Z'
        
    def is_T(self, phonem):
        self.verify_str(phonem)
        return phonem == 'T'

    def is_double_consonants(self, prev, cur):
        self.verify_str(prev)
        self.verify_str(cur)
        return prev in self.DOUBLE_CONSONANTS and cur in self.DOUBLE_CONSONANTS[prev]

    def get_R(self):
        return self.R_COLORED[0]

    def get_W(self):
        return self.W_COLORED[0]

    def get_Y(self):
        return self.DOUBLE_CONNECTIVE[0]
        
    def set_path(self, nodeId):
        self.verify_str(str(nodeId))
        self.parse_path.append(str(nodeId))
        