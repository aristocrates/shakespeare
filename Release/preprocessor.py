"""
Module for preprocessing the sonnets
"""
import numpy as np
import pandas as pd
from collections import OrderedDict
import re

def punctuation_list(as_frozen_set = False):
    """
    Returns a set of punctuation marks
    """
    dict_list = [",", ".", "?", "!", ":", ";"]
    if as_frozen_set:
        return frozenset(dict_list)
    else:
        return dict_list

def all_tokens():
    """
    Gets a dict of all tokens
    """
    return {token:i for i, token in enumerate(punctuation_list() +
                                              list(syllable_dict().keys()))}

def tokens_to_indices(tokens, all_tokens_dict):
    """
    Gives a consistent assignment of a word or punctuation mark to a
    unique number from 0 to num_tokens

    Whenever the tokenization changes, change this function accordingly

    tokens: a list of strings
    tokens_dict: {token:index}
    """
    return [all_tokens_dict[tok] for tok in tokens]

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
        return OrderedDict([(word, (syll_norm, syll_end))
                            for word, syll_norm, syll_end in data])
    else:
        return OrderedDict([(word, syll_norm) for word, syll_norm, _ in data])

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

# def tokenize_line(line):
#     tokens = all_tokens()
#     punctuation = punctionation_list()
#     words = line.strip().split(" ")
#     tokens = []
#     the = False
#     for word in words:
#         word = 
#         if the:
#             tokens.append("the "+word)
#         if a:
#             tokens.append("a "+word)
#         else:
#             tokens.append(word)


    

def line_words(line):
    """
    Tokenizes a line of text into words

    sonnet: array of lines in string format
    """
    return line.split()
