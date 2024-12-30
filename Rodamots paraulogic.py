#!/usr/bin/env python
# coding: utf-8


import pickle
with open ('diec.txt', 'rb') as fp:
    words = pickle.load(fp)

word_dict = {}

for word in words:
    word_setted = ''.join((sorted(list(set(word)))))
    if word_setted in word_dict:
        word_dict[word_setted].append(word)
    else:
        word_dict[word_setted] = []
        word_dict[word_setted].append(word)

def powerset(set_of_letters, center_letter):
    powerset = []
    len_set = len(set_of_letters)
    for i in range(1 << len_set):
        powerset.append([set_of_letters[j] for j in range(len_set) if (i & (1 << j))])
    powerset = [''.join((sorted(list(s)))) for s in powerset if center_letter in s]
    return powerset

set_of_letters = list('adotenz')
center_letter = 't'


powerset = powerset(set_of_letters, center_letter)

solution_words = []
for combi in powerset:
    try:
        solution_words.extend(word_dict[combi])
    except:
        pass

solution_words = sorted(list(set([word for word in solution_words if len(word) >= 3])))

from datetime import datetime

today_date = datetime.today().strftime('%Y_%m_%d')

file_name = 'solucio_' + today_date + '.txt'
textfile = open(file_name, "w")
for element in solution_words:
    textfile.write(element + "\n")
textfile.close()




