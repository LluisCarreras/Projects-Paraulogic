import csv
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright



def get_letters():
    """
    Scrape letters from the Paraulogic webpage using Playwright.

    This function automates a browser using Playwright to extract letters displayed
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
    - The function assumes the structure of the Paraulogic webpage remains consistent.

    Example:
    --------
    If the letters on the webpage are:
        Center letter: "A"
        Surrounding letters: "B", "C", "D", "E", "F", "G"
    The function will return: "abcdefg"
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=True for background execution, or headless=False for debugging
        page = browser.new_page()
        url = "https://www.vilaweb.cat/paraulogic/"
        page.goto(url)

        # Wait for the elements to load
        page.wait_for_selector(".hex-in")

        # Find all the divs with class "hex-in"
        divs = page.locator(".hex-in")

        letters = []
        center_letter = None

        # Iterate through each div and extract the letter
        for i in range(divs.count()):
            div = divs.nth(i)
            letter = div.locator("p").inner_text()
            a_tag = div.locator(".hex-link")
            element_id = a_tag.get_attribute("id")
            if element_id == "center-letter":
                center_letter = letter
            letters.append(letter)

        # Format the letters
        if center_letter:
            letters.remove(center_letter)
            letters = [center_letter] + letters
        letters = ''.join(letters).lower()

        print("Extracted letters:", letters)

        browser.close()
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

def save_solution(solution, letters):
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
    filename_1 = 'solution_' + today_date + '.txt'
    filename_2 = 'solution.txt'

    # Create a platform-independent path
    path_1 = current_working_dir / folder / filename_1
    path_2 = current_working_dir / folder / filename_2
    
    # Save in txt file
    textfile = open(path_1, "w")
    letters_text = 'Letters: ' + letters
    textfile.write(letters_text + "\n")
    for element in solution:
        textfile.write(element + "\n")
    textfile.close()

    # Save in txt file
    textfile = open(path_2, "w")
    letters_text = 'Letters: ' + letters
    textfile.write(letters_text + "\n")
    for element in solution:
        textfile.write(element + "\n")
    textfile.close()

def get_solution_from_web():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=True for background execution, or headless=False for debugging
        page = browser.new_page()
        page.goto("https://www.vilaweb.cat/paraulogic/")  # Replace with the target URL

        # Execute JavaScript and retrieve the value of a variable
        js_variable_value = page.evaluate("window.t")  # Replace 'yourVariable' with the actual variable name

        browser.close()

        solution = list(js_variable_value['p'].keys())
        
        return solution


set_of_letters = get_letters() 

try:
    solution = get_solution_from_web()
    print("Gets solution from web...")
except:
    words_dict = make_dictionary()
    power_set = powerset(set_of_letters)
    solution = get_solution(power_set, words_dict)
    print("Gets solution from list...")
finally:
    save_solution(solution, set_of_letters)


    

 

