import spacy
import re
from spacy.lang.en import English
from itertools import filterfalse
import json
import pickle
import numpy as np
import gensim.corpora as corpora
from tika import parser



#read txt files into list
interviews = []
nlp = spacy.load("en_core_web_sm")
for i in range(1, 2): #57
    filename = "German Data/adg0"
    if i<10: filename += "0"
    if i<100: filename += "0"

    raw = parser.from_file(filename+str(i)+"_transcript_de.pdf")
    pdf_content = raw['content']

    print("interview number ", i)

    interview_segments = pdf_content.split("\n\n")
    for i in range(0, 20):
        print(interview_segments[i])

    line_of_interviewer_name = -1
    for i in range(0, len(interview_segments)):
        if interview_segments[i].startswith("Interview: "):
            line_of_interviewer_name = i
    if line_of_interviewer_name == -1:
        print("Interviewer name not found")
    else:
        interviewer = interview_segments[line_of_interviewer_name][12:]
        print("Interviewer ", interviewer)




