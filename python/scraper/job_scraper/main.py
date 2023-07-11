# import time
# import urllib.parse
# import urllib.request
#
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
#
#
# def scrape_linkedin():
#     # Создание экземпляра драйвера браузера
#     driver = webdriver.Safari()
#
#     # Перейти на страницу входа в LinkedIn
#     driver.get('https://www.linkedin.com/login')
#
#     # Найти поле ввода для электронной почты
#     email_field = driver.find_element(By.ID, 'username')
#     email_field.send_keys('Shiko3232@gmail.com')
#
#     # Найти поле ввода для пароля
#     password_field = driver.find_element(By.ID, 'password')
#     password_field.send_keys('12061981Roman!')
#
#     # Отправить форму (нажать Enter)
#     password_field.send_keys(Keys.RETURN)
#
#     # Добавить небольшую задержку для завершения авторизации
#     time.sleep(2)
#
#     # Параметры запроса для поиска вакансий
#     params = {
#         "keywords": "Python",
#         "location": "Ukraine, Europe",
#         "remote": "true"  # Указываем, что ищем удаленные вакансии
#     }
#
#     # Отправка GET-запроса на LinkedIn с заданными параметрами и заголовками
#     url = 'https://www.linkedin.com/jobs/search/?' + urllib.parse.urlencode(params)
#     req = urllib.request.Request(url)
#     req.add_header("User-Agent",
#                    "Mozilla/5.0 (Macintosh; Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36")
#
#     req.add_header("Accept-Language", "ru-RU,ru;q=0.9,en-US,en;q=0.8")
#     response = urllib.request.urlopen(req)
#     page_data = response.read().decode("utf-8")
#
#     soup = BeautifulSoup(page_data, "html.parser")
#     job_elements = soup.find_all("li", class_="result-card")
#
#     for job_element in job_elements:
#         title = job_element.find("h3", class_="result-card__title").text.strip()
#         company = job_element.find("h4", class_="result-card__subtitle").text.strip()
#         location = job_element.find("span", class_="job-result-card__location").text.strip()
#         print(f"Title: {title}\nCompany: {company}\nLocation: {location}\n")
#         time.sleep(2)  # Добавляем задержку в 2 секунды между запросами
#
#     # Закрыть браузер
#     driver.quit()
#
#
# scrape_linkedin()


import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, OnSiteOrRemoteFilters

# Change root logger level (default is WARN)
logging.basicConfig(level=logging.INFO)


# Fired once for each successfully processed job
def on_data(data: EventData):
    print('[ON_DATA]', data.title, data.company, data.company_link, data.date, data.link, data.insights, len(data.description))


# Fired once for each page (25 jobs)
def on_metrics(metrics: EventMetrics):
    print('[ON_METRICS]', str(metrics))


def on_error(error):
    print('[ON_ERROR]', error)


def on_end():
    print('[ON_END]')


scraper = LinkedinScraper(
    chrome_executable_path=None,  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
    chrome_options=None,  # Custom Chrome options here
    headless=True,  # Overrides headless mode only if chrome_options is None
    max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
    slow_mo=0.5,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
    page_load_timeout=40  # Page load timeout (in seconds)
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

queries = [
    Query(
        options=QueryOptions(
            limit=27  # Limit the number of jobs to scrape.
        )
    ),
    Query(
        query='Engineer',
        options=QueryOptions(
            locations=['United States', 'Europe'],
            apply_link=True,  # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page must be navigated. Default to False.
            skip_promoted_jobs=True,  # Skip promoted jobs. Default to False.
            page_offset=2,  # How many pages to skip
            limit=5,
            filters=QueryFilters(
                company_jobs_url='https://www.linkedin.com/jobs/search/?f_C=1441%2C17876832%2C791962%2C2374003%2C18950635%2C16140%2C10440912&geoId=92000000',  # Filter by companies.
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.MONTH,
                type=[TypeFilters.FULL_TIME, TypeFilters.INTERNSHIP],
                on_site_or_remote=[OnSiteOrRemoteFilters.REMOTE],
                experience=[ExperienceLevelFilters.MID_SENIOR]
            )
        )
    ),
]

scraper.run(queries)
