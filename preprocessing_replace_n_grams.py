from preprocessing_functions import replace_n_grams 
import pickle
import json

with open("interviews_for_n_grams.txt", "rb") as fp:   # Unpickling
    interviews = pickle.load(fp)

interviews = replace_n_grams(interviews)

for interview in interviews:
    for segment in interview:
        segment["list_of_words"] = [x for x in segment["list_of_words"] if not "\ufffd" in x]
        segment["list_of_not_lemmatized_words"] = [x for x in segment["list_of_not_lemmatized_words"] if not "\ufffd" in x]



with open("interviews_after_n_grams.json", "w", encoding="utf-8") as fp:
    json.dump(interviews, fp, indent = 2)
with open("interviews_after_n_grams.txt", "wb") as fp:   #Pickling
    pickle.dump(interviews, fp)