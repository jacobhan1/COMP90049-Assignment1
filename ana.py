import cProfile
import pickle
import re
import editdistance as ed
# Levenshtein/global edit distance, sourced from github.com/aflc/editdistance
import os.path
import multiprocessing as mp
from functools import partial
from ngram import NGram
import distance
import time
import pyjarowinkler as jw


def has_many_duplicate(word):
    #return true if word has a sequence of
    #more than 2 consecutive identical letters and flase otherwise
    return re.search("([a-zA-Z])\\1{2,}", word)


def longest_common_prefix(w1, w2):
    x = 0
    while x < len(w1) and x < len(w2) and w1[x] == w2[x]:
        x += 1
    return w1[:x]


def longest_common_suffix(w1, w2):
    # Reverse w1 and w2 to find LCS using LCP
    w1 = ''.join(list(reversed(w1)))
    w2 = ''.join(list(reversed(w2)))
    lcp = longest_common_prefix(w1, w2)
    lcp = ''.join(list(reversed(lcp)))
    return lcp


def is_common_prefix(w1, w2):
    return w1[:2] == w2[:2]


def ngram_test(w1,w2,n):
    return NGram.compare(w1, w2, N=n)


def clean_data_set(candidate, dic):
    dic_clean = []
    candidate_clean = []
    # Restrictions on candidate blends:
    #
    # 1. Candidate blend must not have many repeated characters
    #
    # 2. Candidate blend must be at least 6 characters long (Short
    #    words are more likely to have a blend interpretation and then
    #    the number of candidates goes up a lot.)
    #
    for c in candidate:
        if not has_many_duplicate(c):
            if len(c) > 5:
                candidate_clean.append(c)
    # Restrictions on candidate blends:
    #
    # 1. dic have many repeated characters do not need to compare with candidate
    #
    # clean the dic, make faster search
    for d in dic:
        if not has_many_duplicate(d):
            dic_clean.append(d)
    return candidate_clean, dic_clean


def process_date():
    blend = []
    with open("candidates.txt") as a:
        candidate = a.read().strip().split()
    with open("dict.txt") as b:
        dic = b.read().strip().split()
    with open("blends.txt") as c:
        for line in c:
            blend.append(line.strip().split()[0])

    return candidate, dic, blend

def predict_blends(test_list, dic_list, method):
    prefix = []
    result = []
    for t in test_list:
        for d in dic_list:
            if len(longest_common_prefix(t,d)) >= 2:
                if ngram_test(t, d, 2) > 0.3:
                    prefix.append(t)
                    break
    for s in prefix:
        for d in dic_list:
            if len(longest_common_suffix(s,d)) >= 2:
                if ngram_test(s, d, 2) > 0.3:
                    result.append(s)
                    break
    return result


candidate, dic, blends = process_date()
clean_candidate, clean_dic = clean_data_set(candidate, dic)
print(predict_blends(clean_candidate, clean_dic, ""))