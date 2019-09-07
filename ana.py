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
import pyjarowinkler
from pyjarowinkler import distance

'''
@author: xhhan1@student.unimelb.edu.au
Use different string match methods to interpret the candidate blend words.
Evaluate the result from the real blend txt file.

Please forgive me to duplicate some of these methods. 
'''


def has_many_duplicate(word):
    # return true if word has a sequence of
    # more than 2 consecutive identical letters and flase otherwise
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


# Use jaro-winkler method to interpret the candidate blend words
def predict_blends_global(test_list, dic_list):
    result = []
    count = 0
    recount = 0
    for t in test_list:
        for d in dic_list:
            if t[0] == d[0]:
                if distance.get_jaro_distance(t, d, winkler=True, scaling=0.1) > 0.9\
                        and ed.eval(t, d) > 1:
                    count = count + 1
            elif t[-1] == d[-1]:
                if distance.get_jaro_distance(t, d, winkler=True, scaling=0.1) > 0.9\
                        and ed.eval(t, d) > 1:
                    recount = recount + 1

            if count > 0 and recount > 0:
                result.append(t)
                break
        count = 0
        recount = 0

    return result


# Use ngram(2,3,4...) method to interpret the candidate blend words
def predict_blends_ngram(test_list, dic_list, n):
    result = []
    count = 0
    recount = 0
    for t in test_list:
        for d in dic_list:
            if t[0] == d[0]:
                if ngram_test(t, d, n) > 0.5 and ed.eval(t, d) > 1:
                    count = count + 1
            elif t[-1] == d[-1]:
                if ngram_test(t, d, n) > 0.5 and ed.eval(t, d) > 1:
                    recount = recount + 1

            if count > 0 and recount > 0:
                result.append(t)
                break
        count = 0
        recount = 0

    return result


# calculate the result from the real blend words txt
def calculate_result(result, blends):
    count = 0
    for word in result:
        if word in blends:
            count = count + 1
    return count / len(result)


candidate, dic, blends = process_date()
clean_candidate, clean_dic = clean_data_set(candidate, dic)


#result = predict_blends_global(clean_candidate, clean_dic)
result1 = predict_blends_ngram(clean_candidate, clean_dic, 3)
#print(result)
print(result1)
#print(calculate_result(result, blends))
print(calculate_result(result1, blends))


# ngram > 0.5  0.0135  3gram > 0.5 0.01
# jw > 0.7 0.011 >0.8 0.0114 > 0.9  0.01224