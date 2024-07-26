# messages_to_images_and_back/main.py

import sys
import traceback

from cli import parse_arguments, process_action
from config import config
from logger_config import logger
from steganography import Steganographer


def main() -> None:
    """
    Основная функция приложения, которая обрабатывает командную строку или выполняет действия по умолчанию.
    """
    try:
        # Проверяем, были ли переданы аргументы командной строки.
        if len(sys.argv) > 1:
            # Если аргументы командной строки присутствуют, разбираем их и выполняем соответствующее действие.
            args = parse_arguments()
            process_action(args.action, args.image_path, args.message)

        else:
            # Если аргументы командной строки не переданы, выполняем действие по умолчанию.
            # Например, можно скрыть полезные данные во всех изображениях в входной директории.
            logger.info("No command-line arguments provided. Running default actions.")
            # Создаем объект Steganographer с использованием секретного ключа из конфигурации.
            steganographer = Steganographer(config.secret_key)

            # Используем значение по умолчанию для действия из конфигурации.
            action = config.default_action

            # Проверяем, если аргументы командной строки все же были переданы (хотя это и не должно быть здесь).
            if len(sys.argv) > 1:
                action = sys.argv[1]

            # Выполняем действие в зависимости от аргумента: 'hide' или 'extract'.
            if action == 'hide':
                # Если действие 'hide', обрабатываем файл по умолчанию для скрытия сообщения.
                steganographer.process_file(config.file_path, 'hide')
            elif action == 'extract':
                # Если действие 'extract', обрабатываем файл по умолчанию для извлечения сообщения.
                steganographer.process_file(config.file_path_out, 'extract')
            else:
                # Если передано неверное действие, выводим ошибку и завершает выполнение с кодом 1.
                logger.error("Invalid action. Use 'hide' or 'extract'.")
                sys.exit(1)

    except Exception as e:
        # Обрабатываем любые исключения, произошедшие в основной функции.
        detailed_error = traceback.format_exc()
        logger.error(f"Произошла ошибка в основной функции: {str(e)}\n{detailed_error}")


# Проверяем, является ли текущий модуль главным, и запускаем основную функцию.
if __name__ == "__main__":
    logger.info("Запуск приложения")
    try:
        main()
    except KeyboardInterrupt:
        # Ловим прерывание выполнения приложения пользователем (например, Ctrl+C).
        logger.warning("Приложение прервано пользователем")
    except Exception as error:
        # Обрабатываем любые исключения, произошедшие при запуске приложения.
        detailed_error = traceback.format_exc()
        logger.error(f"Непредвиденная ошибка в приложении: {error}\n{detailed_error}")
