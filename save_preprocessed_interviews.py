import pickle




with open("list_of_interviews_after_preprocessing_with_stopwords.txt", "rb") as fp:   # Unpickling
    interviews_from_prepr = pickle.load(fp)


interviews = []

#When we use whole interviews
for interview in interviews_from_prepr:
    interview_textsegments = []
    for segment in interview:
        if not segment["speaker"] == "unsure":
            seg = segment["list_of_not_lemmatized_words"]
            del seg[0]
            text = " ".join(seg)
            interview_textsegments.append(text)
    interviews.append(interview_textsegments)

i = 1
for interview in interviews: 
    interview_text = ""
    for segment in interview:
        interview_text+=segment
        interview_text+="\n\n"
    with open("English Data/metadata_removed/interview_"+str(i)+".txt",'w',encoding='utf8') as f:
        f.write(interview_text)
    i+=1

'Möglichkeit: unsure rauslassen'