import HMM
import preprocessor
import pickle
import random

def random_start(starters):
    return random.choice(starters)

# Get the sonnets from the sonnet file
sonnets = preprocessor.sonnets_from_file("data/tokenized_sonnets_unpunctuated.txt")

# Get dicts mapping indices and tokens
index2token = preprocessor.token_dict_from_file("data/token_dict_unpunctuated.json")
token2index = {t:int(i) for i, t in index2token.items()}

# Get the dictionary mapping words to syllables
word_syllable_dict = preprocessor.syllable_dict(end_syllable = True)
# Map the words to indices to get the syllable dictionary
syllable_dict = {token2index[x] : word_syllable_dict[x] for x in token2index.keys()}

# Set up the training data
reversed_lines = []
for sonnet in sonnets:
    reversed_lines += [line[::-1] for line in sonnet]

reversed_hmm = HMM.unsupervised_HMM(reversed_lines, 15, 10)


rhyming_words = preprocessor.get_rhyme_pairs(preprocessor.load_sonnets())
rhyming_lines = []

for i in range(7):
    start1, start2 = [token2index[x] for x in random.choice(rhyming_words)]
    line1 = reversed_hmm.generate_emission_syllables(10, syllable_dict, start1)[0]
    line2 = reversed_hmm.generate_emission_syllables(10, syllable_dict, start2)[0]
    rhyming_lines.append((" ".join([index2token[str(x)] for x in line1[::-1]]),
                          " ".join([index2token[str(x)] for x in line2[::-1]])))

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
