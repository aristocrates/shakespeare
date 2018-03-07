"""
Module for preprocessing the sonnets
"""
import numpy as np
import pandas as pd

def syllable_dict(filename = 'data/Syllable_dictionary.txt',
                  end_syllable = False):
    """
    Loads a syllable dictionary

    Returns {words: num_syllables} if end_syllable is False
    otherwise {words: (num_syllables, num_syllables_end)}
    """
    # load with pandas to avoid errors, but still process things manually
    data = pd.read_csv('data/Syllable_dictionary.txt',
                       names = ['word', 'dat1', 'dat2'],
                       header = None, index_col = False,
                       delim_whitespace = True).as_matrix()
    syllables_normal = np.where(np.isnan(data[:,2].astype(float)),
                                data[:,1],data[:,2]).astype(int)
    syllables_end = np.where(np.isnan(data[:,2].astype(float)),
                             data[:,1], [d[-1] for d in data[:,1]]).astype(int)
    if end_syllable:
        return {word: (syllables_normal[i], syllables_end[i])
                for i, word in enumerate(data[:,0])}
    else:
        return {word: syllables_normal[i] for i, word in enumerate(data[:,0])}
