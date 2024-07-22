# Web Scraping Projects Description

Both projects use the Scrapy framework to gather data from the book store website "https://books.toscrape.com".

## Project 1: Collecting Basic Data from One Page (books)

### Project Goal
This project is designed to collect basic information about books from the main page and category pages of the website.

### Key Components
1. `books_crawl.py`:
   - The main spider file that defines the data collection logic.
   - Uses the `BooksCrawlSpider` class, which inherits from `scrapy.Spider`.
2. `parse` Method:
   - Processes each page with a list of books.
   - Extracts information about each book on the page.

This spider crawls through the website, collecting basic information about each book: image URL, title, and price.

### Features
- Collects data only from book listing pages.
- Does not navigate to individual book pages for additional information.
- Suitable for a quick overview of the catalog and prices.

## Project 2: Collecting Detailed Data from All Pages (books_pages)

### Project Goal
This project aims for a more in-depth data collection, including detailed information from individual book pages.

### Key Components
1. `pages_crawl.py`:
   - The main spider file using the `PagesCrawlSpider` class, which inherits from `CrawlSpider`.
   - Defines rules for navigating the website and collecting data.
2. Rules:
   - Determine how the spider should move through the site.
   - Include rules for accessing individual book pages and the next catalog pages.
3. `parse_item` Method:
   - Processes the individual book page.
   - Extracts detailed information about the book.

This spider is more complex. It uses rules to navigate through the site, accessing individual book pages and subsequent catalog pages. The `parse_item` method extracts detailed information about each book.

### Features
- Collects more detailed information about each book.
- Navigates through all catalog pages and visits each book page.
- Extracts additional data such as book description and UPC.
- Suitable for creating a comprehensive database of the books in the store.

### Application
- Project 1 is suitable for quick monitoring of prices and catalog.
- Project 2 is ideal for creating a complete database of books.

## Project Structure

```bash
📁 scraper_spider                                # Root directory of the project
│
├── 📁 books/                                    # Directory for the first spider (basic book data collection)
│   │
│   ├── 📁 books/                                # Main Scrapy project directory
│   │   │
│   │   ├── 📁 spiders/                          # Directory for Scrapy spiders
│   │   │   │
│   │   │   ├── __init__.py                      # Initialization file for the spiders package
│   │   │   │
│   │   │   └── books_crawl.py                   # Spider file for collecting book data
│   │   │
│   │   ├── __init__.py                          # Initialization file for the Scrapy package
│   │   │
│   │   ├── items.py                             # Definition of data structure for collection
│   │   │
│   │   ├── middlewares.py                       # Scrapy middleware settings
│   │   │
│   │   ├── pipelines.py                         # Data processing after collection
│   │   │
│   │   └── settings.py                          # Scrapy project settings
│   │
│   ├── books.csv                                # Output file with data in CSV format
│   │
│   ├── books.json                               # Output file with data in JSON format
│   │
│   └── scrapy.cfg                               # Configuration file for the Scrapy project
│   
├── 📁 books_pages/                              # Directory for the second spider (detailed book data collection)
│   │
│   ├── 📁 books_pages/                          # Main Scrapy project directory
│   │   │
│   │   ├── 📁 spiders/                          # Directory for Scrapy spiders
│   │   │   │
│   │   │   ├── __init__.py                      # Initialization file for the spiders package
│   │   │   │
│   │   │   └── pages_crawl.py                   # Spider file for collecting detailed book data
│   │   │
│   │   ├── __init__.py                          # Initialization file for the Scrapy package
│   │   │
│   │   ├── items.py                             # Definition of data structure for collection
│   │   │
│   │   ├── middlewares.py                       # Scrapy middleware settings
│   │   │
│   │   ├── pipelines.py                         # Data processing after collection
│   │   │
│   │   └── settings.py                          # Scrapy project settings
│   │
│   ├── books_pages.csv                          # Output file with detailed data in CSV format
│   │
│   ├── books_pages.json                         # Output file with detailed data in JSON format
│   │
│   └── scrapy.cfg                               # Configuration file for the Scrapy project
│   
├── .gitignore                                   # File specifying which files and directories to ignore by Git
│   
├── README.md                                    # File with project description, installation, and usage instructions
│                                            
└── requirements.txt                             # List of Python project dependencies
```