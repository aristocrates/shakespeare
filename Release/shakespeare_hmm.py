import HMM
from preprocessor import read_from_file

sonnets = read_from_file()
lines = []
for sonnet in sonnets:
    lines += sonnet
hmm = HMM.unsupervised_HMM(lines, 10, 1000)
print(hmm.generate_emission(10))

