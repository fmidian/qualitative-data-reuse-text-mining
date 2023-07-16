from itertools import filterfalse
import spacy

def read_files_and_remove_metadata(number_of_interviews):
    output = open("output.txt","w")

    #read txt files into list
    interviews = []
    #loop through all 56 interviews?
    for i in range(1, number_of_interviews+1): #57
        filename = "English Data/6226int0"
        if i<10: filename += "0"

        with open(filename+str(i)+".txt", encoding="utf-8", errors="replace") as file:
            text = file.read()

            #interview is divided into segments after each blank line. Because of the structure of the txt.files, this means there is a new segment for every change of speaker
            interview_segments = text.split("\n\n")

            print("Interview number: ", i)
            #sometimes there is thertain metadata at the beginning of interviews (such as CD 1 or Tape 1)
            if "track" in interview_segments[0].lower() or "CD 1" in interview_segments[0] or "Tape 1" in interview_segments[0]:
                del interview_segments[0]
            elif "track" in interview_segments[1].lower() or "CD 1" in interview_segments[1] or "Tape 1" in interview_segments[1]:
                del interview_segments[1]
            elif "track" in interview_segments[2].lower() or "CD 1" in interview_segments[2] or "Tape 1" in interview_segments[2]:
                del interview_segments[2]

            #-> Forderung an Interview-Archive: Einheitlichkeit bei der Formatierung. Hier werden 5 verschiedene Formuliereungen ("interview conducted", "interviewed by", ...) für den gleichen Inhalt benutzt, was die computationelle Verarbeitung verkompliziert 
            line_of_start = -1
            for i in range(0, 5):
                if "interview held" in interview_segments[i].lower() or "interview conducted" in interview_segments[i].lower() or "interviewed by" in interview_segments[i].lower() or "interview with" in interview_segments[i].lower() or "interviewed on" in interview_segments[i].lower():
                    line_of_start = i
                    break
            if line_of_start != -1:
                print("line of interview start", line_of_start)
                del interview_segments[:line_of_start+1]
            else:
                print("interview start not found")
                print("0", interview_segments[0])
                print("1", interview_segments[1])
                print("2", interview_segments[2])

                #in this cases the interview starts without metadata before it, so nothing has to be done


            line_of_end = -1
            for i in range(len(interview_segments)-1, -1, -1):
                if "end of interview" in interview_segments[i].lower():
                    line_of_end = i
                    break
            if line_of_end != -1:
                print("line of interview ending", line_of_end)
                del interview_segments[line_of_end:]
            else:
                for i in range(len(interview_segments)-1, -1, -1):
                    if "name of project:" in interview_segments[i].lower():
                        line_of_end = i-1
                        break
                if line_of_end != -1:
                    print("line of interview ending", line_of_end)
                    del interview_segments[line_of_end:]
                else:
                    print("End of interview not found")
            print("number of interview segments: ", len(interview_segments))
            print("")

            #remove new lines
            interview_segments = [x.replace("\n", "") for x in interview_segments]
            
            #to lowercase
            interview_segments = [x.lower() for x in interview_segments]


            #only filters some empty lines
            #interview_segments = filterfalse(lambda x: len(x)<2, interview_segments)

            interviews.append(interview_segments)

    print("number of interviews ", len(interviews))
    return interviews

#todo: Speichern zu welchem interview ein segment gehört

def remove_speakers_and_meta_content_in_transcript_itself(interviews):
    nlp = spacy.load("en_core_web_trf")
    #todo maybe use bigger model? Like en_core_web_lg bzw. en_core_web_trf
    #download model: python -m spacy download en_core_web_trf
    nlp_interviews = []
    i = 0
    for interview in interviews:
        nlp_segments = []
        for segment in interview:
            doc = nlp(segment)
            nlp_segments.append(doc)
        nlp_interviews.append(nlp_segments)
        print("interview ", i)
        i+=1
    
    interviews_after_prepr = []
    i = 1
    for interview in nlp_interviews:
        #this assumes, that the first segment is spoken by the interviewer. I made sure that this is true for all interviews
        interviewer = interview[0][0].text
        interviewee = interview[1][0].text
        # Erstes Token in jedem Segment enthaelt entweder Interviewer oder Interviewee.
        print("next interview: ", i)
        print("interviewer", interviewer)
        print("interviewee", interviewee)
        i = i+1
        segments_in_interview = []
        segment_with_speaker_before = "start"
        segments_in_interview = []

        for segment in interview:
            #list_of_all_words = []
            #list_of_not_lemmatized_words = []
            list_of_tokens = list(segment)

            segment_with_speaker = {
                "speaker": "unsure",
                "list_of_tokens": [],
                "list_of_words": [], 
                "list_of_not_lemmatized_words": [],
                "continuous_text": ""
            }

            if len(list_of_tokens) > 1:
                if list_of_tokens[0].text.casefold() == interviewer.casefold():
                    segment_with_speaker["speaker"] = "interviewer"
                    del list_of_tokens[0]
                elif list_of_tokens[0].text.casefold() == interviewee.casefold():
                    segment_with_speaker["speaker"] = "interviewee"
                    del list_of_tokens[0]
                elif len(list_of_tokens) > 5 and segment_with_speaker_before != "start":
                    segment_with_speaker["speaker"] = segment_with_speaker_before["speaker"]
                    print("unsure speaker and greater 5: ", ''.join(token.text_with_ws for token in segment))
                else:
                    print("unsure speaker: ", ''.join(token.text_with_ws for token in segment))
                    #example output: 
                    # unsure speaker:    interruption
                    # unsure speaker:    pause
                    # unsure speaker:    interruption
                    # unsure speaker:    break
                    # unsure speaker:    interruption
                    # unsure speaker:    interruption
                    # unsure speaker:    interruption
                    # unsure speaker:    interruption
                    # unsure speaker:    break
                    # unsure speaker:    break
                    # unsure speaker:    telephone
                    # unsure speaker:    telephone

                    #-> these segments are often meaningless
                    continue

                    # if list_of_tokens[0].text == "interruption" or list_of_tokens[0].text == "pause" or list_of_tokens[0].text == "break" or list_of_tokens[0].text == "telephone" or list_of_tokens[1].text == "interruption" or list_of_tokens[1].text == "pause" or list_of_tokens[1].text == "break" or list_of_tokens[1].text == "telephone" or list_of_tokens[0].text == "content" or list_of_tokens[1].text == "content" or list_of_tokens[0].text == "interview" or list_of_tokens[1].text == "interview" or list_of_tokens[0].text == "laughter" or "tape" in list_of_tokens[0].text or "end" in list_of_tokens[0].text or "track" in list_of_tokens[0].text:
                    #     print("deleted segment: ", continuous_text)
                    #     continue
                if list_of_tokens[0].text == ":":
                    del list_of_tokens[0]
                if list_of_tokens[0].text.isspace():
                    del list_of_tokens[0]
                continuous_text = ''.join(token.text_with_ws for token in list_of_tokens)
                # print("plain text without metadata:")
                # print(continuous_text)

                #todo: einklammerung bei sinnlosen segmenten nutzen []

                segment_with_speaker["continuous_text"] = continuous_text
                segment_with_speaker["list_of_tokens"] = list_of_tokens
                segments_in_interview.append(segment_with_speaker)
                segment_with_speaker_before = segment_with_speaker

        interviews_after_prepr.append(segments_in_interview)

    return interviews_after_prepr

#todo Filter Groß/Kleinschreibung scheint nicht zu funktionieren
#idee erkennung interviewer: Größere Textanteile hat Interviewter -> autmatische erkennung -> könnte testen wie oft das richtig ist

def is_stopword(token):
    manually_added_stopwords = ["d", "ve", "s", "t", "yes", "know", "think", "go", "say", "don", "actually", "get", "come", "didn", "thing", "erm", "m", "wasn", "oh", "yeah", "er", "remember", "lot", "bit", "okay", "couldn", "weren", "m", "\ufffdm", "\ufffd", "laughs", "mildre", 'like', 'mean', 'way', 'kind', 'want', 'look', 'sort', 'laugh', 'find', 'take', 'try', 'start', 'tell', 'happen', 'place', 'later', 'see', 'couldn', 'll', 'somebody', "people", "live", "life", "stuff", "ray", "tony", "collin", "11", "robinns", "year", "ask", "john", "david", "right", "etc", "paul", "brian", "elliott", "hadn", "mainly", "occur", "didn", "isn", "sseldorf", "nonetheless", "robert","ian", "stuart", "yea", "nay", "peter", "inaudible", "rosemary", "barbara", "michael", "evans", "raymond", "audrey", "particular", "particularly", "let", "everard", "have", "aren"]
    #Mögliches Beispiel für Besonderheit gesprochene Sprache: stopwords yeah, yes, oh werden in Spacy standardmäßig nicht gefiltert; 
    #Auch Wörter wie like und think eventuell anders in gesprochener Sprache
    #Vor der Bereinigung der Namen mit Doppelpunkt vor den Beiträgen: Topics bilden sich um die Namen
    if token.is_stop:
        # print("spacy stopword: ", token.lemma_)
        return True
    elif token.lemma_ in manually_added_stopwords:
        return True
    else:
        return False

def remove_punctuation_and_stopwords(interviews):
    for interview in interviews:
        for segment in interview:
            segment["list_of_tokens"] = [token for token in segment["list_of_tokens"] if not (token.is_punct or token.text.isspace() or is_stopword(token))]
    return interviews

def add_lists_of_words_and_remove_list_of_tokens(interviews):
    for interview in interviews:
        for segment in interview:
            segment["list_of_words"] = [token.lemma_ for token in segment["list_of_tokens"]]
            segment["list_of_not_lemmatized_words"] = [token.text for token in segment["list_of_tokens"]]

    without_tokens = interviews.copy()
    for interview in without_tokens:
        for segment in interview:
            del segment["list_of_tokens"]
    return without_tokens

def change_analysis_units_to_number_of_words(number_of_words_in_unit, interviews):
    x = 0
    for interview in interviews:
        x+=len(interview)
    print("total number of segments before unification: ", x)

    interviews_with_units = []

    lowest = 1000
    highest = 300

    sum_for_mean = 0
        
    interview_number = 1
    for interview in interviews:
        segments_of_interview = []
        segment_of_unit = {
            "list_of_words": [], 
            "list_of_not_lemmatized_words": [],
            "continuous_text": "",
            "interview_number": interview_number
        }
        for segment in interview:
            segment_of_unit["list_of_words"].extend(segment["list_of_words"])
            segment_of_unit["list_of_not_lemmatized_words"].extend(segment["list_of_not_lemmatized_words"])
            segment_of_unit["continuous_text"] += "\n\n" + segment["continuous_text"]
            number_of_words = len(segment_of_unit["list_of_words"])
            if  number_of_words >= number_of_words_in_unit and segment["speaker"] == "interviewee":
                segments_of_interview.append(segment_of_unit)
                sum_for_mean += number_of_words
                if number_of_words > highest: 
                    highest = number_of_words
                if number_of_words < lowest:
                    lowest = number_of_words
                segment_of_unit = {
                    "list_of_words": [], 
                    "list_of_not_lemmatized_words": [],
                    "continuous_text": "", 
                    "interview_number": interview_number
                }
        number_of_words = len(segment_of_unit["list_of_words"])
        if number_of_words != 0:
            segments_of_interview.append(segment_of_unit)
            sum_for_mean += number_of_words
            if number_of_words > highest: 
                highest = number_of_words
            if number_of_words < lowest:
                lowest = number_of_words
        else:
            print(segment_of_unit["list_of_words"])
        interviews_with_units.append(segments_of_interview)
        interview_number += 1
    print("lowest unit", lowest)
    print("highest unit", highest)

    x = 0
    for interview in interviews_with_units:
        x+=len(interview)
    print("total number of segments after unification: ", x)

    print("mean number of words in segment: ", sum_for_mean/x)
    return interviews_with_units

def change_to_segments_of_interviewee(interviews):
    x = 0
    for interview in interviews:
        x+=len(interview)
    print("total number of segments before change_to_segments_of_interviewee: ", x)

    interviews_interviewee = []
    for interview in interviews:
        interview_interviewee = []
        for segment in interview:
            if segment["speaker"] == "interviewee":
                interview_interviewee.append(segment)
        interviews_interviewee.append(interview_interviewee)
    x = 0
    for interview in interviews_interviewee:
        x+=len(interview)
    print("total number of segments after change_to_segments_of_interviewee: ", x)

    return interviews_interviewee

def replace_n_grams(interviews):
    #manually created list of bi- and trigrams taken from the list of the most common ones
    bigrams_for_tokenization = [["working", "class"], ["social", "mobility"], ["old", "people"], ["young", "people"], ["years", "ago"], ["middle", "class"], ["social", "science"], ["oral", "history"], ["grammar", "school"], ["vice", "chancellor"], ["labour", "party"], ["south", "africa"], ["social", "sciences"], ["cultural", "studies"], ["community", "studies"], ["time", "time"], ["spent", "time"], ["sri", "lanka"], ["great", "depression"]]
    trigrams_for_tokenization = [["social", "science", "research"], ["london",  "school",  "economics"], ["second",  "world",  "war"], ["british", "household", "panel"], ["national", "health", "service"]]

    for interview in interviews:
        for segment in interview:
            not_lemmatized_words = segment["list_of_not_lemmatized_words"]
            lemmatized_words = segment["list_of_words"]
            #print("len ", len(not_lemmatized_words))
            i = 1
            while i<len(not_lemmatized_words):
                #print(i)
                for trigram in trigrams_for_tokenization:
                    if trigram[2] == not_lemmatized_words[i] and trigram[1] == not_lemmatized_words[i-1] and trigram[2] == not_lemmatized_words[i-2]:
                        not_lemmatized_words[i-2] = trigram[0]+ "_"+trigram[1]+ "_"+trigram[2]
                        del not_lemmatized_words[i-1]
                        del not_lemmatized_words[i-1]
                        lemmatized_words[i-2] = trigram[0]+ "_"+trigram[1]+ "_"+trigram[2]
                        del lemmatized_words[i-1]
                        del lemmatized_words[i-1]
                        i -= 2                
                for bigram in bigrams_for_tokenization:
                    if bigram[1] == not_lemmatized_words[i] and bigram[0] == not_lemmatized_words[i-1]:
                        not_lemmatized_words[i-1] = bigram[0]+ "_"+bigram[1]
                        del not_lemmatized_words[i]
                        lemmatized_words[i-1] = bigram[0]+ "_"+bigram[1]
                        del lemmatized_words[i]
                        i -= 1
                        #print("replaced something")
                i+=1
    return interviews
                


    #done unit soll mit interviewer-segment starten
    #todo großen Spacy Englisch Korpus für nlp benutzen?
    #done metriken zur Evaluierung der verschiedenen Topic Models benutzen (siehe papers, eigene Idee Wortähnlichkeit)

    #for schleife evaluation
    #ausprobierte möglichkeiten
        #chunks von 10 in 10-er Schritten zu 100
        #alle oder nur befragter
        #jeweils nur 3/4 und 1/2 der Topics Anzahl



        


    



