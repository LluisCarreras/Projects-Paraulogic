from playwright.sync_api import sync_playwright

def get_js_variable():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True for background execution
        page = browser.new_page()
        page.goto("https://www.vilaweb.cat/paraulogic/")  # Replace with the target URL

        # Execute JavaScript and retrieve the value of a variable
        js_variable_value = page.evaluate("window.t")  # Replace 'yourVariable' with the actual variable name

        browser.close()

        solution = js_variable_value['p'].keys()

        return solution
        

print(get_js_variable())










