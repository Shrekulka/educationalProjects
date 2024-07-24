# Instagram_scraper_instaloader – a tool for collecting and analyzing Instagram profile data using the Instaloader 
# library. The project allows for asynchronous retrieval of detailed profile data, saving it to files, and logging 
# information about them.

## Key Features:
1. Profile Data Retrieval: Extracts information about Instagram profiles, including the number of posts, followers, 
   followings, data about the latest post (including likes, comments, URL, and timestamp), as well as 
   additional parameters such as business category and presence of highlights.
2. Data Saving: Supports saving data in JSON and CSV formats.
3. Logging: Records information about the execution process and errors in log files.
4. Settings: Allows configuring delays between requests and data saving formats.

## Code Execution Sequence
1. Import Libraries and Configurations:
- Required libraries (asyncio, csv, json, random, traceback, datetime, and Instaloader) are imported.
- Settings and configurations from other modules (config, logger_config) are imported.

2. Define Functions:
- `format_timestamp(timestamp: int) -> str`: Formats timestamps into a readable format.
- `get_profile_data(username: str) -> Dict[str, Any]`: Asynchronously retrieves Instagram profile data.
- `get_all_profile_data(usernames: List[str]) -> List[Dict[str, Any]]`: Retrieves data for a list of users with 
  delays between requests.
- `log_profile_data(profile_data: Dict[str, Any]) -> None`: Logs profile information.
- `save_to_json(data: List[Dict[str, Any]], filename: str) -> None`: Saves data to a JSON file.
- `save_to_csv(data: List[Dict[str, Any]], filename: str) -> None`: Saves data to a CSV file.
- `main() -> None`: The main asynchronous function to start the data collection process, logging, and saving.

3. Run Main Code:
- `if __name__ == "__main__"`: Checks if the script is being run as the main program.
- `asyncio.run(main())`: Runs the main asynchronous function.
- Exceptions and errors are handled, with logging of them.

## Project Settings
Project settings are stored in `config.py` and can be configured via environment variables.

*Main settings include:*
1. Instagram Profiles List (`instagram_profiles`): A list of Instagram usernames for which data needs to be collected.
Example `.env`
```bash
INSTAGRAM_PROFILES=["Pupoc", "Basy"]
```
2. Data Saving Format (save_format): Format for saving data (json or csv).
3. Output File Name (output_file): Name of the file where data will be saved, including path.
4. Request Delay (min_delay and max_delay): Minimum and maximum delay between requests to prevent blocking.
5. Semaphore for limiting simultaneous requests (SEMAPHORE = asyncio.Semaphore(5)).

## Project Features
- Asynchronous Execution: Uses asynchronous programming for efficient request handling and data processing without
  blocking.
- Logging Configuration: Logger is set up to record important information and errors, aiding in debugging and monitoring.
- User Settings: The project supports flexible configuration through environment variables and configuration files.
- Error Handling: Built-in error handling to ensure robustness and reliability.

## Project Structure

```bash
📁 Instagram_scraper_instaloader/  # Root directory of the project
│
├── .env                           # File with environment variables
│
├── .gitignore                     # File indicating which files/folders Git should ignore
│
├── config.py                      # Project configuration and settings
│
├── log.py                         # Logger definitions and logging functions
│
├── logger_config.py               # Logger configuration for the project
│
├── main.py                        # Main script for running the application
│
├── profile.py                     # Module for handling Instagram profiles
│
├── README.md                      # Project documentation
│
├── requirements.txt               # List of Python dependencies for the project
│
├── save.py                        # Module for saving data (in JSON or CSV)
│
├── utils.py                       # Utility functions
│
└── 📁 venv/                       # Python virtual environment (usually ignored in .gitignore)
```