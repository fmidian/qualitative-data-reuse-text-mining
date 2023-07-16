import little_mallet_wrapper as mallet
from topic_modeling import load_data
import numpy

output_directory_path = r"C:/mallet_output"
number_of_topics = 59
number_of_words_in_unit = 20
onlyInterviewee = False
number_of_text_passages = 10

interested_topics = [11, 13, 21, 26, 31, 33, 36, 44, 45, 55, 56, 58]

topic_distributions = mallet.load_topic_distributions(output_directory_path + '/mallet.topic_distributions.nrtopics' + str(number_of_topics)+'.segment'+str(number_of_words_in_unit)+'.onlyInterviewee'+str(onlyInterviewee))
#print(topic_distributions)

topic_keys = mallet.load_topic_keys(output_directory_path + '/mallet.topic_keys.nrtopics' + str(number_of_topics)+'.segment'+str(number_of_words_in_unit)+'.onlyInterviewee'+str(onlyInterviewee))

topic_word_probability_dict = mallet.load_topic_word_distributions(output_directory_path + '/mallet.word_weights.nrtopics' + str(number_of_topics)+'.segment'+str(number_of_words_in_unit)+'.onlyInterviewee'+str(onlyInterviewee))
#for _topic, _word_probability_dict in topic_word_probability_dict.items():
    #print('Topic', _topic)
    #for _word, _probability in sorted(_word_probability_dict.items(), key=lambda x: x[1], reverse=True)[:5]:
        #print(round(_probability, 4), '\t', _word)
        #print()

segment_with_interview_number = load_data(number_of_words_in_unit, onlyInterviewee, True)
segments = [s for s, n in segment_with_interview_number]
assert(len(topic_distributions) == len(segments))

interview_numbers_list = ["interview "+str(n) for s, n in segment_with_interview_number]
assert(len(interview_numbers_list) == len(segments))

#mallet.plot_categories_by_topics_heatmap(interview_numbers_list, topic_distributions, topic_keys, output_directory_path+"/interviews_topics.pdf", dim=(number_of_topics, 56))
output = "Übersicht der "+str(number_of_text_passages)+" am höchsten gewichteten Textstellen für einige vorher identifizierte Topics für das 59-20-false Modell\n\n"
for interested_topic in interested_topics:
    top_docs = mallet.get_top_docs(segments, topic_distributions, interested_topic, number_of_text_passages)
    #print(top_docs)

    output += "topic number: "+str(interested_topic)+"\n"
    output += "topic word list: "+str(topic_keys[interested_topic])+"\n\n"
    list_of_segment_tuples = []

    for top_seg in top_docs:
        for text, number in segment_with_interview_number:
            if top_seg[1] == text:
                interview_number = number
                break
        list_of_segment_tuples.append((text, interview_number, top_seg[0]))
    for text, number, prob in sorted(list_of_segment_tuples, key=lambda x: x[1]):
        output+="\nsegment in interview "+str(number)+" with probability "+str(prob)+" for topic "+str(interested_topic)
        text = text.replace("\ufffd", "'")
        output+=text+"\n\n"
    output += "\n#___________________________________________________________________\n"

print(output)


with open(r'interesting_text_parts.txt', 'w') as fp:
    fp.write(output)
    #         fp.write("%s\n\n" % item)




