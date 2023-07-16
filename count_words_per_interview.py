#read txt files into list
interviews = []
#loop through all 56 interviews
number_of_words = 0
for i in range(1, 57): #57
    filename = "English Data/6226int0"
    if i<10: filename += "0"

    with open(filename+str(i)+".txt", encoding="utf-8", errors="replace") as file:
        text = file.read()
        list_text = text.split()
        number_of_words += len(list_text)

print("average number of words in corpus", number_of_words / 56)
        