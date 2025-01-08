import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pathlib import Path
import shutil
import chromedriver_autoinstaller
from pyvirtualdisplay.display import Display
import platform





def get_webdriver():

    if platform.system() != "Windows":
        from pyvirtualdisplay.display import Display
        display = Display(visible=False, size=(800, 800))
        display.start()

    # Check if the current version of chromedriver exists
    chromedriver_autoinstaller.install()
    # and if it doesn't exist, download it automatically,
    # then add chromedriver to path

    chrome_options = webdriver.ChromeOptions()

    # Add your options as needed
    options = [
        # Define window size here
        "--window-size=1200,1200",
        "--ignore-certificate-errors"

        # "--headless",
        # "--disable-gpu",
        # "--window-size=1920,1200",
        # "--ignore-certificate-errors",
        # "--disable-extensions",
        # "--no-sandbox",
        # "--disable-dev-shm-usage",
        # '--remote-debugging-port=9222'
    ]

    for option in options:
        chrome_options.add_argument(option)


    driver = webdriver.Chrome(options=chrome_options)

    return driver

    

def get_letters():
    """
    Scrape letters from the Paraulogic webpage using Selenium.

    This function automates a browser using Selenium to extract letters displayed
    on the "https://www.vilaweb.cat/paraulogic/" webpage. The letters are retrieved 
    from `<div>` elements with the class `hex-in`. One of these letters is designated 
    as the "center letter," identified by having the `id="center-letter"` attribute 
    in its parent `<a>` tag.

    The function formats the letters so that the center letter appears first, 
    followed by the other letters, concatenates them into a single lowercase string, 
    and returns this string.

    Returns:
    --------
    str
        A single lowercase string of letters with the center letter as the first character.

    Notes:
    ------
    - Ensure you have Selenium installed (`pip install selenium`) and the appropriate 
      WebDriver for your browser (e.g., ChromeDriver for Google Chrome).
    - The function assumes the structure of the Paraulogic webpage remains consistent.

    Example:
    --------
    If the letters on the webpage are:
        Center letter: "A"
        Surrounding letters: "B", "C", "D", "E", "F", "G"
    The function will return: "abcdefg"
    """

    # Set up the Selenium WebDriver (e.g., ChromeDriver)
    driver = get_webdriver() 
    url = "https://www.vilaweb.cat/paraulogic/"
    driver.get(url)

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
    
    # Format the letters
    letters.remove(center_letter)
    letters = [center_letter] + letters
    letters = ''.join(letters) # type: ignore
    letters = letters.lower()
    print("Extracted letters:", letters)

    # Close the browser
    driver.quit()

    return letters


def make_dictionary():
    """
    Create a dictionary of words grouped by their unique, sorted letters.

    Reads a CSV file named `clean_words.csv` containing a list of words. For each word, 
    the function determines its unique set of letters (sorted alphabetically) and uses 
    this as the key in the dictionary. Words with the same set of unique letters are grouped 
    under the same key.

    Returns:
    --------
    dict
        A dictionary where:
        - Keys are strings representing unique, sorted letters of the words (e.g., "aelpr").
        - Values are lists of words from the CSV that match the key's letter set.

    Example:
    --------
    If the CSV contains:
        apple
        pear
        pale
        leap
        reap

    The resulting dictionary will be:
        {
            "aelpr": ["pale", "leap"],
            "aelp": ["apple"],
            "aepr": ["pear", "reap"]
        }

    Notes:
    ------
    - The function assumes the CSV has one word per row.
    - The input file `clean_words.csv` must exist in the same directory as the script.
    - Words are processed as lowercase and deduplicated by their letter set.
    """

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
    """
    Generate a powerset of the input set of letters, including only subsets 
    that contain the first letter of the input.

    The function computes all subsets of the given set of letters, sorts 
    each subset alphabetically, and filters the subsets to include only 
    those containing the first letter (`center_letter`).

    Args:
        set_of_letters (str): A string of unique letters. The first letter 
            in this string is considered the "center letter" and will 
            be included in all subsets in the resulting powerset.

    Returns:
        list[str]: A list of strings representing the subsets of 
            `set_of_letters` that include the `center_letter`. Each subset 
            is sorted alphabetically.
    
    Example:
        >>> powerset("abc")
        ['a', 'ab', 'ac', 'abc']
    """

    powerset = []
    center_letter = set_of_letters[0]
    set_of_letters = list(set_of_letters)
    len_set = len(set_of_letters)
    for i in range(1 << len_set):
        powerset.append([set_of_letters[j] for j in range(len_set) if (i & (1 << j))])
    powerset = [''.join((sorted(list(s)))) for s in powerset if center_letter in s]
    return powerset

def get_solution(the_powerset, words_dict):
    """
    Generate a list of solution words based on combinations in a powerset and a dictionary of words.

    Parameters:
    -----------
    the_powerset : list of str
        A list of strings representing all combinations of letters from a given set.
        Typically, this is the output of a powerset generation function.

    words_dict : dict
        A dictionary where keys are letter combinations (as strings) and values are lists of words
        that can be formed using those combinations.

    Returns:
    --------
    solution_words : list of str
        A list of words found in `words_dict` that match the combinations in `the_powerset`.
        Words from matching combinations are added to the result list.

    Notes:
    ------
    - If a combination from `the_powerset` is not found in `words_dict`, it is ignored.

    Example:
    --------
    powerset = ["abc", "abd", "acd"]
    words_dict = {"abc": ["cab", "bac"], "abd": ["bad", "dab"]}
    result = get_solution(powerset, words_dict)
    # result: ["cab", "bac", "bad", "dab"]
    """

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
    """
    Save the solution words to a text file with a timestamped filename.

    Parameters:
    -----------
    solution : list of str
        A list of solution words to be saved in the file. Each word is written as a new line.

    Behavior:
    ---------
    - The function generates a filename in the format `solution_YYYY_MM_DD.txt` where the date 
      corresponds to the day the function is executed.
    - Writes each element from the `solution` list as a new line in the file.

    Example:
    --------
    solution = ["word1", "word2", "word3"]
    save_solution(solution)
    # Creates a file named like `solution_2024_12_30.txt` containing:
    # word1
    # word2
    # word3
    """

    today_date = datetime.today().strftime('%Y_%m_%d')

    # Example path components
    # Get the current working directory
    current_working_dir = Path.cwd()
    folder = "solutions"
    filename = 'solution_' + today_date + '.txt'

    # Create a platform-independent path
    path = current_working_dir / folder / filename
    
    # Save in txt file
    textfile = open(path, "w")
    for element in solution:
        textfile.write(element + "\n")
    textfile.close()


set_of_letters = get_letters()  
words_dict = make_dictionary()
power_set = powerset(set_of_letters)
solution = get_solution(power_set, words_dict)
save_solution(solution)


    

 

