cd /Users/user/Desktop/telegram_bot
python3 -m venv venv 
cd /Users/user/Desktop/telegram_bot/venv/bin/
source activate
pip install aiogram


1. Структура проекта:
```bash
non_functional telegram_bot/   # Основна папка проекта.
│
│
├── data_base/                              
│   ├── __init__.py                  
│   └── sqlite_db.py                 
│
├── handlers/                       
│   ├── __init__.py                   
│   ├── admin.py
│   ├── client.py
│   └── other.py
│
├── keyboards/
│   ├── __init__.py
│   ├── admin_kb.py
│   └── client_kb.py
│
├── bot_telegram.py
│
├── config.py
│
├── create_bot.py
│
├── inline.py
│                         
│
├── README.md
│
└── to_json.py
```