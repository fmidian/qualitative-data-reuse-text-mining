import json
import numpy as np
import pickle
from preprocessing_for_topic_modeling import preprocess_topic_modeling
import pandas
import dataframe_image
import openpyxl
import little_mallet_wrapper as mallet
from bs4 import BeautifulSoup
from datetime import datetime

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
#from gensim.models.wrappers import LdaMallet

#bigram = gensim.models.Phrases(data, min_count=20, threshold=100)

# with open("list_of_interviews_after_preprocessing.json", 'r',  encoding="utf-8") as f:
#     interviews_from_prepr = json.load(f)

# test1 = "mother father family bear War live brother parent sister die" #good
# test2 = "school boy School girl child teacher age send parent year" #good
# test3 = "people way kind work like mean different sense idea find" #bad
# test4 = "people work time george interview sort like mean talk way" #bad
# test5 = "talk john back ground perspective differently personality broad 10th 1935" #bad

# x1 = "Party Labour politic political War Communist member Socialist Latin active"
# x2 = "interview people question datum survey qualitative ask research study material"
# x3 = "mother father child family live parent marry bear brother house"
# x4 = "service Marx economy Marxism production buy Marxist food good produce"
# x5 = "event depression difference rate disorder psychiatrist patient increase autonomy anxiety"

# tests = [test1, test2, test3, test4, test5]
# tests2 = [x1, x2, x3, x4, x5]
# models = [tests, tests2]

def load_data(number_of_words_in_unit, onlyInterviewee, full_text):
        preprocess_topic_modeling(number_of_words_in_unit, onlyInterviewee)
        print("topic modeling for number of words ", number_of_words_in_unit)
        with open("interviews_for_topic_modeling.txt", "rb") as fp:   # Unpickling
            interviews_from_prepr = pickle.load(fp)

        segments = []

        for interview in interviews_from_prepr:
            for segment in interview:
                if full_text:
                    segments.append((segment["continuous_text"], segment["interview_number"]))
                else:
                    segments.append(" ".join(segment["list_of_words"]))
                    #mallet.print_dataset_stats(segments)

        print(len(segments))
        print("ready")
        return segments

def train_topic_model():
    evaluate_table = []
    bool_values = [False, True] #False, True

    break_count = 0

    #remember to not contain whitespaces in your path, that will create problems
    #see: https://stackoverflow.com/questions/57895899/how-do-i-pass-a-file-path-containing-spaces-to-the-gensim-lda-mallet-wrapper
    path_to_mallet = r"C:/mallet-2.0.8/bin/mallet" #r
    output_directory_path = r"C:/mallet_output"

    path_to_training_data           = output_directory_path + '/training.txt'
    path_to_formatted_training_data = output_directory_path + '/mallet.training'

    bad_topics = []

    for onlyInterviewee in bool_values:
        if(break_count == 1):
            break
        for number_of_words_in_unit in range(10, 20, 10):
            if(break_count == 1):
                break
            
            segments = load_data(number_of_words_in_unit, onlyInterviewee, False)

            number_of_topics_origin = int(236*pow(number_of_words_in_unit*3, -0.267))
            #see https://doi.org/10.1007/s11135-020-00976-w
            #mal 3, da schon gesäuberte Daten verwendet werden (stopwords)

            for number_of_topics in [number_of_topics_origin, int(number_of_topics_origin*3/4), int(number_of_topics_origin/2)]:
                
                if(break_count == 1):
                    break

                path_to_model                   = output_directory_path + '/mallet.model.nrtopics' + str(number_of_topics)+'.segment'+str(number_of_words_in_unit)+'.onlyInterviewee'+str(onlyInterviewee)
                path_to_topic_keys              = output_directory_path + '/mallet.topic_keys.nrtopics' + str(number_of_topics)+'.segment'+str(number_of_words_in_unit)+'.onlyInterviewee'+str(onlyInterviewee)
                path_to_topic_distributions     = output_directory_path + '/mallet.topic_distributions.nrtopics' + str(number_of_topics)+'.segment'+str(number_of_words_in_unit)+'.onlyInterviewee'+str(onlyInterviewee)
                path_to_word_weights            = output_directory_path + '/mallet.word_weights.nrtopics' + str(number_of_topics)+'.segment'+str(number_of_words_in_unit)+'.onlyInterviewee'+str(onlyInterviewee)
                path_to_diagnostics             = output_directory_path + '/mallet.diagnostics.nrtopics' + str(number_of_topics)+'.segment'+str(number_of_words_in_unit)+'.onlyInterviewee'+str(onlyInterviewee) + '.xml'
                
                mallet.import_data(path_to_mallet,
                    path_to_training_data,
                    path_to_formatted_training_data,
                    segments)

                mallet.train_topic_model(path_to_mallet,
                        path_to_formatted_training_data,
                        path_to_model,
                        path_to_topic_keys,
                        path_to_topic_distributions,
                        path_to_word_weights,
                        path_to_diagnostics,
                        number_of_topics)

                print("number of topics: ", number_of_topics)

                topic_keys = mallet.load_topic_keys(output_directory_path + '/mallet.topic_keys.nrtopics' + str(number_of_topics)+'.segment'+str(number_of_words_in_unit)+'.onlyInterviewee'+str(onlyInterviewee))
                # for i, t in enumerate(topic_keys[:5]):
                #     print(i, '\t', ' '.join(t[:10]))

                #testing
                topic_distributions = mallet.load_topic_distributions(output_directory_path + '/mallet.topic_distributions.nrtopics' + str(number_of_topics)+'.segment'+str(number_of_words_in_unit)+'.onlyInterviewee'+str(onlyInterviewee))
                assert(len(topic_distributions) == len(segments))

                topic_word_probability_dict = mallet.load_topic_word_distributions(output_directory_path + '/mallet.word_weights.nrtopics' + str(number_of_topics)+'.segment'+str(number_of_words_in_unit)+'.onlyInterviewee'+str(onlyInterviewee))
                for _topic, _word_probability_dict in topic_word_probability_dict.items():
                    print('Topic', _topic)
                    for _word, _probability in sorted(_word_probability_dict.items(), key=lambda x: x[1], reverse=True)[:5]:
                        print(round(_probability, 4), '\t', _word)
                        print()

                with open(output_directory_path + '/mallet.diagnostics.nrtopics' + str(number_of_topics)+'.segment'+str(number_of_words_in_unit)+'.onlyInterviewee'+str(onlyInterviewee) + '.xml', 'r') as f:
                    diagnostics = f.read()
                
                # Passing the stored data inside
                # the beautifulsoup parser, storing
                # the returned object
                Bs_data = BeautifulSoup(diagnostics, "xml")
                
                # Finding all instances of tag topic
                topics_diag = Bs_data.find_all('topic')
                print("diagnostics")
                print(len(topics_diag))
                print(topics_diag[0])
                print(topics_diag)

                coherence = 0
                word_length = 0
                uniform_dist = 0
                corpus_dist = 0
                rank_one_docs = 0
                exclusivity = 0

                assert(len(topics_diag) == number_of_topics)
                number_of_bad_topics = 0

                for topic_diag in topics_diag:
                    number_of_bad_categories = 0
                    coherence += float(topic_diag["coherence"])
                    if float(topic_diag["coherence"]) < -550:
                        number_of_bad_categories += 1
                    word_length += float(topic_diag["word-length"])
                    if float(topic_diag["word-length"]) < 5.5:
                        number_of_bad_categories += 1
                    uniform_dist += float(topic_diag["uniform_dist"])
                    if float(topic_diag["uniform_dist"]) < 4:
                        number_of_bad_categories += 1
                    corpus_dist += float(topic_diag["corpus_dist"])
                    if float(topic_diag["corpus_dist"]) < 2:
                        number_of_bad_categories += 1
                    rank_one_docs += float(topic_diag["rank_1_docs"])
                    if float(topic_diag["rank_1_docs"]) < 0.04:
                        #bad topic
                        number_of_bad_categories += 1
                    exclusivity += float(topic_diag["exclusivity"])   
                    if float(topic_diag["exclusivity"]) < 0.3:
                        number_of_bad_categories += 1
                            
                    if number_of_bad_categories > 1:
                        bad_topics.append(topic_word_probability_dict[int(topic_diag["id"])])
                        number_of_bad_topics += 1

                coherence /= number_of_topics #should be high
                word_length /= number_of_topics #should be high
                uniform_dist /= number_of_topics #should be high
                corpus_dist /= number_of_topics #should be high
                rank_one_docs /= number_of_topics #should be high
                exclusivity /= number_of_topics #should be high

                print("coherence", coherence)
                print("word length", word_length)
                print("uniform_dist", uniform_dist)
                print("corpus_dist", corpus_dist)
                print("rank_one_docs", rank_one_docs)
                print("exclusivity", exclusivity)

                print("current number of identified bad topics", len(bad_topics))

                #score = coherence/1000 + word_length/10 + uniform_dist/5 + corpus_dist/10 + rank_one_docs*10 + exclusivity
                proportion_bad_topics = number_of_bad_topics / number_of_topics
                mean_num_words = int(np.mean([len(d.split()) for d in segments]))

                evaluate_table.append([mean_num_words, number_of_topics, onlyInterviewee, coherence, word_length, uniform_dist, corpus_dist, rank_one_docs, exclusivity, proportion_bad_topics])
                df = pandas.DataFrame(evaluate_table, columns=["mean number of words in unit", "number of topics", "only interviewee", "coherence", "word_length", "uniform_dist", "corpus_dist", "rank_one_docs", "exclusivity", "proportion_bad_topics"])
                df.to_excel("evaluation.xlsx")

                #break_count += 1


    with open(r'bad_topics.txt', 'w') as fp:
        for item in bad_topics:
            fp.write("%s\n\n" % item)

    df = pandas.DataFrame(evaluate_table, columns=["number of words in unit", "number of topics", "only interviewee", "coherence", "word_length", "uniform_dist", "corpus_dist", "rank_one_docs", "exclusivity", "score"])
    df = df.sort_values(by=["score"], ascending=False)
    now = datetime.now()
    dataframe_image.export(df,"evaluation"+now.strftime("%m_%d_%M")+".png")
    df.to_excel("evaluation"+str(now)[:20]+".xlsx")

if __name__ == "__main__":
    with open("interviews_for_topic_modeling.txt", "rb") as fp:   # Unpickling
            interviews_from_prepr = pickle.load(fp)

    interview_number = 2
    segment_number = 10

    print("Interview ", interview_number)
    print(interviews_from_prepr[interview_number])
    # for interview in interviews_from_prepr:
    #     for segment in interview:
    #         if full_text:
    #             segments.append((segment["continuous_text"], segment["interview_number"]))
    #         else:
    #             segments.append(" ".join(segment["list_of_words"]))
    print("end")
    #train_topic_model()

            #mögliches todo (prio mittel) mit mallet topic modeling: Verlauf im Durchschnitt innheralb eines Interviews der Topics
            #mögliches todo (prio niedrig) mit mallet topic modeling: label interviewer interviewee ausnutzen und unterschiede in den topics anzeigen
            
            #Vorschlag topic coherence
            # lda_coherence = CoherenceModel(topics=ldatopics, texts=texts, dictionary=dictionary, window_size=10)
            #-> weiter recherchieren

            #todo ldavis Visualisierung
            # pyLDAvis.enable_notebook()
            #vis = gensimvis.prepare(lda_model, corpus, id2word, mds="mmds", R=30)
            # print(vis)
            #pyLDAvis.save_html(vis, "lda_"+str(number_of_topics)+"topics_"+str(number_of_words_in_unit)+"number_of_words_in_unit_"+str(onlyInterviewee)+"onlyInterviewee.html")


#             #evaluate model
#             model_score_similarity = 0
#             model_score_frequent_meaningless = 0
#             model_score_overall = 0
#             i = 1
#             words_set = set()
#             for topic in model:
#                 word_list = []
#                 for x in topic[1]:
#                     word_list.append(x[0])
#                     words_set.add(x[0])
#                 # print(word_list)
#                 #print("test ", i)
#                 tokens = nlp(" ".join(word_list))
#                 similarity_score = 0
#                 frequent_meaningless_score = 0
#                 number_of_same_words = 0
#                 for token1 in tokens:
#                     if token1.lemma_ == "Vice" or token1.lemma_ == "Vice Chancellor":
#                         print("############################ detected ##################")
#                         print(token1.lemma_)
#                     for token2 in tokens:
#                         similarity_score += token1.similarity(token2)
#                         #print(token1.text, token2.text, token1.similarity(token2))
#                     if token1.lemma_ in frequent_meaningless:
#                         frequent_meaningless_score -= 2
#                 model_score_similarity += similarity_score
#                 model_score_frequent_meaningless += frequent_meaningless_score
#                 if similarity_score + frequent_meaningless_score > 0:
#                     model_score_overall += pow(similarity_score + frequent_meaningless_score, 2)
#                 else:
#                     model_score_overall -= pow(similarity_score + frequent_meaningless_score, 2)
#                 # print("similarity_score ", similarity_score)
#                 # print("frequent meaningless score ", frequent_meaningless_score)
#                 # print("overall score ", similarity_score + frequent_meaningless_score)
#                 i += 1
#             model_score_similarity /= float(number_of_topics)
#             model_score_frequent_meaningless /= float(number_of_topics)
#             model_score_overall /= float(number_of_topics)
            
#             number_double_words = (number_of_topics*10 - len(words_set))/number_of_topics
#             model_score_overall -= 25*number_double_words
#             print("number double words ", number_double_words)
#             print("similarity_score ", model_score_similarity)
#             print("frequent meaningless score ", model_score_frequent_meaningless)
#             print("overall score ", model_score_overall)

#             evaluate_table.append([number_of_words_in_unit, number_of_topics, onlyInterviewee, model_score_similarity, model_score_frequent_meaningless, number_double_words, model_score_overall])

# df = pandas.DataFrame(evaluate_table, columns=["number of words in unit", "number of topics", "only interviewee", "similarity_score", "frequent meaningless score ", "number of double words", "overall score "])
# dataframe_image.export(df,"evaluation.png")
# df.to_excel("evaluation.xlsx")

