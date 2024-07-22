# 1. loging.py

## Purpose:
This script is designed for automated login to a website using Selenium WebDriver. 
It demonstrates the process of authentication on the site and retrieving page content after a successful login.

## Workflow:
1. Initialize the driver using the setup_driver() function from the common module.
2. Open the login page specified in the configuration.
3. Wait for the username input element to load.
4. Find the login form elements (username field, password field, and login button).
5. Enter the credentials from the configuration.
6. Click the login button.
7. Wait for the page to load after logging in.
8. Retrieve and log the page source.
9. Handle possible exceptions.
10. Close the web driver.

## Features:
- Uses the logging module for detailed logging of actions and errors.
- Applies explicit waits (WebDriverWait) to enhance script reliability.
- Handles exceptions and provides detailed error information.
- Uses a configuration file to store settings.

## Settings (config.py):
The config.py file uses the pydantic library for creating and validating configuration data. 
Pydantic is a powerful Python library for handling data, which provides runtime data type validation and an easy way to 
work with application settings.

1. *Login page URL (login_url):*
    ```python
    login_url: str = 'https://quotes.toscrape.com/login'
    ```
    This is the address of the web page where the login form is located. The script will use this URL to navigate to the
    authentication page.

2. *Username and password:*
    ```python
    username: str
    password: SecretStr
    ```
    These fields are used to store credentials. Note that the password is stored as SecretStr - a special pydantic data 
    type that provides additional security by hiding the password value when outputted or logged.

3. *Path to geckodriver:*
    ```python
    geckodriver_path: str = './geckodriver'
    ```
    This is the path to the geckodriver executable required for Selenium to work with Firefox. Geckodriver is the driver
    that allows Selenium to interact with Firefox.

4. *Web driver settings:*
    ```python
    headless_mode: bool = True
    disable_cache: bool = True
    tracking_protection: bool = True
    custom_user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
    ```
      - headless_mode: If True, the browser runs in the background without a graphical interface, which is useful for 
        automation and server use.
      - disable_cache: If True, disables browser caching, which can be useful for getting fresh data with each request.
      - tracking_protection: If True, enables tracking protection in the browser.
      - custom_user_agent: Allows setting a custom User-Agent, which can help in bypassing some website restrictions.

5. *Additional settings:*
    ```python
    infinite_scroll_url: str = 'https://quotes.toscrape.com/scroll'
    min_pause_time: float = 1.2
    max_pause_time: float = 2.5
    ```
    - infinite_scroll_url: URL of the page with infinite scrolling for the infinite_scroll_scraper.py script.
    - min_pause_time and max_pause_time: Define the range of time for random pauses between actions, helping to mimic 
      human behavior and avoid site blocking.

6. *Loading settings from an environment file:*
    ```python
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    ```
    This configuration allows loading values from a .env file, which is a secure way to store sensitive data like 
    passwords and API keys.

#### Using pydantic for configuration provides several benefits:
- Automatic data type validation.
- Ability to set default values.
- Easy loading of data from environment variables or .env files.
- Secure storage of secret data using SecretStr.

## Web driver setup (common.py): 
The common.py file contains the setup_driver() function, which is responsible for configuring and initializing the 
Firefox web driver with extended options. This function plays a key role in preparing the browser for web scraping tasks.

### Key components and settings:
1. *Initializing Service and Options:*
    ```python
    service = Service(config.geckodriver_path)
    options = Options()
    ```
    - Service is used to specify the path to geckodriver.
    - Options allows configuring the browser's behavior.

2. *Configuring operation mode:*
    ```python
    if config.headless_mode:
        options.add_argument('-headless')
    ```
    Headless mode allows running the browser without a graphical interface, which is useful for automation and server use.

3. *Security and stability settings:*
    ```python
    options.add_argument('-no-sandbox')
    options.add_argument('-disable-dev-shm-usage')
    ```
    These settings improve browser stability, especially in containerized environments.

4. *Cache management:*
    ```python
    if config.disable_cache:
        options.set_preference('browser.cache.disk.enable', False)
        options.set_preference('browser.cache.memory.enable', False)
        # ...
    ```
    Disabling cache can be useful for getting fresh data with each request.

5. *Privacy settings:*
    ```python
    if config.tracking_protection:
        options.set_preference('privacy.trackingprotection.enabled', True)
        options.set_preference('privacy.donottrackheader.enabled', True)
    ```
    These settings enhance privacy during web scraping.

6. *Disabling notifications and pop-ups:*
    ```python
    options.set_preference('dom.webnotifications.enabled', False)
    options.set_preference('dom.push.enabled', False)
    options.set_preference('dom.disable_open_during_load', True)
    ```
    These settings prevent unwanted elements that may interfere with scraping.

7. *Performance optimization:*
    ```python
    options.set_preference('browser.tabs.remote.autostart', False)
    options.set_preference('media.autoplay.default', 0)
    options.set_preference('webgl.disabled', True)
    ```
    These settings help reduce resource usage and improve performance.

8. *Configuring User-Agent:*
    ```python
    if config.custom_user_agent:
        options.set_preference('general.useragent.override', config.custom_user_agent)
    ```
    Setting a custom User-Agent can help in bypassing some website restrictions.

9. *Localization:*
    ```python
    options.set_preference('intl.accept_languages', 'ru-RU,ru')
    options.set_preference('general.useragent.locale', 'ru-RU')
    ```
    These settings simulate a browser with Russian localization.

10. *Creating and returning the web driver:*
    ```python
    return webdriver.Firefox(service=service, options=options)
    ```
    The function returns a fully configured Firefox web driver object.

Using common.py allows centralizing web driver settings, ensuring configuration consistency across different scripts 
(loging.py and infinite_scroll_scraper.py). This simplifies maintenance and modification of settings as all changes can
be made in one place.

# 2. infinite_scroll_scraper.py

## Purpose:
This script is designed for scraping web pages with infinite scrolling. It automatically scrolls the page until all 
content is loaded, then counts the number of loaded items.

## Workflow:
1. Initialize the driver using the setup_driver() function from the common module.
2. Open the infinite scrolling page specified in the configuration.
3. Wait for the first element on the page to load.
4. Scroll the page in a loop:
   - Scroll to the end of the current page.
   - Pause for new content to load.
   - Check if the page height has changed (indicating new data).
5. Count the number of loaded items.
6. Log the results.
7. Handle possible exceptions.
8. Close the web driver.

## Features:
- Uses random pauses between scrolls to mimic human behavior.
- Checks page height changes to determine the end of content.
- Logs the number of loaded items.
- Handles exceptions, including user interruptions.

## Settings:
Similarly to loging.py, settings are loaded from config.py. Additional settings include:
- URL of the infinite scrolling page
- Minimum and maximum pause times between scrolls

Both programs use the common setup_driver() module from common.py, which configures the Firefox web driver with extended
options such as headless mode, cache disabling, privacy settings, and performance enhancements.
These scripts demonstrate an effective approach to web scraping using Selenium, including handling authentication and
dynamically loaded content.

## Project Structure:

```bash
📁 selenium/                      # Root directory of the project
│
├── .env                          # Environment file (logins, passwords)
│
├── .gitignore                    # File indicating which files/folders Git should ignore
│
├── common.py                     # Common functions, including web driver setup
│
├── config.py                     # Configuration file with project settings
│
├── geckodriver                   # Executable file of geckodriver for managing Firefox
│
├── infinite_scroll_scraper.py    # Script for scraping pages with infinite scrolling
│
├── logger_config.py              # Logger configuration for the project
│
├── loging.py                     # Script for automated login to a website
│
├── README.md                     # Project documentation, installation, and usage instructions
│
├── requirements.txt              # List of Python dependencies for the project
│
└── 📁 venv/                      # Python virtual environment (usually ignored in .gitignore)  
```