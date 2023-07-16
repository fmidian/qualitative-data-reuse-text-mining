import nltk
import pickle
import json
import numpy as np
import collections


with open("interviews_for_n_grams.txt", "rb") as fp:   # Unpickling
    interviews_from_prepr_example = pickle.load(fp)


interviews_array = []
interviews = []

for interview in interviews_from_prepr_example:
    interview_words = []
    interview_words_array = []
    for segment in interview:
        # if "yesyes" in segment["list_of_words"]:
        #     print("heather found")
        #     print(segment["list_of_words"])
        interview_words_array.extend(np.array(segment["list_of_words"]))
        interview_words.extend(segment["list_of_words"])
    interviews_array.append(interview_words_array)
    interviews.append(interview_words)

print(len(interviews))    

# frequence of words per interview
for interview in interviews:
    counts = collections.Counter(interview)
    print(counts.most_common(5))
    
# save frequencies per interview
with open("output_frequencies_per_interview.txt", "w") as print_file:
       for interview in interviews:
        counts = collections.Counter(interview)
        print(counts.most_common(10), file=print_file)



#absolute frequency on whole corpus

interviews_onelist = [interview for sublist in interviews for interview in sublist]

print(len(interviews_onelist))
counts = collections.Counter(interviews_onelist)
print(counts.most_common(100))

# save frequencies from whole corpus absolute
with open("output_frequencies_whole_corpus_absolute.txt", "w") as print_file:
        counts = collections.Counter(interviews_onelist)
        print(counts.most_common(100), file=print_file)



import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim import models
import json
import numpy as np
import pickle


with open("list_of_interviews_after_preprocessing_example.txt", "rb") as fp:   # Unpickling
    interviews_from_prepr = pickle.load(fp)



interviews_array = []
interviews = []

for interview in interviews_from_prepr_example:
    interview_words = []
    interview_words_array = []
    for segment in interview:
        # if "yesyes" in segment["list_of_words"]:
        #     print("heather found")
        #     print(segment["list_of_words"])
        interview_words_array.extend(np.array(segment["list_of_words"]))
        interview_words.extend(segment["list_of_words"])
    interviews_array.append(interview_words_array)
    interviews.append(interview_words)


print(len(interviews))

interviews_onelist = [interview for sublist in interviews for interview in sublist]

id2word = corpora.Dictionary(interviews_onelist)
print("dictionary created")

corpus = []
counter = 1
for text in interviews:
    print("part ", counter, "of ", len(interviews))
    counter+=1
    new = id2word.doc2bow(text)
    # id_words = [[(id2word[id], count) for id, count in line] for line in new]
    # for line in new:
    #     print(id2word[line[0]], " Trenner ", id2word[0], " Trenner ", id2word[1])
    #     print(" ")
    #     print("Neues Wort ")
    #     print(" ")
    # print(" ")
    # print("neues Interview")
    # print(" ")
    # print(id_words)
    corpus.append(new)
# print(id2word)

tfidf = models.TfidfModel(corpus, smartirs='ntc')
counter = 0

with open('tdifd_with_numbers_interviews.txt', "w") as print_file:
    for doc in tfidf[corpus]:
        counter+=1
        print("Interview", counter,[[id2word[id], np.around(freq, decimals=2)]for id, freq in doc], file=print_file)
             
tfidf.sort(key=lambda x: x[1])