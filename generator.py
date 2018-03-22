import argparse
import random

parser = argparse.ArgumentParser(description = 'A script which generates text from model')
parser.add_argument('--model', type = str, help = 'Path to model file')
parser.add_argument('--seed', type = str, default = 'None', help = 'First word of generated sequence')
parser.add_argument('--length', type = int, help = 'Length of generated sequence')
parser.add_argument('--output', type = str, help = 'Save file' )
args = parser.parse_args()

d = {}
with open(args.model) as file:
    for line in file:
        line = line.split()
        key = line[0]
        for wordfreq in line[1:]:
            word, freq = wordfreq.split('_')
            if not d.get(key):
                d[key] = {word: int(freq)}
            else:
                d[key][word] = int(freq)
if args.seed == 'None':
    word = random.choice(list(d.keys()))
else:
    word = args.seed
text = []
for i in range(args.length):
    if args.output:
        text.append(word)
    else:
        print(word, end=' ')
    nextwords = []
    if not d.get(word):
        word = random.choice(list(d.keys()))
    else:
        for key in d[word]:
            for j in range(d[word][key]):
                nextwords.append(key)
        word = random.choice(nextwords)
if args.output:
    with open(args.output) as output:
        for word in text:
            output.write(word + ' ')
    