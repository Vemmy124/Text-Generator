import argparse
import pickle
import random
import utils
import sys


class Generator:
    words = dict()
    text = []

    def load_words(self, file):
        self.words = utils.load_dictionary(file)

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
                self.word = utils.weighted_choice(self.words)

    def print_text(self, output):
        with utils.smart_open(output, "w") as fout:
            for word in self.text:
                fout.write('{} '.format(word))


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
