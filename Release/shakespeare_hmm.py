import HMM
import preprocessor
import pickle
import random
import nltk
import json
import re
import argparse

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

def upper_first(word):
    return word[0].upper() + word[1:]
    
def do_hmm(num_states = 15, verbose = False, give_hmm = False):
    """
    verbose:  output the debugging stress pattern matrix
    give_hmm: if True, 
    """
    reversed_hmm = HMM.unsupervised_HMM(reversed_lines, n_states = num_states,
                                        N_iters = 20, verbose = verbose)

    rhyming_words = preprocessor.get_rhyme_pairs(preprocessor.load_sonnets())
    rhyming_lines = []
    wanted_stress = [True, False, True, False, True, False, True, False, True, False]
    for i in range(7):
        start1, start2 = "", ""
        while start1 not in token2index or start2 not in token2index:
            start1, start2 = random.choice(rhyming_words)
        start1 = token2index[start1]
        start2 = token2index[start2]
        line1 = reversed_hmm.generate_emission_syllables(10, syllable_dict, start1,
                                                         stresses = stresses,
                                                         desired_stresses = [x for x in wanted_stress])[0]
        line2 = reversed_hmm.generate_emission_syllables(10, syllable_dict, start2,                                                        stresses = stresses, desired_stresses = [x for x in wanted_stress])[0]
        if verbose:
            print(wanted_stress)
        rhyming_lines.append((" ".join([index2token[x] for x in line1[::-1]]),
                          " ".join([index2token[x] for x in line2[::-1]])))
    sonnet = "\n".join([upper_first(rhyming_lines[0][0])+ ",",
                    rhyming_lines[1][0]+ ".",
                    upper_first(rhyming_lines[0][1])+ ",",
                    rhyming_lines[1][1]+ ".",

                    upper_first(rhyming_lines[2][0])+ ",",
                    rhyming_lines[3][0]+ ".",
                    upper_first(rhyming_lines[2][1])+ ",",
                    rhyming_lines[3][1]+ ".",

                    upper_first(rhyming_lines[4][0])+ ",",
                    rhyming_lines[5][0]+ ".",
                    upper_first(rhyming_lines[4][1])+ ",",
                    rhyming_lines[5][1]+ ".",

                    upper_first(rhyming_lines[6][0])+ ",",
                    rhyming_lines[6][1]+ "."
                    ])
    if give_hmm:
        return (reversed_hmm, sonnet)
    else:
        return sonnet

if __name__ == "__main__":
    desc = "Creates a Shakespearean sonnet using a Hidden Markov Model"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-v", "--verbose", dest="verb",
                        action="store_true",
                        help="output debugging information")
    parser.add_argument("--num_states", dest="n_states",
                        default = "15",
                        help="number of hidden states to use")
    parser.add_argument("-s", dest="seed",
                        default=None,
                        help="specify random seed")
    args = parser.parse_args()

    if args.seed is not None:
        random_seed = args.seed
    else:
        # pick a random seed to print it at the end
        random_seed = random.randint(0, 9999999)
    random.seed(random_seed)
    sonnet = do_hmm(num_states = int(args.n_states),
                    verbose = args.verb, give_hmm = False)
    print(sonnet)
    print("\nRandom seed used: %s" % str(random_seed))