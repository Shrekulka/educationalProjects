# Instagram_scraper_instaloader/utils.py

from datetime import datetime


def format_timestamp(timestamp: int) -> str:
    """
    Форматирует timestamp в человекочитаемый формат времени.
    Args:
        timestamp: Timestamp в формате целого числа, представляющий время поста.
    Returns:
        Строка с отформатированным временем, прошедшим с момента поста.
    """
    # Проверяем, что timestamp имеет тип int
    if not isinstance(timestamp, int):
        return "Invalid timestamp"

    # Получаем текущее время
    now = datetime.now()

    # Преобразуем timestamp в объект datetime
    post_time = datetime.fromtimestamp(timestamp)

    # Вычисляем разницу между текущим временем и временем поста
    delta = now - post_time

    # Определяем количество полных лет, дней, часов, минут и секунд
    years = delta.days // 365                       # Определяем количество лет
    days = delta.days % 365                         # Определяем количество оставшихся дней
    hours, remainder = divmod(delta.seconds, 3600)  # Определяем количество часов и остаток секунд
    minutes, seconds = divmod(remainder, 60)        # Определяем количество минут и остаток секунд

    # Формируем список частей строки, представляющий прошедшее время
    parts = []
    if years > 0:
        parts.append(f"{years} years")      # Добавляем количество лет
    if days > 0:
        parts.append(f"{days} days")        # Добавляем количество дней
    if hours > 0:
        parts.append(f"{hours} hours")      # Добавляем количество часов
    if minutes > 0:
        parts.append(f"{minutes} minutes")  # Добавляем количество минут
    if seconds > 0:
        parts.append(f"{seconds} seconds")  # Добавляем количество секунд

    # Объединяем все части в одну строку и добавляем "ago" в конце
    return ", ".join(parts) + " ago"
