import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_letters():
    # Set up the Selenium WebDriver (e.g., ChromeDriver)
    driver = webdriver.Chrome()  # Ensure you have the ChromeDriver installed
    driver.get("https://www.vilaweb.cat/paraulogic/")

    # Find all the <div> elements with the class "hex-in"
    divs = driver.find_elements(By.CLASS_NAME, "hex-in")

    # Extract the text from each <div>
    letters = []
    center_letter = None
    for div in divs:
        letter = div.find_element(By.TAG_NAME, "p").text
        a_tag = div.find_element(By.CLASS_NAME, "hex-link")
        element_id = a_tag.get_attribute("id")
        if element_id == "center-letter":
            center_letter = letter
        letters.append(letter)

    letters.remove(center_letter)
    letters = [center_letter] + letters
    letters = ''.join(letters)
    letters = letters.lower()

    print("Extracted letters:", letters)

    return letters

    # Close the browser
    driver.quit()

def make_dictionary():
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

    return words_dict

def powerset(set_of_letters):
    powerset = []
    center_letter = set_of_letters[0]
    set_of_letters = list(set_of_letters)
    len_set = len(set_of_letters)
    for i in range(1 << len_set):
        powerset.append([set_of_letters[j] for j in range(len_set) if (i & (1 << j))])
    powerset = [''.join((sorted(list(s)))) for s in powerset if center_letter in s]
    return powerset

def get_solution(the_powerset, words_dict):
    solution_words = []
    for combi in the_powerset:
        try:
            solution_words.extend(words_dict[combi])
        except:
            pass

    solution_words = sorted(list(set([word for word in solution_words if len(word) >= 3])))
    print(solution_words)
    return solution_words

def save_solution(solution):

    today_date = datetime.today().strftime('%Y_%m_%d')

    file_name = 'solution_' + today_date + '.txt'
    textfile = open(file_name, "w")
    for element in solution:
        textfile.write(element + "\n")
    textfile.close()


set_of_letters = get_letters() #'ripevob' 
words_dict = make_dictionary()
power_set = powerset(set_of_letters)
solution = get_solution(power_set, words_dict)
save_solution(solution)


    

 

