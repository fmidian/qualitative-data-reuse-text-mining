from textblob import TextBlob
import pickle
import numpy as np
import matplotlib.pyplot as plt



with open("interviews_for_n_grams.txt", "rb") as fp:   # Unpickling
    interviews_from_prepr = pickle.load(fp)

segment_polarities = []
most_negative = ""
most_positive = ""
most_negative_score= 1
most_positive_score= -1
most_positive_location = ""
most_negative_location = ""
interview_sentiments = []

for interview_index, interview in enumerate(interviews_from_prepr):
    list_of_polarities = []
    all_segments_sentiment_sum = 0
    for segment_index, segment in enumerate(interview):
        if segment["speaker"]!="interviewee":
            continue
        # print(segment["continuous_text"])
        sentiment = TextBlob(segment["continuous_text"]).sentiment
        # print(sentiment, sentiment.polarity, sentiment.polarity*sentiment.subjectivity)
        # print("")     
        polarity = sentiment.polarity
        # print("interview "+str(interview_index+1)+"  segment "+str(segment_index+1)+"  speaker "+segment["speaker"])
        # print(segment["continuous_text"])
        # print(polarity)
        # print("")
        if polarity >= most_positive_score:
            most_positive_score = polarity
            most_positive = segment["continuous_text"]
            most_positive_location = "interview "+str(interview_index+1)+"  segment "+str(segment_index+1)+"  speaker "+segment["speaker"]
        if polarity <= most_negative_score:
            most_negative_score = polarity
            most_negative = segment["continuous_text"]
            most_negative_location = "interview "+str(interview_index+1)+"  segment "+str(segment_index+1)+"  speaker "+segment["speaker"]
        list_of_polarities.append(polarity)
        all_segments_sentiment_sum += polarity
    
    segment_polarities.append( {"polarities": list_of_polarities, "interview": interview_index+1} )
    # segment_polarities.append( {"polarities": list_of_polarities, "continuous_text": segment["continuous_text"], "interview": interview_index+1, "segment": segment_index+1} )
    interview_sentiments.append(all_segments_sentiment_sum/len(interview))

standard_sentiments = [0]*14
for interview in segment_polarities:
    height = []
    length_of_one_part = round(len(interview["polarities"])/14, 0)
    # length_of_one_part = int(len(interview["polarities"])/14)
    i = 0
    sentiment_over_part = 0
    for segment in interview["polarities"]:
        sentiment_over_part+=segment
        i+=1
        if i == int(length_of_one_part):
            height.append(sentiment_over_part/length_of_one_part)
            sentiment_over_part = 0
            i = 0

    if i != 0:
        height.append(sentiment_over_part/i)
    if len(height) == 15:
        height[13]= (height[13] + height[14])/2
        del height[14]
    elif len(height) == 16:
        height[13]= (height[13] + height[14] + height[15])/3
        del height[15]
        del height[14]
    elif len(height) == 13:
        height.append(height[12])
    elif len(height) == 12:
        height.append(height[11])
        height.append(height[11])
    elif len(height) == 11:
        height.append(height[10])
        height.append(height[10])
        height.append(height[10])


    standard_sentiments = [sum(x) for x in zip(standard_sentiments, height)]

    # print("length ", len(height), "length_of_one_part: ", length_of_one_part, "len()/14: ", len(interview["polarities"])/14, "len(): ", len(interview["polarities"]))
    
    bars = range(1, len(height)+1)
    y_pos = np.arange(len(bars))

    plt.ylim(top = 1)


    # Create bars
    plt.bar(y_pos, height)

    # Create names on the x-axis
    plt.xticks(y_pos, bars)

    # Show graphic
    plt.savefig("sentiment_charts/interview"+str(interview["interview"])+".png",dpi=400)

    plt.clf()
standard_sentiments = [x/len(segment_polarities) for x in standard_sentiments]
bars = range(1, len(standard_sentiments)+1)
y_pos = np.arange(len(bars))
plt.ylim(top = 1)
plt.bar(y_pos, standard_sentiments)
plt.xticks(y_pos, bars)
plt.savefig("sentiment_charts/interview_average.png",dpi=400)


print("most negative: ( score: ", most_negative_score, ")")
print(most_negative)
print(most_negative_location)
print("")
print("most positive: ( score: ", most_positive_score, ")")
print(most_positive)
print(most_positive_location)

for index, interview_sent in enumerate(interview_sentiments):
    print("interview ", index+1, " sentiment: ", interview_sent)


