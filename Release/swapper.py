import re

with open("data/Syllable_dictionary.txt") as f, \
        open("data/Syllable_dictionary_updated.txt", 'w') as g:
    for line in f:
        match = re.match("(.*) E?(\d+) (\d+)", line)
        if match:
            g.write("{} {} {}\n".format(match.group(1), match.group(3),
                match.group(2)))
        else:
            match = re.match("^(.*) (\d+)$", line)
            g.write("{} {} {}\n".format(match.group(1), match.group(2),
                match.group(2)))

with open("data/Syllable_dictionary_updated.txt") as g:
    for line in g:
        assert(re.match(".* .* E.*", line) or re.match(".* .*", line))
