import nltk
from nltk import bigrams
from nltk import trigrams
import pickle
import numpy as np



with open("interviews_for_n_grams.txt", "rb") as fp:   # Unpickling
    interviews_from_prepr = pickle.load(fp)


interviews = []

#When we use whole interviews
for interview in interviews_from_prepr:
     interview_words = []
     interview_words_array = []
     for segment in interview:
         interview_words.extend(segment["list_of_not_lemmatized_words"])
     interviews.append(interview_words)

#When we use the whole text
#words = []
#for interview in interviews_from_prepr:
#    interview_words = []
#    interview_words_array = []
#    for segment in interview:
#        interview_words.extend(segment["list_of_not_lemmatized_words"])
        #interview_words.extend(segment["list_of_words"])
#    words.extend(interview_words)
#interviews.append(words)


# i = 1
# for interview in interviews:
#     print("interview ", i)
#     bigram = bigrams(interview)
#     trigram = trigrams(interview)


#     frequence_bigrams = nltk.FreqDist(bigram)
#     frequence_trigrams = nltk.FreqDist(trigram)

#     #for key,value in frequence_bigrams.most_common(30):
#     #   with open("n_grams_bi_not_lemma.txt", "a") as print_file:
#     #      print(key, value, file=print_file)
#     #for key,value in frequence_trigrams.most_common(30):
#     #   with open("n_grams_tri_not_lemma.txt", "a") as print_file:
#     #      print(key, value, file=print_file)
#     i+=1
#     print("")

#load the lemmatized version
interviews_lemma=[]
#interviews_array = []

for interview in interviews_from_prepr:
     interview_words2 = []
     interview_words_array2 = []
     for segment in interview:
        #interviews_array.append(np.array(segment["list_of_words"]))
        #interviews_lemma.append(segment["list_of_words"])
         interview_words2.extend(segment["list_of_words"])
     interviews_lemma.append(interview_words2)

#print("length of interviews without lemma", len(interviews))
#print("length of interviews lemma", len(interviews_lemma))

#print(interviews[0][1763])
#print(interviews_lemma[0][1763])

# manually created list of bi- and trigrams taken from the list of the most common ones
#bigrams_for_tokenization = ["working class", "middle class", "social science", "oral history", "grammar school",
#  "vice chancellor", "labour party", "south africa", "social sciences", "cultural studies", "community studies", 
#  "point of view", "time time", "spent time"]
#trigrams_for_tokenization = ["social science research", "london school economics", "second world war",]

x=0
s=0
print(len(interviews_from_prepr))
print("Interviews from Preprocessing number of elements at 0:", len(interviews_from_prepr[0]))
print("Interviews from Preprocessing number of elements at 1:", len(interviews_from_prepr[1]))
print(type(interviews_from_prepr))
print(interviews_from_prepr[0][15]["list_of_not_lemmatized_words"])


#replace bigrams
for interview in interviews_from_prepr:
    print("Interview", x)
    for segment in interview:
        print("--Segment", s)
        r =len(segment["list_of_not_lemmatized_words"])
        print("--Length of segment", r)
        for k, v in segment.items():
            if k == "list_of_not_lemmatized_words":
                for i in range(r):
                    
                    if v[i] == "class":
                        if v[i-1] =="working":
                            v[i-1] = "working class"
                            del v[i]
                            print("--Word", i, "without lemma replaced")
                            
                            #interviews_lemma[x][i-1]="working class"
                            #del interviews_lemma[x][i]
                            #print("Word with lemma replaced")
                            # for interviewlem in interviews_lemma:
                            #     interviewlem[i-1]="working class"
                            #     del interviewlem[i]

                            i-=1
                            r = len(segment["list_of_not_lemmatized_words"])-1
                        #print("Length of the interview after decrementing: ", r)
                        
                           

                    elif v[i] == 'class':
                        if v[i-1] =="middle":
                            v[i-1] = "middle class"
                            del v[i]

                            #interviews_lemma[x][i-1]="middle class"
                            #del interviews_lemma[x][i]
                        i-=1
                        r = len(interview)-1
                        

                    elif interview[i] == 'science':
                        if interview[i-1] =="social":
                            interview[i-1] = "social science"
                            del interview[i]

                            #interviews_lemma[x][i-1]="social science"
                            #del interviews_lemma[x][i]

                        i-=1
                        r = len(interview)-1
                        

                    elif interview[i] == 'sciences':
                        if interview[i-1] =="social":
                            interview[i-1] = "social science"
                            del interview[i]

                            #interviews_lemma[x][i-1]="social science"
                            #del interviews_lemma[x][i]

                        i-=1
                        r = len(interview)-1
                                    

                    elif interview[i] == 'party':
                        if interview[i-1] =="labour":
                            interview[i-1] = "labour party"
                            del interview[i]

                            #interviews_lemma[x][i-1]="labour party"
                            #del interviews_lemma[x][i]

                        i-=1
                        r = len(interview)-1
                    

                    elif interview[i] == 'party':
                        if interview[i-1] =="labor":
                            interview[i-1] = "labour party"
                            del interview[i]

                            #interviews_lemma[x][i-1]="labour party"
                            #del interviews_lemma[x][i]

                        i-=1
                        r = len(interview)-1
                        

                    elif interview[i] == 'africa':
                        if interview[i-1] =="south":
                            interview[i-1] = "south africa"
                            del interview[i]

                            #interviews_lemma[x][i-1]="south africa"
                            #del interviews_lemma[x][i]

                        i-=1
                        r = len(interview)-1
                    

                    elif interview[i] == 'studies':
                        if interview[i-1] =="community":
                            interview[i-1] = "community"
                            del interview[i]

                            #interviews_lemma[x][i-1]="community studies"
                            #del interviews_lemma[x][i]

                        i-=1
                        r = len(interview)-1
                    
        i+=1
        s+=1
    x+=1    
    print("replacing of bigrams successful")



#########################################################################
#replace bigrams
for interview in interviews_lemma:
    print("Interview", x)
    r =len(interviews[x])
    for i in range(r):
        
        if interview[i] == "class":
            if interview[i-1] =="working":
                interview[i-1] = "working class"
                del interview[i]
                print("Word", i, "without lemma replaced")
            
            i-=1
            r = len(interviews[x])-1
            #print("Length of the interview after decrementing: ", r)
            x +=1
                

        elif interview[i] == 'class':
            if interview[i-1] =="middle":
                interview[i-1] = "middle class"
                del interview[i]

            i-=1
            r = len(interview)-1
            x +=1

        elif interview[i] == 'science':
            if interview[i-1] =="social":
                interview[i-1] = "social science"
                del interview[i]

            i-=1
            r = len(interview)-1
            x +=1

        elif interview[i] == 'sciences':
            if interview[i-1] =="social":
                interview[i-1] = "social science"
                del interview[i]

            i-=1
            r = len(interview)-1
            x +=1                


        elif interview[i] == 'party':
            if interview[i-1] =="labour":
                interview[i-1] = "labour party"
                del interview[i]

            i-=1
            r = len(interview)-1
            x +=1

        elif interview[i] == 'party':
            if interview[i-1] =="labor":
                interview[i-1] = "labour party"
                del interview[i]

            i-=1
            r = len(interview)-1
            x +=1

        elif interview[i] == 'africa':
            if interview[i-1] =="south":
                interview[i-1] = "south africa"
                del interview[i]

            i-=1
            r = len(interview)-1
            x +=1

        elif interview[i] == 'studies':
            if interview[i-1] =="community":
                interview[i-1] = "community"
                del interview[i]

            i-=1
            r = len(interview)-1
            x +=1
    i+=1
print("replacing of bigrams successful")

print("Non lemmatized interviews results:", interviews[0][1762])
print("Lemma_Interview result:", interviews_lemma[0][8086])



# # replace trigrams
# for interview in interviews:
#     x+=1
#     print("Interview", x)
#     for i in range(len(interview)):
#         if interview[i] == "economics":
#             if interview[i-1] =="school":
#                 if interview[i-2] =="london":
#                     interview[i-2] = "london school of economics"
#                     del interview[i]
#                     del interview[i-1]
#                     print("Word", i, "without lemma replaced")  

#                 for interviewlem in interviews_lemma:
#                     interviewlem[i-2]="london school of economics"
#                     del interviewlem[i]
#                     del interviewlem[i-1]
#                 i-=1
#                 i-=1
#                 print("replaced")

#         elif interview[i] == "research":
#             if interview[i-1] =="social science":
#                 interview[i-1] = "social science research"
#                 del interview[i]

#                 for interviewlem in interviews_lemma:
#                     interviewlem[i-1]="social science research"
#                     del interviewlem[i]
#                 i-=1

#         elif interview[i] == 'war':
#             if interview[i-1] =="world":
#                 if interview[i-2] =="second":
#                     interview[i-2] = "second world war"
#                     del interview[i]
#                     del interview[i-1]

#                 for interviewlem in interviews_lemma:
#                     interviewlem[i-2]="second world war"
#                     del interviewlem[i]
#                     del interviewlem[i-1]
#                 i-=2
#     i+=1
# print("replacing of trigrams successful")