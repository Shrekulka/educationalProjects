python -m uvicorn main_api:app --host 127.0.0.1 --port 8000

Команда	                    | Описание
brew services start tor	    | Запустить Tor. Эта команда запускает Tor и регистрирует его как службу, которая будет автоматически стартовать при входе в систему.
brew services stop tor	    | Остановить Tor. Останавливает фоновую службу.
brew services restart tor	| Перезапустить Tor. Это самая полезная для вас команда. Она останавливает и снова запускает Tor, заставляя его построить новую цепочку узлов и получить новый IP-адрес.
brew services list	        | Проверить статус. Показывает список всех служб Homebrew и их состояние (started, stopped, error).

## Структура проекта:
```bash
📁 inter_exchange_arbitrage_bot/   # Корневая директория всего проекта
│
├── 📁 alembic/ ...                 
│
├── 📁 logs/                       # Логи приложения
│   └── __init__.py
│
├── 📁 scripts/                    # Скрипты для автоматизации
│   ├── __init__.py
│   ├── test-bybit-system.sh 
│   └── deployment.sh
│
├── 📁 src/                        # Основная директория с исходным кодом приложения
│   ├── __init__.py
│   │
│   ├── 📁 api/                    # API маршруты и схемы
│   │   ├── __init__.py
│   │   ├── api_router.py
│   │   ├── dependencies.py
│   │   ├── market_intel_router.py
│   │   ├── middleware.py
│   │   ├── news_router.py
│   │   ├── schemas.py  
│   │   └── system_router.py
│   │   
├── 📁 bot/                        # Telegram бот
│   │   ├── __init__.py
│   │   │ 
│   │   ├── 📁 filters/            # Фильтры для обработчиков
│   │   │   ├── __init__.py
│   │   │   └── admin_filter.py
│   │   │ 
│   │   ├── 📁 handlers/           # Обработчики команд и callback'ов
│   │   │   ├── __init__.py
│   │   │   ├── admin_handlers.py 
│   │   │   ├── news_handlers.py 
│   │   │   ├── scanner_handlers.py      
│   │   │   ├── settings_handlers.py  
│   │   │   └── user_handlers.py
│   │   │ 
│   │   ├── 📁 keyboards/          # Инлайн клавиатуры
│   │   │   ├── __init__.py
│   │   │   ├── admin_keyboards.py
│   │   │   ├── balance_keyboard.py
│   │   │   ├── coin_keyboards.py
│   │   │   ├── density_screener_keyboards.py
│   │   │   ├── main_menu_keyboard.py
│   │   │   ├── news_keyboards.py
│   │   │   ├── pagination_keyboard.py
│   │   │   ├── report_keyboards.py
│   │   │   ├── scanner_keyboard.py 
│   │   │   └── settings_keyboard.py
│   │   │ 
│   │   ├── 📁 lexicon/            # Словари с текстами
│   │   │   ├── __init__.py
│   │   │   └── lexicon_ru.py
│   │   │ 
│   │   ├── 📁 logic/              # Бизнес-логика бота
│   │   │   ├── __init__.py
│   │   │   ├── admin_logic.py
│   │   │   ├── balance_logic.py    
│   │   │   ├── density_logic.py
│   │   │   ├── greeting_logic.py
│   │   │   ├── menu_logic.py
│   │   │   ├── news_logic.py
│   │   │   ├── recon_logic.py
│   │   │   ├── report_maps.py
│   │   │   └── settings_logic.py
│   │   │ 
│   │   └── 📁 states/             # FSM состояния
│   │       ├── __init__.py
│   │       └── user_states.py
│   │    
│   ├── 📁 constants/              # Константы приложения
│   │   ├── __init__.py
│   │   ├── api_constants.py   
│   │   ├── prompts.py
│   │   ├── rate_limiting_constants.py
│   │   ├── service_constants.py
│   │   ├── system_constants.py
│   │   ├── telegram_constants.py 
│   │   ├── trading_constants.py       
│   │   └── trading_greetings.py  
│   │    
│   ├── 📁 core/                   # Основные конфигурации
│   │   ├── __init__.py
│   │   ├── config.py      
│   │   ├── database.py   
│   │   ├── enhanced_ai_resilience.py
│   │   ├── resilience.py
│   │   ├── scheduler.py
│   │   └── state.py
│   │   
│   ├── 📁 models/                 # Модели данных
│   │   ├── __init__.py
│   │   ├── arbitrage_attempt.py
│   │   ├── screener_models.py
│   │   ├── system_models.py    
│   │   ├── user_models.py   
│   │   └── user_settings.py
│   │   
│   ├── 📁 services/               # Сервисы для работы с внешними API
│   │   ├── __init__.py
│   │   ├── ai_trade_advisor_service.py
│   │   ├── api_health_checker.py
│   │   ├── arbitrage_report_service.py
│   │   ├── balance_service.py      
│   │   ├── blacklist_manager.py
│   │   ├── data_enricher_service.py
│   │   ├── density_chart_service.py
│   │   ├── density_screener_service.py
│   │   ├── dynamic_pairs_manager.py  
│   │   ├── enhanced_ai_processor_service.py
│   │   ├── exchange_service.py     
│   │   ├── market_data_service.py
│   │   ├── market_intelligence_service.py
│   │   ├── news_aggregator_service.py
│   │   ├── news_service.py
│   │   ├── notifier_service.py 
│   │   ├── proxy_manager.py
│   │   ├── reconnaissance_service.py
│   │   ├── report_formatter.py
│   │   ├── scanner_api_service.py     
│   │   ├── scanner_state_service.py
│   │   ├── service_manager.py   
│   │   └──📁 news_providers/                 
│   │      ├── __init__.py
│   │      ├── alphavantage_provider.py
│   │      ├── base_provider.py
│   │      ├── coincap_provider.py   
│   │      ├── coinmarketcap_provider.py
│   │      ├── cryptocompare_provider.py
│   │      ├── cryptopanic_provider.py
│   │      ├── diagnostic_wrapper.py
│   │      ├── messari_provider.py
│   │      └── newsapi_provider.py
│   │    
│   ├── 📁 strategies/             # Торговые стратегии
│   │   ├── __init__.py
│   │   ├── arbitrage_strategy.py 
│   │   ├── base_strategy.py 
│   │   └── enums.py
│   │    
│   └── 📁 utils/                  
│       ├── __init__.py
│       ├── api_error_handler.py
│       ├── app_lifecycle.py
│       ├── chat_actions.py  
│       ├── decorators.py
│       ├── exceptions.py
│       ├── helpers.py
│       ├── logger.py
│       └── metrics.py            
│   
├── .env.sample                    # Образец переменных окружения
├── .gitignore                     # Исключения для Git
├── alembic.ini
├── main_api.py                    # Точка входа для бота и API
├── requirements.txt               # Зависимости проекта
└── README.md                      # Документация
 ```