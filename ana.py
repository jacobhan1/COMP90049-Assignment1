import cProfile
import pickle
import editdistance as ed
import os.path
import multiprocessing as mp
from functools import partial
import ngram
import distance
import time
import pyjarowinkler as jw
# Levenshtein/global edit distance, sourced from github.com/aflc/editdistance
print(ed.eval('banana', 'bahama'))


def process_date():
    with open("candidates.txt") as a:
        candidate = a.read().strip()
    with open("dict.txt") as b:
        dic = b.read().strip()
    with open("blends.txt") as c:
        for line in c:
            blends = line.strip().split()[0]

    return candidate, dic, blends


candidate, dic, blends = process_date()
