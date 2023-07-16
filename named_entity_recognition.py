import nltk
from nltk import bigrams
from nltk import trigrams
import pickle


with open("list_of_interviews_after_preprocessing_example.txt", "rb") as fp:   # Unpickling
    interviews_from_prepr = pickle.load(fp)


interviews = []

#When we use whole interviews
for interview in interviews_from_prepr:
     interview_words = []
     interview_words_array = []
     for segment in interview:
         interview_words.extend(segment["list_of_not_lemmatized_words"])
     interviews.append(interview_words)