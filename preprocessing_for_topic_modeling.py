import pickle
import json 
from preprocessing_functions import change_analysis_units_to_number_of_words
from preprocessing_functions import change_to_segments_of_interviewee

def preprocess_topic_modeling(number_of_words_in_unit, use_only_interviewee):
    with open("interviews_after_n_grams.txt", "rb") as fp:   # Unpickling
        interviews = pickle.load(fp)
    if use_only_interviewee:
        interviews = change_to_segments_of_interviewee(interviews)
    interviews = change_analysis_units_to_number_of_words(number_of_words_in_unit, interviews)

    with open("interviews_for_topic_modeling.json", "w", encoding="utf-8") as fp:
        json.dump(interviews, fp, indent = 2)
    with open("interviews_for_topic_modeling.txt", "wb") as fp:   #Pickling
        pickle.dump(interviews, fp)