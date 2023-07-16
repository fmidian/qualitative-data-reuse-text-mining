import pickle

with open("LUSIR_df_speakers_clean_normalized_1sentence(s)_NEW - CORPUS", "rb") as fp:   # Unpickling
#with open("ods_transcripts_df_sentences_clean_normalized_10sentence(s)_NEW", "rb") as fp:   # Unpickling

    segments = pickle.load(fp)


print(len(segments))

for x in segments:
    print(["id"])



for index, row in segments.iterrows():
    print(row['id'], row['chunk'])
    interview_id = int(row["id"][3:7])
    print(interview_id)

segments = segments.loc[:, "chunk"].tolist()
sum_words = 0

segments = [x.split() for x in segments]

for segment in segments:
    sum_words += len(segment)


mean_words_in_segment = sum_words / len(segments)

print("mean number of words in segment", mean_words_in_segment)



#1 sentence -> 21 words in segment (without lemmatization)

# nlp = spacy.load("en_core_web_sm")
# nlp_interviews = []
# i = 0
# for interview in interviews:
#     nlp_segments = []
#     for segment in interview:
#         doc = nlp(segment)
#         nlp_segments.append(doc)
#     nlp_interviews.append(nlp_segments)
#     print("interview ", i)
#     i+=1

# interviews_after_prepr = []
# i = 1
# for interview in nlp_interviews:
#     #this assumes, that the first segment is spoken by the interviewer. I made sure that this is true for all interviews
#     interviewer = interview[0][0].text
#     interviewee = interview[1][0].text
#     # Erstes Token in jedem Segment enthaelt entweder Interviewer oder Interviewee.
#     print("next interview: ", i)
#     print("interviewer", interviewer)
#     print("interviewee", interviewee)
#     i = i+1
#     segments_in_interview = []
#     segment_with_speaker_before = "start"
#     segments_in_interview = []

#     for segment in interview:
#         #list_of_all_words = []
#         #list_of_not_lemmatized_words = []
#         list_of_tokens = list(segment)

#         segment_with_speaker = {
#             "speaker": "unsure",
#             "list_of_tokens": [],
#             "list_of_words": [], 
#             "list_of_not_lemmatized_words": [],
#             "continuous_text": ""
#         }

#         if len(list_of_tokens) > 1:
#             if list_of_tokens[0].text.casefold() == interviewer.casefold():
#                 segment_with_speaker["speaker"] = "interviewer"
#                 del list_of_tokens[0]
#             elif list_of_tokens[0].text.casefold() == interviewee.casefold():
#                 segment_with_speaker["speaker"] = "interviewee"
#                 del list_of_tokens[0]
#             elif len(list_of_tokens) > 5 and segment_with_speaker_before != "start":
#                 segment_with_speaker["speaker"] = segment_with_speaker_before["speaker"]
#                 print("unsure speaker and greater 5: ", ''.join(token.text_with_ws for token in segment))
#             else:
#                 print("unsure speaker: ", ''.join(token.text_with_ws for token in segment))
#                 #example output: 
#                 # unsure speaker:    interruption
#                 # unsure speaker:    pause
#                 # unsure speaker:    interruption
#                 # unsure speaker:    break
#                 # unsure speaker:    interruption
#                 # unsure speaker:    interruption
#                 # unsure speaker:    interruption
#                 # unsure speaker:    interruption
#                 # unsure speaker:    break
#                 # unsure speaker:    break
#                 # unsure speaker:    telephone
#                 # unsure speaker:    telephone

#                 #-> these segments are often meaningless
#                 continue

#                 # if list_of_tokens[0].text == "interruption" or list_of_tokens[0].text == "pause" or list_of_tokens[0].text == "break" or list_of_tokens[0].text == "telephone" or list_of_tokens[1].text == "interruption" or list_of_tokens[1].text == "pause" or list_of_tokens[1].text == "break" or list_of_tokens[1].text == "telephone" or list_of_tokens[0].text == "content" or list_of_tokens[1].text == "content" or list_of_tokens[0].text == "interview" or list_of_tokens[1].text == "interview" or list_of_tokens[0].text == "laughter" or "tape" in list_of_tokens[0].text or "end" in list_of_tokens[0].text or "track" in list_of_tokens[0].text:
#                 #     print("deleted segment: ", continuous_text)
#                 #     continue
#             if list_of_tokens[0].text == ":":
#                 del list_of_tokens[0]
#             if list_of_tokens[0].text.isspace():
#                 del list_of_tokens[0]
#             continuous_text = ''.join(token.text_with_ws for token in list_of_tokens)
#             # print("plain text without metadata:")
#             # print(continuous_text)

#             #todo: einklammerung bei sinnlosen segmenten nutzen []

#             segment_with_speaker["continuous_text"] = continuous_text
#             segment_with_speaker["list_of_tokens"] = list_of_tokens
#             segments_in_interview.append(segment_with_speaker)
#             segment_with_speaker_before = segment_with_speaker

#     interviews_after_prepr.append(segments_in_interview)
