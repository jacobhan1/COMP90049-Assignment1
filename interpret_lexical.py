import cProfile
import pickle
import re
import nltk
import editdistance as ed
# Levenshtein/global edit distance, sourced from github.com/aflc/editdistance
import os.path
import multiprocessing as mp
from functools import partial
from ngram import NGram
import distance
import time
import pyjarowinkler
from pyjarowinkler import distance

'''
@author: xhhan1@student.unimelb.edu.au
Use different string match methods to interpret the candidate blend words.
Evaluate the result from the real blend txt file.
 
'''


def has_many_duplicate(word):
    # return true if word has a sequence of
    # more than 2 consecutive identical letters and flase otherwise
    return re.search("([a-zA-Z])\\1{2,}", word)


# For nox suffixes are common inflectional suffixes for nouns and verbs
suffixes = ['s', 'ed', 'ing', 'en', 'ed']


def is_morpho_suffix(s):
    return s in suffixes


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


# ngram test method
def ngram_test(w1, w2, n):
    return NGram.compare(w1, w2, N=n)


# clean data from the data file
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
            if len(c) > 4:
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


# process data from the candidate, dict and blends from the source file.
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


# Use ngram(2,3,4...) method to interpret the candidate blend words
def predict_blends_ngram(test_list, dic_list, n):
    result = []
    count = 0
    recount = 0
    for t in test_list:
        word_stem = stemmer.stem(t)
        for d in dic_list:
            if len(longest_common_prefix(t, d)) >= 2 and word_stem == stemmer.stem(d):
                if ngram_test(t, d, n) > 0.3 and ed.eval(t, d) > 1:
                    count = count + 1
            elif len(longest_common_suffix(t, d)) >= 2:
                if is_morpho_suffix(longest_common_suffix(t, d)):
                    break
                else:
                    if ngram_test(t, d, n) > 0.3 and ed.eval(t, d) > 1:
                        recount = recount + 1

            if count > 0 and recount > 0:
                result.append(t)
                break
        count = 0
        recount = 0

    return result


# calculate the result from the real blend words txt
def calculate_result(result, blends, candidate):
    count = 0
    true_blend = 0
    for c in candidate:
        if c in blends:
            true_blend += 1
    for word in result:
        if word in blends:
            count = count + 1
    recall = count / true_blend
    precision = count / len(result)
    return recall, precision



stemmer = nltk.stem.PorterStemmer()
candidate, dic, blends = process_date()
clean_candidate, clean_dic = clean_data_set(candidate, dic)

result = predict_blends_ngram(clean_candidate, clean_dic, 2)
result1 = predict_blends_ngram(clean_candidate, clean_dic, 3)
print(result)
print(result1)
print(calculate_result(result, blends, candidate))
print(calculate_result(result1, blends, candidate))


# ngram > 0.5  0.0135  3gram > 0.5 0.01
# jw > 0.7 0.011 >0.8 0.0114 > 0.9  0.01224


# 改进后： 2gram > 0.5 0.0324  3gram > 0.3 recall: 12.90  precision: 3
# jav-wiklot > 0.7  0.02411  : 539
# > 0.8 0.0225 533