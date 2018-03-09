import HMM
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


    curr = stresses[token2index[key]][0]
    for x in stresses[token2index[key]][1:]:
        if x == curr:
            print(key)
            break
        curr = not curr
with open("stresses.json", "w") as f:
    json.dump({index2token[int(x)] : i for x, i in stresses.items()}, f)

reversed_hmm = HMM.unsupervised_HMM(reversed_lines, 15, 1)

rhyming_words = preprocessor.get_rhyme_pairs(preprocessor.load_sonnets())
rhyming_lines = []

for i in range(7):
    start1, start2 = "", ""
    while start1 not in token2index or start2 not in token2index:
        start1, start2 = random.choice(rhyming_words)
    start1 = token2index[start1]
    start2 = token2index[start2]
    line1 = reversed_hmm.generate_emission_syllables(10, syllable_dict, start1, stresses = stresses)[0]
    print(line1)
    line2 = reversed_hmm.generate_emission_syllables(10, syllable_dict, start2, stresses = stresses)[0]
    print(line2)
    rhyming_lines.append((" ".join([index2token[x] for x in line1[::-1]]),
                          " ".join([index2token[x] for x in line2[::-1]])))

sonnet = "\n".join([rhyming_lines[0][0],
                    rhyming_lines[1][0],
                    rhyming_lines[0][1],
                    rhyming_lines[1][1],

                    rhyming_lines[2][0],
                    rhyming_lines[3][0],
                    rhyming_lines[2][1],
                    rhyming_lines[3][1],

                    rhyming_lines[4][0],
                    rhyming_lines[5][0],
                    rhyming_lines[4][1],
                    rhyming_lines[5][1],

                    rhyming_lines[6][0],
                    rhyming_lines[6][1],
                    ])

print(sonnet)
