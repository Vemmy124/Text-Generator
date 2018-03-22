import argparse
import os
from sys import stdin

def Parse(text, info, words):
    newline = ''
    for x in text:
        if x.isalpha() or x == ' ' or (x == '-' and newline[-1].isalpha()):
            if info.lc:
                x = x.lower()
            newline += x
    newline = newline.split()
    for i in range(1, len(newline)):
        if not words.get(newline[i - 1]):
            words[newline[i - 1]] = {newline[i]: 1}
        elif not words[newline[i - 1]].get(newline[i]):
            words[newline[i - 1]][newline[i]] = 1
        else:
            words[newline[i - 1]][newline[i]] += 1

parser = argparse.ArgumentParser(description = 'A script which collects words from file')
parser.add_argument('--input-dir', dest = 'directory', type = str, default = 'stdin', help = 'File directory' )
parser.add_argument('--model', type = str, help = 'Save file' )
parser.add_argument('--lc', action = 'store_true', help = 'Switch to lowercase' )
args = parser.parse_args()
d = {}
if args.directory == 'stdin':
    for line in stdin:
        Parse(line, args, d)
else:
    files = os.listdir(args.directory)
    for file in files:
        if len(file) < 5 or file[-4:] != '.txt':
            raise Exception
        with open(args.directory + '\\' +file) as file:
            for line in file:
                Parse(line, args, d)
with open(args.model, "w") as newfile:
    for key in d.keys():
        newfile.write(key + " ")
        for value in d[key]:
            newfile.write(value + "_" + str(d[key][value]) + " ")
        newfile.write("\n")