# Project Title: LEGO Scraper

## General Description
*LEGO Scraper* is a project for collecting data about LEGO sets from the official LEGO.com website. The project includes
two implementation options: a synchronous scraper (`sync_scraper`) and a multithreaded scraper (`thread_scraper`).

## Project Tasks
1. Collect information about LEGO themes (collections).
2. Extract data about each LEGO set within these themes.
3. Save the collected data into CSV files for further analysis.

## How the Project Works:

1. Loads the LEGO themes page.
2. Extracts a list of all available themes.
3. For each theme:
   - Loads the LEGO sets page for that theme.
   - Determines the number of pages of sets.
   - Iterates through each page and extracts information about the sets.
4. Aggregates all the information into a single list.
5. Saves the data into a CSV file.

## Features
- Two implementation options: synchronous and multithreaded.
- Handling and skipping of promotional blocks.
- Extraction of various set attributes: name, age, number of pieces, rating, price, discount, availability.
- Logging of process and errors.

## Project Settings are stored in `config/settings.py`:
- `CUSTOM_USER_AGENT`: Custom user agent for requests.
- `BASE_URL` and `THEME_URL`: Base URLs for the LEGO website.
- `DEFAULT_PAGE` and `DEFAULT_OFFSET`: Pagination parameters.
- Paths to CSV files for saving data.

# Sync Scraper

## Main Functions:
1. `get_page_content(page_url: str) -> bytes`: Retrieves the content of a page by URL.
2. `get_soup(base_url: str, page_number: int = config.DEFAULT_PAGE) -> bs`: Creates a BeautifulSoup object for parsing 
    HTML.
3. `get_themes(themes_page_soup)`: Extracts information about LEGO themes.
4. `get_toys_page(theme_page_soup)`: Retrieves the number of toys and pages for the theme.
5. `get_toys_data(toy_page_soup, theme_name="Marvel")`: Extracts data about LEGO sets from the page.

## Workflow:
1. Load the themes page.
2. Extract the list of themes.
3. Sequentially process each theme and page of sets.
4. Collect data on each set.
5. Save all data to a CSV file.

# Thread Scraper

## Main Functions:
1. `get_page_content(page_url: str) -> bytes`: Similar to `sync_scraper`.
2. `get_soup(base_url: str, page_number: int = config.DEFAULT_PAGE) -> bs`: Similar to `sync_scraper`.
3. `extract_themes(themes_page_soup: bs) -> List[Dict[str, str]]`: Extracts information about LEGO themes.
4. `extract_toy_count_and_pages(theme_page_soup: bs) -> Tuple[int, int]`: Retrieves the number of toys and pages for 
    the theme.
5. `extract_toys_from_page(toy_page_soup: bs, theme_name: str) -> List[Dict[str, Optional[str]]]`: Extracts data about
    LEGO sets from the page.
6. `process_theme(theme: Dict[str, str]) -> List[Dict[str, Optional[str]]]`: Processes a single theme completely.

## Workflow:
1. Load the themes page.
2. Extract the list of themes.
3. Create a thread pool.
4. Process each theme in a separate thread.
5. Aggregate the results from all threads.
6. Save all data to a CSV file.

## Features of `thread_scraper`:
- Uses `ThreadPoolExecutor` for concurrent theme processing.
- Can significantly speed up data collection, especially with a large number of themes and sets.

## Conclusion
This project provides a flexible tool for collecting data about LEGO sets. The synchronous version is simpler for 
debugging and suitable for small data volumes, while the multithreaded version offers higher performance when working 
with large datasets. The choice between them depends on specific needs and resources.

## Project Structure:

```bash
📁 lego_scraper/                      # Root directory of the project
│
├── 📁 src/                           # Application source code
│   │
│   ├── __init__.py                   # Initialization of the src package
│   │ 
│   ├── 📁 sync_scraper/              # Synchronous scraper module
│   │   │  
│   │   ├── __init__.py               # Initialization of the sync_scraper package
│   │   │ 
│   │   ├── main.py                   # Entry point for the synchronous scraper
│   │   │ 
│   │   ├── scraper.py                # Main logic for synchronous scraping
│   │   │ 
│   │   └── extractors.py             # Data extraction functions for sync_scraper
│   │
│   └── 📁 thread_scraper/            # Multithreaded scraper module
│       │ 
│       ├── __init__.py               # Initialization of the thread_scraper package
│       │ 
│       ├── main.py                   # Entry point for the multithreaded scraper
│       │ 
│       ├── scraper.py                # Main logic for multithreaded scraping
│       │ 
│       ├── processors.py             # Data processors for thread_scraper
│       │ 
│       └── extractors.py             # Data extraction functions for thread_scraper
│
├── 📁 data/                          # Directory for storing data
│   │
│   ├── all_toy_data_simple.csv       # Results from sync_scraper
│   │
│   └── all_toy_data_threads.csv      # Results from thread_scraper
│ 
├── 📁 config/                        # Configuration files
│   │
│   ├── __init__.py                   # Initialization of the config package
│   │
│   └── settings.py                   # Project settings
│ 
├── 📁 utils/                         # Utility scripts
│   │
│   ├── __init__.py                   # Initialization of the utils package
│   │
│   └── logger_config.py              # Logger configuration
│ 
├── .gitignore                        # Git ignore file
│ 
├── README.md                         # Project description
│ 
├── requirements.txt                  # Project dependencies
│ 
└── 📁 venv/                          # Python virtual environment
```