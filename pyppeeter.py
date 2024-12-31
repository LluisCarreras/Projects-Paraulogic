from requests_html import HTMLSession
from lxml.html.clean import Cleaner


url = 'https://www.vilaweb.cat/paraulogic/'


session = HTMLSession()
response = session.get(url)

# Render the JavaScript (wait=2 adjusts time for JS execution)
response.html.render(wait=2)

# Extract data
data = response.html.find('CSS_SELECTOR')  # Replace with the relevant CSS selector
for item in data:
    print(item.text)
