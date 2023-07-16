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


