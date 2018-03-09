import preprocessor
import json

sonnets = preprocessor.load_sonnets()
used_tokens = set()
tokenized_sonnets = []
for sonnet in sonnets:
    tokenized_lines = []
    for line in sonnet:
        tokenized_lines.append(preprocessor.tokenize_line(line))
        used_tokens = used_tokens.union(set(tokenized_lines[-1]))
    tokenized_sonnets.append(tokenized_lines)

token2index = {token : i for i, token in enumerate(used_tokens)}
index2token = {i : token for i, token in enumerate(used_tokens)}
with open("data/token_dict_unpunctuated.json", "w") as f:
    json.dump(index2token, f)

indices_sonnets = [[[token2index[token] for token in line] for line in sonnet] for sonnet in tokenized_sonnets]
with open("data/tokenized_sonnets_unpunctuated.txt", "w") as f:
    for sonnet in indices_sonnets:
        for line in sonnet:
            f.write(" ".join([str(x) for x in line]) + "\n")
        f.write("\n\n")

