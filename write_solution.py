from playwright.sync_api import sync_playwright
import re
import csv


def scrape_page(words):
    try:
        with sync_playwright() as p:
            # Launch the browser and open the page
            browser = p.chromium.launch(headless=True)  
            context = browser.new_context()
            page = context.new_page()

            # Navigate to the webpage
            url = "https://www.vilaweb.cat/paraulogic/"  
            page.goto(url)

            # Automate the process for each word in the list
            for word in words:
                # Write the word into the <p> element
                page.evaluate(f"""
                    document.getElementById('test-word').textContent = '{word}';
                """)
                
                # Click the submit button
                page.click('#submit-button')

                # Optional: Add a short delay between submissions if needed
                page.wait_for_timeout(500)  # Wait 0.5 seconds (adjust as needed)

           
            # Wait for the page to load fully
            page.wait_for_load_state("networkidle")
            
            # Get the full HTML content of the page
            #content = page.content()

            # Extract the content of the <ul> with id "hex-grid"
            ul_content = page.locator("ul#hex-grid").inner_html()

            # Extract the content of the <div> with the specified class
            div_content = page.locator("div.scoreboard").inner_html()

            # Define the regular expression pattern
            pattern_1 = r"<div>(.*?)</div>"
            
            # Search for the pattern in the input text
            div_content_txt = re.search(pattern_1, div_content).group(0)

            # Regular expression pattern to match the onclick attribute
            pattern_2 = r' onclick(.*?)false\);"'
             
            # Clean all matches
            clean_div_content = re.sub(pattern_2, '', div_content_txt)

            score = page.locator("div#score").inner_html()
            
            browser.close()
            return ul_content, clean_div_content, score
        
    except Exception as e:
        print(f"An error occurred: {e}")
        #return None, None

# List of words to submit
word_lt = []

file_path = 'solutions/solution.txt'

# Read the CSV file
with open(file_path, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        word_lt.append(row[0])

word_lt = word_lt[1:]
print(word_lt)

ul_content, div_content, score = scrape_page(word_lt)
print(div_content)

nl = '\n'

html = '''<!DOCTYPE html><html lang="ca"><head>
  <title>Solució del Paraulògic</title>
  <meta charset="utf-8">
  <style>
    p,
    ul {
      margin: 0;
      padding: 0
    }

    h1, h3 {
        text-align: center;
    }

    body {
      margin: 0 auto;
      max-width: 800px;
      display: flex;
      flex-direction: column;
      font-family: 'Open Sans', sans-serif;
      line-height: 30px;
      position: relative;
      color: #000;
      background: #fff
    }

    body.dark {
      color: #fff;
      background: #212529
    }

    body.book {
      background: #ebf7fd
    }

    body.quadern {
      background: #ebf7fd
    }

    body,
    html {
      touch-action: manipulation
    }

    a {
      color: #000;
      background-color: transparent;
      text-decoration: none;
      font-weight: bolder
    }

    .dark a {
      color: #fff
    }

    a:hover {
      text-decoration: underline
    }

    b,
    strong {
      font-weight: bolder
    }

    .scoreboard {
      display: flex;
      justify-content: center;
      flex-direction: column;
      margin-bottom: 20px
    }

    .scoreboard>div {
      align-self: center;
      line-height: 1.5;
      margin: 4px 20px
    }

    .pangrama #stars {
      color: #fc0
    }

    span.pangrama {
      font-weight: bolder;
      color: #ec4a49
    }

    #definition,
    .sol-def {
      font-size: 10pt;
      font-family: Verdana, Geneva, Tahoma, sans-serif;
      margin-top: 0;
      margin-bottom: 10px
    }

    #definition a,
    .sol-def a {
      cursor: initial;
      text-decoration: none
    }

    .title {
      font-weight: 700
    }

    #definition h3,
    .sol-def h3 {
      font-weight: 400;
      font-size: 14px;
      color: #e3282a
    }

    .scoreboard div.copyright {
      margin-bottom: 20px
    }

    #hex-grid {
      display: grid;
      grid-gap: 6px;
      grid-template-columns: repeat(6, 2fr);
      padding-bottom: 30px;
      width: 250px;
      margin: 0 auto;
      font-size: .9em;
      list-style-type: none;
      overflow: hidden
    }

    .container-hexgrid {
      display: flex;
      flex-direction: column;
      align-items: center;
      z-index: 0
    }

    .hex {
      grid-column-end: span 2;
      position: relative;
      user-select: none;
      pointer-events: none
    }

    .hex::after {
      content: '';
      display: block;
      padding-bottom: 86.602%
    }

    .hex p {
      text-transform: uppercase;
      width: 100%;
      padding: 38%;
      box-sizing: border-box;
      font-size: 1.4em;
      color: #000
    }

    .hex #center-letter p {
      color: #fff
    }

    .hex-in {
      position: absolute;
      width: 100%;
      padding-bottom: 115.47%;
      overflow: hidden;
      transform: rotate3d(0, 0, 1, -60deg) skewY(30deg);
      pointer-events: none
    }

    .hex-in * {
      position: absolute
    }

    #center-letter {
      background-color: #ec4a49
    }

    .hex-link {
      display: block;
      width: 100%;
      height: 100%;
      text-align: center;
      background-color: #63bcca;
      overflow: hidden;
      transform: skewY(-30deg) rotate3d(0, 0, 1, 60deg);
      outline: 0;
      pointer-events: auto;
      cursor: pointer;
      -webkit-tap-highlight-color: transparent
    }

    .hex-link:not(.no-pointer):focus p,
    .hex-link:not(.no-pointer):hover p {
      box-shadow: inset 0 0 100px 100px rgba(255, 255, 255, .1)
    }

    .hex:nth-child(5n+1) {
      grid-column-start: 2
    }

    .hex:nth-child(5n+3) {
      grid-column-start: 1
    }

    #test-word {
      text-align: center
    }

    #message {
      position: absolute;
      background-color: #ec4a49;
      color: #fff;
      border-radius: 3px;
      padding: 5px;
      z-index: 100;
      pointer-events: none
    }

    .message-ok {
      background-color: #63bcca !important
    }

    .hide {
      opacity: 0;
      transition: opacity 1.5s
    }

    .hide-initial {
      opacity: 0
    }

    .message-shake {
      animation: shake .4s cubic-bezier(.36, .07, .19, .97) both;
      transform: translate3d(0, 0, 0);
      backface-visibility: hidden;
      perspective: 1000px
    }

    @keyframes shake {

      25%,
      75% {
        transform: translate3d(1px, 0, 0)
      }

      50% {
        transform: translate3d(0, 0, 0)
      }
    } 
  </style>
</head>
<body class="pangrama">
<h1>Solució del Paraulògic</h1>
<br>
<h3>En aquesta pàgina es mostra la solució del <a href="https://www.vilaweb.cat/paraulogic/">Paraulògic</a> del dia actual.</h3>
<br>
  <div class="container-hexgrid">
    <ul id="hex-grid">
'''
html += ul_content
html += nl + '''</ul>
</div>
<div class="scoreboard">
'''
html += div_content
html += nl + '<div id="score">'
html += score 
html += '''</div>
</div>
</body>
</html>'''


# File path where the HTML content will be saved
file_path = "parau.html"

# Save the string to a file
with open(file_path, "w", encoding="utf-8") as file:
    file.write(html)

print(f"HTML content saved to {file_path}")


















