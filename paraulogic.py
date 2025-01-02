import csv
from datetime import datetime

file_path = 'clean_words.csv'

# Initialize an empty list to store words
words_lt = []

# Read the CSV file
with open(file_path, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        words_lt.append(row[0])

words_dict = {}

for word in words_lt:
    word_setted = ''.join((sorted(list(set(word)))))
    if word_setted in words_dict:
        words_dict[word_setted].append(word)
    else:
        words_dict[word_setted] = []
        words_dict[word_setted].append(word)

def powerset(set_of_letters):
    powerset = []
    center_letter = set_of_letters[0]
    set_of_letters = list(set_of_letters)
    len_set = len(set_of_letters)
    for i in range(1 << len_set):
        powerset.append([set_of_letters[j] for j in range(len_set) if (i & (1 << j))])
    powerset = [''.join((sorted(list(s)))) for s in powerset if center_letter in s]
    return powerset

set_of_letters = 'sodiau'

power_set = powerset(set_of_letters)


solution_words = []
for combi in power_set:
    try:
        solution_words.extend(words_dict[combi])
    except:
        pass

solution_words = sorted(list(set([word for word in solution_words if len(word) >= 3])))
print(solution_words)

today_date = datetime.today().strftime('%Y_%m_%d')

file_name = 'solution_' + today_date + '.txt'
textfile = open(file_name, "w")
for element in solution_words:
    textfile.write(element + "\n")
textfile.close()




