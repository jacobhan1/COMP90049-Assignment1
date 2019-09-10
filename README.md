# COMP90049-Assignment1
COMP90049 Knowledge Technologies assignment

I use several external package to help me to interpret the lexical words:

ngram package( Available at: https://github.com/gpoulter/python-ngram), 

editdistance package(Available at: https://github.com/aflc/editdistance), 

nltk package(Available at: http://www.nltk.org/), 

How to use our program to interpret and evaluate the result:

Step1: process_date() to change the candidate, dic and blends files to the list

Step2: clean the data. Using clean_data_set(candidate, dic), we clean the duplicate characters words and length less than 4

Step3: interpret the data. Using predict_blends_ngram(clean_candidate, clean_dic, 2) or predict_blends_ngram(clean_candidate, clean_dic, 3)

The method will return a list of predicted blend words.

Step4: print the method: Calculate_result(result, blends, candidate) to see the precision and recall result.
