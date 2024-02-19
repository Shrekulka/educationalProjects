# simple_echo_bot/bot_telegram.py

from create_bot import dp, bot

# Регистрация обработчиков для клиента
from handlers import client
client.register_handlers_client(dp)


# Если файл запускается непосредственно, а не импортируется как модуль, то запускается бот с использованием polling
if __name__ == "__main__":
    dp.run_polling(bot)
