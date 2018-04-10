import os
import sys
import contextlib
import random
import pickle


@contextlib.contextmanager
def smart_open(opening=None, mode=None):
    if mode == "w" or mode == "wb":
        if opening:
            fh = open(opening, mode)
        else:
            fh = sys.stdout
    elif mode == "r" or mode == "rb":
        if opening and opening != 'stdin':
            try:
                files = os.listdir(opening)
                for i in range(len(files)):
                    files[i] = open("{}\\{}".format(opening, files[i]), mode)
                fh = files
            except NotADirectoryError:
                fh = open(opening, mode)
        else:
            fh = sys.stdin
    else:
        raise Exception
    try:
        yield fh
    finally:
        if type(fh) == list:
            for file in fh:
                file.close()
        elif fh != sys.stdin and fh != sys.stdout:
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


def all_files_generator(files):
    for file in files:
        for line in file:
            yield line


def dump_dictionary(model, words):
    with smart_open(model, "wb") as fout:
        pickle.dump(words, fout)


def load_dictionary(model):
    with smart_open(model, "rb") as file:
        return pickle.load(file)
