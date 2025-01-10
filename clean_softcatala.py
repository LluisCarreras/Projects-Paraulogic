import csv
import re
import unicodedata

file_path = 'adjectius-fdic.txt'

# Initialize an empty list to store words
words_lt = []

# Function to clean the string
def clean_string(input_string):
    # Regex to retain `[fem. ...]` content and remove other brackets and their content
    output_string = re.sub(
        r"\[fem\. ([^\]]+)\]|\[[^\]]+\]",
        lambda m: m.group(1) if m.group(1) else "",
        input_string,
    ).strip()
    return output_string

def correct_femenine(item):
    words = item.split()
    if len(words) == 2:
        first_word = words[0]
        second_word = words[1] 
        if second_word[0] == '-':
            if second_word in ('-ada', '-issa', '-ossa', '-ida', '-iva', '-osa', '-oqua'):
                second_word = first_word[:-2] + second_word[1:]
            elif second_word in ('-ana', '-ina'):
                second_word = first_word[:-1] + second_word[1:]
            else:
                second_word = first_word + 'a'
            new_item = ' '.join([first_word, second_word])
            return new_item
    return item

def clean_word(dirty_word):
    # Split and take only the first part
    one_word = dirty_word.split()[0]

    # Normalize the string to decompose characters with accents
    normalized_word = unicodedata.normalize('NFD', one_word)
    # Filter out combining characters (diacritics)
    normalized_word = ''.join(char for char in normalized_word if unicodedata.category(char) != 'Mn')

    # Delete trailing '-'
    if normalized_word[0] == '-':
        return None
    if normalized_word[-1] == '-':
        return None
    
    # Removes any non-word and non-space characters
    normalized_word = re.sub(r'[^a-zA-Z\-]', "", normalized_word)  

    # Delete '-se'
    if normalized_word[-3:] == '-se':
        normalized_word = normalized_word[:-3]

    # Removes any non trailing '-' 
    normalized_word = re.sub(r'-', "", normalized_word)  

    return normalized_word

# Read the CSV file
with open(file_path, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        row_text = row[0]

        # If trailing #, delete it
        if row_text[0] == '#': 
            row_text = row_text[1:]

        # Take only the rows that contain adjectives
        if '=categories: A;' in row_text:

            # Take the adjectives part of the row
            row_text = row_text.split('=')[0]

            # Apply the regular expression
            row_text = clean_string(row_text)
            
            # Make correct femenine
            row_text = correct_femenine(row_text)
            words_lt.append(row_text)


#for i in range(10):
#   print(words_lt[i])

separated_words_lt = [word.split() for word in words_lt]
flat_words_lt = [word for sublist in separated_words_lt for word in sublist]
clean_words_lt = [clean_word(word) for word in flat_words_lt]

input_file = "clean_words.csv"
#output_file = "extended_clean_words.csv"

words_to_add = []

# Open the input file and filter data
with open(input_file, "r", encoding="utf-8") as infile:
    reader = csv.reader(infile)
    for row in reader:
        if row:
            raw_word = row[0]
            if raw_word in clean_words_lt:
                for sublist in separated_words_lt:
                    if raw_word in sublist:
                        words_to_add.extend(sublist)

# Open the file in append mode
with open(input_file, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for word in words_to_add:
        writer.writerow([word])  # Wrap string in a list

