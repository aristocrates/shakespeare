import re
with open("Syllable_dictionary_updated.txt") as f, open("Syllable_dictionary_updated2.txt", "w") as g:
    for line in f:
        match = re.match("^(.+) (\d+) (\d+)$", line)
        word = match.group(1)
        syll = int(match.group(2))
        end_syll = int(match.group(3))
        g.write("{} {} {}\n".format(word, syll, end_syll))
        g.write("\"the {}\" {} {}\n".format(word, syll + 1, end_syll  + 1))
        g.write("\"a {}\" {} {}\n".format(word, syll + 1, end_syll + 1))
