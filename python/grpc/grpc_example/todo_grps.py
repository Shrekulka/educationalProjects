
import asyncio
import traceback

from logger_config import logger
from services.todo_services import serve

# Точка входа в программу, запускаем сервер при выполнении скрипта.
if __name__ == '__main__':
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        logger.warning("Приложение прервано пользователем")
    except Exception as error:
        detailed_error = traceback.format_exc()
        logger.error(f"Неожиданная ошибка приложения: {error}\n{detailed_error}")
