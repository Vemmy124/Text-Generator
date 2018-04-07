import argparse
import pickle
import random
import contextlib
import sys


class Generator:
    words = dict()
    text = []

    def load_words(self, file):
        with open(args.model, "rb") as file:
            self.words = pickle.load(file)

    def set_seed(self, seed):
        if not seed:
            try:
                self.word = random.choice(list(self.words.keys()))
            except Exception:
                print("Dictionary not initialized")
                raise IndexError
        else:
            self.word = seed

    def build_text(self, length):
        for i in range(length):
            self.text.append(self.word)
            nextwords = []
            if not self.words.get(self.word):
                self.word = random.choice(list(self.words.keys()))
            else:
                self.word = weighted_choice(self.words)

    def print_text(self, output):
        with smart_open(output) as fout:
            for word in self.text:
                fout.write('{} '.format(word))


@contextlib.contextmanager
def smart_open(filename=None):
    if filename:
        fh = open(filename, 'w')
    else:
        fh = sys.stdout
    try:
        yield fh
    finally:
        if fh != sys.stdout:
            fh.close()


def summary_length(lst):
    length = 0
    for item in lst:
        length += len(item)
    return length


def weighted_choice(dictionary):
    rnd = random.random() * summary_length(dictionary.values())
    for key, value in dictionary.items():
        rnd -= len(value)
        if rnd < 0:
            return key


parser = argparse.ArgumentParser(description='A script which generates text from model')
parser.add_argument('--model',
                    required=True,
                    type=str,
                    help='Path to model file')
parser.add_argument('--seed',
                    type=str,
                    help='First word of generated sequence')
parser.add_argument('--length',
                    required=True,
                    type=int,
                    help='Length of generated sequence')
parser.add_argument('--output',
                    type=str,
                    help='Save file')
args = parser.parse_args()

if __name__ == '__main__':
    g = Generator()
    g.load_words(args.model)
    g.set_seed(args.seed)
    g.build_text(args.length)
    g.print_text(args.output)
