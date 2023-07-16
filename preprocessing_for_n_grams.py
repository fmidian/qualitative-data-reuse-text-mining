from preprocessing_functions import read_files_and_remove_metadata
from preprocessing_functions import remove_speakers_and_meta_content_in_transcript_itself
from preprocessing_functions import remove_punctuation_and_stopwords
from preprocessing_functions import add_lists_of_words_and_remove_list_of_tokens
import pickle
import json

interviews = read_files_and_remove_metadata(56) #56
interviews = remove_speakers_and_meta_content_in_transcript_itself(interviews)
interviews = remove_punctuation_and_stopwords(interviews)
interviews = add_lists_of_words_and_remove_list_of_tokens(interviews)

with open("interviews_for_n_grams.json", "w", encoding="utf-8") as fp:
    json.dump(interviews, fp, indent = 2)
with open("interviews_for_n_grams.txt", "wb") as fp:   #Pickling
    pickle.dump(interviews, fp)