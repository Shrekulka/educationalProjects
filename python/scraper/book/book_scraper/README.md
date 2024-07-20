# 1. single_page_scraper.py

## Purpose:
This script is designed to extract book information from a single page of the website "https://books.toscrape.com/".

## Structure and Operation:
- Import necessary libraries (requests, BeautifulSoup, logger).
- Define the constant BOOKS_URL with the target page address.
- Main function `main()`:
    - Send a GET request to the target page.
    - Parse HTML content using BeautifulSoup.
    - Find and extract book information (image, title, price).
    - Save book data in a list of dictionaries.
    - Log the process and results.
- Exception handling for error resilience.

## Features:
- Works with only one page.
- Detailed logging of each step.
- Extracts basic book information (image, title, price).

# 2. multi_page_scraper.py

## Purpose:
This script is designed to extract book information from all pages of the catalogue on the website 
"https://books.toscrape.com/catalogue/".

## Structure and Operation:
- Import necessary libraries.
- Define constants (BASE_URL, START_URL, USER_AGENT).
- Functions:
    - `get_page_content()`: Retrieve HTML content of a page.
    - `parse_books()`: Extract book data from a single page.
    - `get_next_page_url()`: Find the URL of the next page.
    - `main()`: Main function managing the scraping process.
- Loop in `main()` to traverse all pages of the catalogue.
- Exception handling for error resilience.

## Features:
- Handles multiple pages of the catalogue.
- Uses User-Agent to simulate a browser.
- More structured code with function separation.
