import argparse
import os
import pickle
import contextlib
import sys


class Parser:
    def init(self, line):
        self.line = line

    def preprocess(self, lc):
        newline = ''
        for x in self.line:
            if x.isalpha() or x == ' ' or (x == '-' and newline[-1].isalpha()):
                if lc:
                    x = x.lower()
                newline += x
        self.line = newline.split()

    def get_tokens(self, words):
        for i in range(1, len(self.line)):
            if not words.get(self.line[i - 1]):
                words[self.line[i - 1]] = {self.line[i]: 1}
            elif not words[self.line[i - 1]].get(self.line[i]):
                words[self.line[i - 1]][self.line[i]] = 1
            else:
                words[self.line[i - 1]][self.line[i]] += 1
        return words


@contextlib.contextmanager
def smart_open(directory=None):
    if directory and directory != 'stdin':
        files = os.listdir(directory)
        yield all_files_generator(directory, files)
    else:
        fh = sys.stdin
        yield fh

def all_files_generator(directory, files):
    for file in files:
        with open("{}\\{}".format(directory, file)) as fin:
            for line in fin:
                yield line

def dump_dictionary(model, words):
    with open(model, "wb") as fout:
        pickle.dump(words, fout)

parser = argparse.ArgumentParser(description='A script which collects words from file')
parser.add_argument('--input-dir',
                    dest='directory',
                    type=str,
                    default='stdin',
                    help='File directory')
parser.add_argument('--model',
                    required=True,
                    type=str,
                    help='Save file')
parser.add_argument('--lc',
                    action='store_true',
                    help='Switch to lowercase')
args = parser.parse_args()

if __name__ == '__main__':
    p = Parser()
    words = {}
    with smart_open(args.directory) as fin:
        for line in fin:
            p.init(line)
            p.preprocess(args.lc)
            p.get_tokens(words)
    dump_dictionary(args.model, words)
