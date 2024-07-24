# Instagram_scraper_instaloader/main.py

import asyncio
import traceback

from config import config
from log import log_profile_data
from logger_config import logger
from profile import get_all_profile_data
from save import save_to_json, save_to_csv


async def main() -> None:
    """
    Основная асинхронная функция для сбора и сохранения данных профилей Instagram.

    1. Логирует запуск и собирает данные профилей с помощью `get_all_profile_data`.
    2. Логирует собранные данные с помощью `log_profile_data`.
    3. Сохраняет данные в формате JSON или CSV, если это указано в конфигурации.
    4. Обрабатывает и логирует любые возникшие исключения.
    5. Логирует завершение работы.
    """
    logger.info("Запуск основной функции")

    try:
        # Получаем данные профилей Instagram для списка пользователей
        profile_data_list = await get_all_profile_data(config.instagram_profiles)

        # Логируем данные профилей
        for profile_data in profile_data_list:
            log_profile_data(profile_data)

        # Проверяем, нужно ли сохранять данные
        if config.save_data:

            # Сохраняем данные в формате JSON, если указан формат "json"
            if config.save_format == "json":
                save_to_json(profile_data_list, config.output_file)

            # Сохраняем данные в формате CSV, если указан формат "csv"
            elif config.save_format == "csv":
                save_to_csv(profile_data_list, config.output_file)

    except Exception as e:
        detailed_error = traceback.format_exc()
        logger.error(f"Произошла ошибка в основной функции: {str(e)}\n{detailed_error}")

    finally:
        logger.info("Процесс завершен")


if __name__ == "__main__":
    logger.info("Запуск приложения")
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.warning("Приложение прервано пользователем")

    except Exception as error:
        detailed_error = traceback.format_exc()
        logger.error(f"Непредвиденная ошибка в приложении: {error}\n{detailed_error}")

    finally:
        logger.info("Завершение работы приложения")
