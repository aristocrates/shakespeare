"""
Module for preprocessing the sonnets
"""
import numpy as np
import pandas as pd

def punctuation_list():
    """
    Returns a set of punctuation marks
    """
    return frozenset([",", ".", "?", "!", ":", ";"])

class Sonnet:
    """
    Encapsulates a sonnet
    """
    def __init__(self, sonnet_lines):
        self.lines = list(sonnet_lines)

def syllable_dict(filename = 'data/Syllable_dictionary_updated.txt',
                  end_syllable = False):
    """
    Loads a syllable dictionary

    Returns {words: num_syllables} if end_syllable is False
    otherwise {words: (num_syllables, num_syllables_end)}
    """
    # load with pandas to avoid errors, but still process things manually
    data = pd.read_csv('data/Syllable_dictionary_updated.txt',
                       names = ['word', 'syll', 'syll_ending'],
                       header = None, index_col = False,
                       delim_whitespace = True).as_matrix()
    if end_syllable:
        return {word: (syll, syll_ending)
                for word, syll, syll_ending in data}
    else:
        return {word: syll
                for word, syll, _ in data}
print(syllable_dict(end_syllable = True))


def load_sonnets(sonnets_file = "data/shakespeare.txt", remove_num = True):
    """
    Returns array of sonnets from file
    Each sonnet is a list of lines in untokenized string format

    Keeps the number at the top
    """
    sonnets = []
    with open(sonnets_file, "r") as f:
        # don't give splitlines any args
        text = f.read()
        raw_lines = text.splitlines()

        current_sonnet = []
        prev_blank = True
        for line in raw_lines:
            if line == '':
                # don't append a blank sonnet on the second new line
                if not prev_blank:
                    sonnets.append(current_sonnet)
                    current_sonnet = []
                    prev_blank = True
            else:
                prev_blank = False
                current_sonnet.append(line)
        # add the last sonnet
        sonnets.append(current_sonnet)

        if remove_num:
            for i, sonnet in enumerate(sonnets):
                sonnets[i] = sonnet[1:]
        return sonnets

def line_words(line):
    """
    Tokenizes a line of text into words

    sonnet: array of lines in string format
    """
    return line.split()
