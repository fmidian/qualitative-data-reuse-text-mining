import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim import models
import numpy as np
import pickle
import spacy


def calculate_similarity_score(words):
    """
    Calculate the similarity score between a list of words.
    """
    total_score = 0.0
    pair_count = 0

    for i in range(len(words)):
        word1 = words[i]
        for j in range(i + 1, len(words)):
            word2 = words[j]
            token1 = nlp(word1)
            token2 = nlp(word2)
            
            if token1.has_vector and token2.has_vector:
                similarity = token1.similarity(token2)
            else:
                continue

            total_score += similarity
            pair_count += 1

    if pair_count > 0:
        average_score = total_score / pair_count
    else:
        average_score = 0.0

    print(words)
    print(average_score)

    return average_score


# Example usage
print("Similarity test")

with open("interviews_for_n_grams.txt", "rb") as fp:
    # Load interviews data from a pickled file
    interviews_from_prepr = pickle.load(fp)

interviews = []
for interview in interviews_from_prepr:
    interview_words = []
    for segment in interview:
        interview_words.extend(segment["list_of_words"])
    interviews.append(interview_words)

print("Number of interviews:", len(interviews))
print("Number of words in the first three interviews:", len(interviews[0]), len(interviews[1]), len(interviews[2]))

dct = corpora.Dictionary(interviews)
print("Dictionary created")

corpus = [dct.doc2bow(line) for line in interviews]  # Convert corpus to BoW format
tfidf = models.TfidfModel(corpus)
print(tfidf)
vector = tfidf[corpus]  # Apply model to the corpus
counter = 0
output = ""
words_with_similarity = []
nlp = spacy.load("en_core_web_lg")

for doc in vector:
    counter += 1
    doc.sort(key=lambda x: x[1], reverse=True)
    doc_with_interview = [(id, dct[id], np.around(freq, decimals=2), "Interview " + str(interview)) for id, freq in doc]
    
    try:
        # Calculate similarity scores for the current document
        words = [word for id, word, freq, interview in doc_with_interview][:10]
        similarity_score = calculate_similarity_score(words)
        output = "Interview " + str(counter) + str([[dct[id], np.around(freq, decimals=2)] for id, freq in doc][:10])

        words_with_similarity.append((output, similarity_score))
    
    finally:
        # Clear unnecessary objects to free up memory
        del words
        del doc_with_interview

words_with_similarity.sort(key=lambda x: x[1], reverse=True)
for x in words_with_similarity:
    print(x[0])
    print(x[1])
    print("\n\n\n\n")