"""
Module for preprocessing the sonnets
"""
import numpy as np
import pandas as pd
from collections import OrderedDict
import re
import json

def punctuation_list(as_frozen_set = False):
    """
    Returns a set of punctuation marks
    """
    dict_list = [",", ".", "?", "!", ":", ";", "'", "(", ")"]
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

def get_rhyme_pairs(sonnets):
    """
    """
    rhyme_pattern = [(0,2),(1,3),(4,6),(5,7),(8,10),(9,11),(12,13)]
    rhyme_pairs = []
    for sonnet in sonnets:
        for r in rhyme_pattern:
            try:
                first_rhyme = sonnet[r[0]].split()[-1].strip(" .,:;'()!?")
                second_rhyme = sonnet[r[1]].split()[-1].strip(" .,:;'()!?")
                rhyme_pairs.append((first_rhyme, second_rhyme))
            except IndexError:
                print("That one stupid sonnet")
    return rhyme_pairs

def tokens_to_indices(tokens, all_tokens_dict):
    """
    Gives a consistent assignment of a word or punctuation mark to a
    unique number from 0 to num_tokens

    Whenever the tokenization changes, change this function accordingly

    tokens: a list of strings
    tokens_dict: {token:index}
    """
    return [all_tokens_dict[tok] for tok in tokens]

def syllable_dict_punct(filename = 'data/Syllable_dictionary_updated2.txt',
                        end_syllable = False, keys_as_nums = True):
    """
    Gives dictionary of syllables including punctuation
    """
    #sylldict = syllable_dict(filename, end_syllable)
    #ans = {k:}
    pass

def syllable_dict(filename = 'data/Syllable_dictionary_updated2.txt',
                  end_syllable = False):
    """
    Loads a syllable dictionary

    Returns {words: num_syllables} if end_syllable is False
    otherwise {words: (num_syllables, num_syllables_end)}
    """
    # load with pandas to avoid errors, but still process things manually
    data = pd.read_csv(filename,
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

def tokenize_line(line):
    """
    Tokenizes the line into a list of tokens.
    """
    def append_if_token(character, valid_tokens, lst):
        if character != "":
            if character not in tokens:
                raise Exception(character + " isn't in tokens")
            lst.append(character)
    # tokens is the list of valid tokens
    tokens = all_tokens()
    # The tokenized version of the line
    tokenized = []

    # Just break the line on spaces to get the words, plus some punctuations
    naive_words = [word.lower().strip() for word in line.strip().split(" ")]
    # The and a are the booleans refering to whether the or a modifies the 
    # current words
    the = False
    a = False

    for word in naive_words:
        # The list of punctuation that needs to be added to the token list after
        # main word.
        punct = []
        # Match the word to find the punctuation at the beginning and end of
        # the word
        matches = re.match("^([^a-zA-Z]*)(.*?)([^a-zA-Z]*)$", word.strip())
        befores = list(matches.group(1))
        word = matches.group(2)
        afters = list(matches.group(3))

        # If there are punctuation marks before the main word, and the previous
        #punctuation mark + word makes a valid word, then add that as the word
        if not (len(befores) == 0) and befores[-1] + word in tokens:
            word = befores[-1] + word
            for after in afters:
                append_if_token(after, tokens, punct)
            for before in befores[:-1]:
                append_if_token(before, tokens, tokenized)

        elif not (len(afters) == 0) and word + afters[0] in tokens:
            word = word + afters[0]
            for after in afters[1:]:
                append_if_token(after, tokens, punct)
            for before in befores:
                append_if_token(before, tokens, tokenized)

        # If the word is a token by itself, then add it to the word list 
        elif word in tokens:
            for after in afters:
                append_if_token(after, tokens, punct)
            for before in befores:
                append_if_token(before, tokens, tokenized)
        else:
            raise Exception(word + " isn't in tokens")

        # Check if the previous word is the, and then append the+word if that's
        # the case
        if the:
            tokenized.append("the "+word)
            the = False
        elif a:
            tokenized.append("a "+word)
            a = False
        else:
            if word == "the":
                the = True
                continue
            if word == "a":
                a = True
                continue
            tokenized.append(word)
        tokenized += punct
    assert(all(token in tokens for token in tokenized))
    return tokenized

def line_words(line):
    """
    Tokenizes a line of text into words

    sonnet: array of lines in string format
    """
    return line.split()

def dump_to_file(token_dict_file = "data/token_dict.json",
        sonnet_file = "data/tokenized_sonnets.txt"):
    sonnets = load_sonnets()
    used_tokens = set()
    tokenized_sonnets = []
    for sonnet in sonnets:
        tokenized_lines = []
        for line in sonnet:
            tokenized_lines.append(tokenize_line(line))
            used_tokens = used_tokens.union(set(tokenized_lines[-1]))
        tokenized_sonnets.append(tokenized_lines)

    token2index = {token : i for i, token in enumerate(used_tokens)}
    with open(token_dict_file, "w") as f:
        json.dump(token2index, f)

    indices_sonnets = [[[token2index[token] for token in line] for line in sonnet] for sonnet in tokenized_sonnets]
    with open(sonnet_file, "w") as f:
        for sonnet in indices_sonnets:
            for line in sonnet:
                f.write(" ".join([str(x) for x in line]) + "\n")
            f.write("\n\n")

def sonnets_from_file(sonnet_file = "data/tokenized_sonnets.txt"):
    with open(sonnet_file) as f:
        sonnets = []
        sonnet = []
        for line in f:
            if line == "\n" and len(sonnet) != 0:
                sonnets.append(sonnet)
                sonnet = []
            if line != "\n":
                tokens = [int(token) for token in line.split(" ")]
                sonnet.append(tokens)
    return sonnets

def token_dict_from_file(token_dict_file = "data/token_dict.json"):
    return json.load(open(token_dict_file))
