# Read TXT files into a list of interviews
interviews = []

# Initialize word count
total_word_count = 0

# Loop through all 56 interviews
for i in range(1, 57):
    # Set the base filename
    filename = "English Data/6226int0"

    # Add leading zero for filenames 1-9
    if i < 10:
        filename += "0"

    # Construct the full filename
    full_filename = filename + str(i) + ".txt"

    # Open the file and read its content
    with open(full_filename, encoding="utf-8", errors="replace") as file:
        text = file.read()
        list_text = text.split()

        # Count the number of words in the current interview
        interview_word_count = len(list_text)

        # Add the word count of the current interview to the total word count
        total_word_count += interview_word_count

        # Add the list of words to the interviews list
        interviews.append(list_text)

# Calculate the average number of words in the corpus
average_word_count = total_word_count / 56

# Print the average number of words in the corpus
print("Average number of words in the corpus:", average_word_count)