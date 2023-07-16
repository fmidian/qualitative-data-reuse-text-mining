for i in range(1, 57): #57
    filename_input = "English Data/6226int0"
    filename_output = "English Data/utf8/6226int0"
    if i<10: 
        filename_input += "0"
        filename_output += "0"
    
    with open(filename_input+str(i)+".txt", encoding="utf-8", errors="replace") as file:
        text = file.read()
        with open(filename_output+str(i)+".txt",'w',encoding='utf8') as f:
            f.write(text)