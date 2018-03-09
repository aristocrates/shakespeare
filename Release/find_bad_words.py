import preprocessor
import re

with open("data/shakespeare.txt") as f:
    tokens = preprocessor.all_tokens()
    for line in f:
        words = line.split(" ")
        for word in words:
            if re.match("^\d+$", word):
                continue
            if word.strip() != "" and word.lower() not in tokens:
                matches = re.match("^([^a-zA-Z]*)([a-zA-Z]*)([^a-zA-Z]*)$", word.strip())
                if not matches:
                    print(word)
                    continue
                if (matches.group(1) != "" and matches.group(3) != "") or matches.group(2).lower() not in tokens:
                    print(word)
                    print(matches.group(2))
