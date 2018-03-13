import HMM
import numpy as np
import preprocessor
import pickle
import random
import nltk
import json
import re

def random_start(starters):
    return random.choice(starters)

# Get the sonnets from the sonnet file
sonnets = preprocessor.sonnets_from_file("data/tokenized_sonnets_stresses.txt")

# Get dicts mapping indices and tokens
token2index = preprocessor.token_dict_from_file("data/token_dict_stresses.json")
index2token = {int(i):t for t, i in token2index.items()}

# Get the dictionary mapping words to syllables
word_syllable_dict = preprocessor.syllable_dict(end_syllable = True)
# Map the words to indices to get the syllable dictionary
syllable_dict = {token2index[x] : word_syllable_dict[x] for x in token2index.keys()}

# Set up the training data
reversed_lines = []
for sonnet in sonnets:
    reversed_lines += [line[::-1] for line in sonnet]

cmu_dict = nltk.corpus.cmudict.dict()

stresses = dict()
def get_stresses(word, cmu_dict):
    sylls = cmu_dict[word][0]
    stresses = []
    for syll in sylls:
        matches = re.match("^\w+(\d+)$", syll)
        if matches:
            stresses.append(int(matches.group(1)) > 0)
    return stresses

for key in token2index.keys():
    stresses[token2index[key]] = []
    mod_key = key
    two_words = False
    if len(key.split(" ")) == 2:
        two_words = True
        mod_key = key.split(" ")[1]
    hyphen = mod_key.split("-")
    if len(hyphen) == 2:
        stresses[token2index[key]] += get_stresses(hyphen[0], cmu_dict) + \
                                      get_stresses(hyphen[1], cmu_dict)
    else:
        stresses[token2index[key]] += get_stresses(mod_key, cmu_dict)
    if two_words:
        stresses[token2index[key]] = [not stresses[token2index[key]][0]] + stresses[token2index[key]]

with open("stresses.json", "w") as f:
    json.dump({index2token[int(x)] : i for x, i in stresses.items()}, f)


rhyming_classes = [list(x) for x in preprocessor.get_rhyme_classes(preprocessor.load_sonnets())]
rhyming_triples = [list(x) for x in rhyming_classes if len(x) > 2]

rhyming_pair = [""]
while any(x not in token2index for x in rhyming_pair):
    rhyming_pair = np.random.choice(np.random.choice(rhyming_classes), size = 2, replace = False)
print(rhyming_pair)

rhyming_triple = [""]
while any(x not in token2index for x in rhyming_triple):
    rhyming_triple = np.random.choice(np.random.choice(rhyming_triples), size = 3, replace = False)
print(rhyming_triple)

reversed_hmm = HMM.unsupervised_HMM(reversed_lines, 15, 10)

wanted_stress_1 = [True, False, False, True, False, False, True, False, False]
wanted_stress_2 = [True, False, False, True, False, False]

triple = []
for x in rhyming_triple:
    ind = token2index[x]
    triple.append(reversed_hmm.generate_emission_syllables(9, syllable_dict, ind, stresses = stresses, desired_stresses = [x for x in wanted_stress_1])[0])

pair = []
for x in rhyming_pair:
    ind = token2index[x]
    pair.append(reversed_hmm.generate_emission_syllables(6, syllable_dict, ind, stresses = stresses, desired_stresses = [x for x in wanted_stress_1])[0])


lymmerick = "\n".join([ " ".join([index2token[x] for x in triple[0][::-1]]),
                     " ".join([index2token[x] for x in triple[1][::-1]]),
                     " ".join([index2token[x] for x in pair[0][::-1]]),
                     " ".join([index2token[x] for x in pair[1][::-1]]),
                     " ".join([index2token[x] for x in triple[2][::-1]])
                    ])

print(lymmerick)
