# first_steps_with_SQLite/logger.py

import logging
import sys
import traceback

from colorama import Style, Fore, Back


def configure_logging():
    try:
        level = logging.DEBUG

        log_format = (
            f'{Fore.MAGENTA}%(asctime)s{Style.RESET_ALL} | '
            f'{Back.GREEN + Style.BRIGHT + Fore.BLACK}%(lineno)04d-%(levelname)-7s{Style.RESET_ALL} | - | '
            f'{Fore.BLUE}%(name)s{Style.RESET_ALL} | - | '
            f'{Fore.GREEN}%(funcName)s{Style.RESET_ALL} | - | '
            f'{Style.BRIGHT + Fore.CYAN}%(message)s{Style.RESET_ALL} |'
        )

        logging.basicConfig(filename='val.log', format=log_format, filemode='a', level=level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(log_format))

        logging.getLogger().addHandler(console_handler)
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        logging.error(f"Error configuring logging: {e}\n{detailed_send_message_error}")
        sys.exit(1)  # Завершить программу в случае ошибки настройки логирования


configure_logging()

logger = logging.getLogger(__name__)
logger.info(f"{Back.BLUE + Style.BRIGHT + Fore.BLACK}HI! HI! HI!!!{Style.RESET_ALL}")
