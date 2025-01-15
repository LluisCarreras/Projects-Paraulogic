from playwright.sync_api import sync_playwright


def scrape_page(words):
    try:
        with sync_playwright() as p:
            # Launch the browser and open the page
            browser = p.chromium.launch(headless=False)  # Set headless=True for non-UI mode
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
            content = page.content()
            
            browser.close()
            return content
        
    except Exception as e:
        print(f"An error occurred: {e}")

# List of words to submit
word_list = ['elemi', 'elm', 'multiple', 'pop']

# Save the HTML to a file
html_content = scrape_page(word_list)
with open("web_content.html", "w", encoding="utf-8") as file:
    file.write(html_content)



















