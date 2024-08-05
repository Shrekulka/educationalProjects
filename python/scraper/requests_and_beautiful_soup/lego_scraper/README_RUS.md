# Название проекта: LEGO Scraper

## Общее описание
*LEGO Scraper* - это проект для сбора данных о наборах LEGO с официального сайта LEGO.com. Проект включает в себя два 
варианта реализации: синхронный скрапер (sync_scraper) и многопоточный скрапер (thread_scraper).

## Задачи проекта
1. Сбор информации о темах (коллекциях) LEGO.
2. Извлечение данных о каждом наборе LEGO в рамках этих тем.
3. Сохранение собранных данных в CSV-файлы для дальнейшего анализа.

## Проект работает следующим образом:

1. Загружает страницу с темами LEGO.
2. Извлекает список всех доступных тем.
3. Для каждой темы:
   - Загружает страницу с наборами LEGO.
   - Определяет количество страниц с наборами.
   - Проходит по каждой странице и извлекает информацию о наборах.
4. Собирает всю информацию в единый список.
5. Сохраняет данные в CSV-файл.

## Особенности
- Два варианта реализации: синхронный и многопоточный.
- Обработка рекламных блоков и их пропуск.
- Извлечение различных атрибутов наборов: название, возраст, количество деталей, рейтинг, цена, скидка, доступность.
- Логирование процесса работы и ошибок.

## Настройки проекта хранятся в файле config/settings.py:
- CUSTOM_USER_AGENT: пользовательский агент для запросов.
- BASE_URL и THEME_URL: базовые URL для сайта LEGO.
- DEFAULT_PAGE и DEFAULT_OFFSET: параметры пагинации.
- Пути к CSV-файлам для сохранения данных.

# Sync Scraper (Синхронный скрапер)

## Основные функции:
1. get_page_content(page_url: str) -> bytes: Получает содержимое страницы по URL.
2. get_soup(base_url: str, page_number: int = config.DEFAULT_PAGE) -> bs: Создает объект BeautifulSoup для парсинга HTML.
3. get_themes(themes_page_soup): Извлекает информацию о темах LEGO.
4. get_toys_page(theme_page_soup): Получает количество игрушек и страниц для темы.
5. get_toys_data(toy_page_soup, theme_name="Marvel"): Извлекает данные о наборах LEGO с страницы.

## Последовательность работы:
1. Загрузка страницы с темами.
2. Извлечение списка тем.
3. Последовательный проход по каждой теме и странице с наборами.
4. Сбор данных о каждом наборе.
5. Сохранение всех данных в CSV-файл.

# Thread Scraper (Многопоточный скрапер)

## Основные функции:
1. get_page_content(page_url: str) -> bytes: Аналогично sync_scraper.
2. get_soup(base_url: str, page_number: int = config.DEFAULT_PAGE) -> bs: Аналогично sync_scraper.
3. extract_themes(themes_page_soup: bs) -> List[Dict[str, str]]: Извлекает информацию о темах LEGO.
4. extract_toy_count_and_pages(theme_page_soup: bs) -> Tuple[int, int]: Получает количество игрушек и страниц для темы.
5. extract_toys_from_page(toy_page_soup: bs, theme_name: str) -> List[Dict[str, Optional[str]]]: Извлекает данные о 
   наборах LEGO с страницы.
6. process_theme(theme: Dict[str, str]) -> List[Dict[str, Optional[str]]]: Обрабатывает одну тему целиком.

## Последовательность работы:
1. Загрузка страницы с темами.
2. Извлечение списка тем.
3. Создание пула потоков.
4. Параллельная обработка каждой темы в отдельном потоке.
5. Сбор результатов всех потоков.
6. Сохранение всех данных в CSV-файл.

## Особенности thread_scraper:
- Использует ThreadPoolExecutor для параллельной обработки тем.
- Может значительно ускорить процесс сбора данных, особенно при большом количестве тем и наборов.

## Заключение
Этот проект предоставляет гибкий инструмент для сбора данных о наборах LEGO. Синхронная версия проще в отладке и 
подходит для небольших объемов данных, в то время как многопоточная версия обеспечивает более высокую производительность
при работе с большими объемами данных. Выбор между ними зависит от конкретных потребностей и ресурсов.

## Структура проекта:

```bash
📁 lego_scraper/                      # Корневая директория проекта
│
├── 📁 src/                           # Исходный код приложения
│   │
│   ├── __init__.py                   # Инициализация пакета src
│   │ 
│   ├── 📁 sync_scraper/              # Модуль синхронного скрапера
│   │   │  
│   │   ├── __init__.py               # Инициализация пакета sync_scraper
│   │   │ 
│   │   ├── main.py                   # Точка входа для синхронного скрапера
│   │   │ 
│   │   ├── scraper.py                # Основная логика синхронного скрапинга
│   │   │ 
│   │   └── extractors.py             # Функции извлечения данных для sync_scraper
│   │
│   └── 📁 thread_scraper/            # Модуль многопоточного скрапера
│       │ 
│       ├── __init__.py               # Инициализация пакета thread_scraper
│       │ 
│       ├── main.py                   # Точка входа для многопоточного скрапера
│       │ 
│       ├── scraper.py                # Основная логика многопоточного скрапинга
│       │ 
│       ├── processors.py             # Обработчики данных для thread_scraper
│       │ 
│       └── extractors.py             # Функции извлечения данных для thread_scraper
│
├── 📁 data/                          # Директория для хранения данных
│   │
│   ├── all_toy_data_simple.csv       # Результаты работы sync_scraper
│   │
│   └── all_toy_data_threads.csv      # Результаты работы thread_scraper
│ 
├── 📁 config/                        # Конфигурационные файлы
│   │
│   ├── __init__.py                   # Инициализация пакета config
│   │
│   └── settings.py                   # Настройки проекта
│ 
├── 📁 utils/                         # Вспомогательные утилиты
│   │
│   ├── __init__.py                   # Инициализация пакета utils
│   │
│   └── logger_config.py              # Конфигурация логгера
│ 
├── .gitignore                        # Файл для игнорирования Git
│ 
├── README.md                         # Описание проекта
│ 
├── requirements.txt                  # Зависимости проекта
│ 
└── 📁 venv/                          # Виртуальное окружение Python
```