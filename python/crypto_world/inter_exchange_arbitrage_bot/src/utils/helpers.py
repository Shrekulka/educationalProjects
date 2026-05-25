# inter_exchange_arbitrage_bot/src/utils/helpers.py
import re
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Tuple, List, Union
from typing import Optional

import httpx

from src.constants.api_constants import COINGECKO_SYMBOL_ALIASES
from src.core.config import config, BaseExchangeConfig, KuCoinConfig
from src.utils.logger import logger


def safe_get_numeric(data: Any, key: str, default: float = 0.0) -> float:
    """
    Безопасно извлекает числовое значение из словаря.
    Если data не является словарем или ключ отсутствует/неконвертируем, возвращает default.
    """
    # Проверяем, что нам вообще передали словарь. Если нет - сразу выходим.
    if not isinstance(data, dict):
        return default

    try:
        value = data.get(key)
        if value is None:
            return default
        return float(value)
    except (ValueError, TypeError):
        return default


def calculate_profit_metrics(buy_cost: float, sell_revenue: float) -> Tuple[float, float]:
    """
    Расчет метрик прибыльности

    Args:
        buy_cost: Стоимость покупки
        sell_revenue: Выручка от продажи

    Returns:
        Tuple[float, float]: (чистая_прибыль, roi_процент)
    """
    if buy_cost <= 0:
        return 0.0, 0.0

    net_profit = sell_revenue - buy_cost
    roi_percent = (net_profit / buy_cost) * 100

    return net_profit, roi_percent


def validate_trade_amount(amount: float, min_amount: float, max_amount: float) -> Tuple[bool, str]:
    """
    Валидация суммы сделки

    Args:
        amount: Проверяемая сумма
        min_amount: Минимальная сумма
        max_amount: Максимальная сумма

    Returns:
        Tuple[bool, str]: (валидна, сообщение_об_ошибке)
    """
    if amount < min_amount:
        return False, f"Сумма слишком мала. Минимум: ${min_amount:,.2f}"

    if amount > max_amount:
        return False, f"Сумма слишком велика. Максимум: ${max_amount:,.2f}"

    return True, ""


def format_precision_amount(amount: float, precision: int) -> float:
    """
    Форматирование суммы с учетом точности биржи

    Args:
        amount: Исходная сумма
        precision: Количество знаков после запятой

    Returns:
        float: Отформатированная сумма
    """
    from decimal import ROUND_DOWN

    if precision <= 0:
        return float(int(amount))

    decimal_amount = Decimal(str(amount))
    precision_decimal = Decimal('0.1') ** precision

    formatted = decimal_amount.quantize(precision_decimal, rounding=ROUND_DOWN)
    return float(formatted)


def get_number_emoji(n: int) -> str:
    """Возвращает эмодзи для чисел от 1 до 10."""
    emojis = {
        1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣",
        6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "🔟"
    }
    return emojis.get(n, "🔹")


def get_configured_exchanges() -> list[str]:
    """
    Динамически сканирует объект config и возвращает список названий бирж,
    для которых есть корректная конфигурация (API ключи и т.д.).

    УЛУЧШЕННАЯ ВЕРСИЯ: Автоматически определяет конфигурации бирж
    без хардкода списков исключений.
    """
    configured_exchanges = []
    logger.debug("🔍 Начинаю сканирование конфигурации бирж...")

    for attr_name in dir(config):
        # Игнорируем служебные атрибуты Python
        if attr_name.startswith('_'):
            continue
        try:
            exchange_config_instance = getattr(config, attr_name, None)
            logger.debug(f"📊 Проверяю атрибут '{attr_name}': type={type(exchange_config_instance).__name__}")

            # Проверяем, что это не None
            if exchange_config_instance is None:
                logger.debug(f"⏭️ {attr_name}: конфигурация не установлена (None)")
                continue

            # Проверяем принадлежность к BaseExchangeConfig БЕЗ логирования "ошибок"
            if not isinstance(exchange_config_instance, BaseExchangeConfig):
                # Просто молча пропускаем - это нормально для network, tg_bot, db и т.д.
                continue

            # Дополнительные проверки для конфигураций бирж
            if not hasattr(exchange_config_instance, 'api_key') or not hasattr(exchange_config_instance, 'api_secret'):
                logger.debug(f"❌ {attr_name}: отсутствуют обязательные поля api_key/api_secret")
                continue

            if (not exchange_config_instance.api_key or not exchange_config_instance.api_secret or
                    not exchange_config_instance.api_key.strip() or not exchange_config_instance.api_secret.strip()):
                logger.debug(f"❌ {attr_name}: пустые api_key или api_secret")
                continue

            # Специальная, типобезопасная проверка для KuCoin
            if isinstance(exchange_config_instance, KuCoinConfig):
                # Проверяем и наличие, и заполненность passphrase для KuCoin
                if not hasattr(exchange_config_instance,
                               'api_passphrase') or not exchange_config_instance.api_passphrase:
                    logger.warning(f"❌ {attr_name} (KuCoin): пропущено из-за отсутствия обязательного api_passphrase.")
                    continue

            # Успешно прошли все проверки
            configured_exchanges.append(attr_name)
            logger.debug(f"✅ {attr_name}: конфигурация корректна")

        except Exception as e:
            logger.warning(f"⚠️ Ошибка при проверке конфигурации {attr_name}: {e}")
            continue

    logger.info(f"🎯 Найдено {len(configured_exchanges)} настроенных бирж: {configured_exchanges}")

    if not configured_exchanges:
        logger.critical("⚠️ НЕ НАЙДЕНО НИ ОДНОЙ НАСТРОЕННОЙ БИРЖИ!")
        logger.critical("Проверьте .env файл и API ключи")

    return configured_exchanges


async def get_public_ip() -> str | None:
    """Получает текущий внешний IP-адрес с помощью внешнего сервиса."""
    try:
        # Используем надежный и простой сервис api.ipify.org
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.ipify.org?format=json")
            response.raise_for_status()  # Вызовет ошибку, если статус не 2xx
            return response.json().get("ip")
    except Exception as e:
        logger.error(f"Не удалось определить публичный IP-адрес: {e}")
        return None


def create_progress_bar(progress: float, total: float, length: int = 10) -> str:
    """
    Создает текстовую строку прогресс-бара.
    Пример: [████░░░░░░]
    """
    if total <= 0:
        return f"[{'░' * length}]"

    percent = progress / total
    filled_length = int(length * percent)
    bar = '█' * filled_length + '░' * (length - filled_length)
    return f"[{bar}]"


def split_long_message(text: str, max_length: int) -> List[str]:
    """
    Разделяет длинный текст на части, не превышающие max_length,
    стараясь не разрывать строки.
    """
    if len(text) <= max_length:
        return [text]

    messages = []
    current_chunk = ""
    lines = text.split('\n')

    for line in lines:
        # Проверяем, не превысит ли добавление новой строки лимит
        if len(current_chunk + line + "\n") > max_length:
            # Если превысит, и в чанке что-то есть - сохраняем его
            if current_chunk:
                messages.append(current_chunk.strip())
            # Начинаем новый чанк с текущей строки
            current_chunk = line + "\n"
        else:
            # Иначе просто добавляем строку в текущий чанк
            current_chunk += line + "\n"

    # Не забываем добавить последний оставшийся чанк
    if current_chunk.strip():
        messages.append(current_chunk.strip())

    return messages


def build_caption_and_remainder(lines: List[str], max_length: int) -> Tuple[str, str]:
    """
    Собирает текст для подписи из списка строк, не превышая лимит.
    Возвращает кортеж (текст_для_подписи, оставшийся_текст).
    """
    caption_lines = []
    current_length = 0

    # Находим индекс строки, на которой происходит превышение лимита
    split_index = -1
    for i, line in enumerate(lines):
        # +1 для символа переноса строки
        if current_length + len(line) + 1 > max_length:
            split_index = i
            break
        caption_lines.append(line)
        current_length += len(line) + 1

    caption_part = "\n".join(caption_lines)

    if split_index != -1:
        # Если было разделение, оставшиеся строки идут в remainder
        remainder_part = "\n".join(lines[split_index:])
    else:
        # Если весь текст поместился, остатка нет
        remainder_part = ""

    return caption_part, remainder_part


def get_prioritized_search_results(all_items: List[str], search_queries: Union[str, List[str]]) -> List[str]:
    """
    ФИНАЛЬНАЯ ВЕРСИЯ: Фильтрует и сортирует список, принимая как одну строку,
    так и список поисковых запросов.
    """
    # Если на входе ничего нет, возвращаем все как есть
    if not search_queries:
        return all_items

    # Превращаем одиночный запрос в список для единообразной обработки
    if isinstance(search_queries, str):
        queries = [search_queries]
    else:
        queries = search_queries

    # Готовим список запросов: убираем пустые, приводим к верхнему регистру
    queries_upper = {q.upper().strip() for q in queries if q.strip()}
    if not queries_upper:
        return all_items

    # --- Фильтрация ---
    # Монета проходит, если она соответствует ХОТЯ БЫ ОДНОМУ из запросов
    filtered_items = [
        item for item in all_items
        if any(query in item.upper() for query in queries_upper)
    ]

    # --- Сортировка (логика остается прежней, но применяется к первому запросу для приоритета) ---
    # Это сделано для того, чтобы если пользователь ищет "BTC ETH", BTC был выше в списке
    primary_query = list(queries_upper)[0]

    sorted_items = sorted(filtered_items, key=lambda item: (
        item.upper() != primary_query,
        not item.upper().startswith(primary_query),
        item
    ))

    return sorted_items


def get_canonical_symbol(symbol: str) -> str:
    """
    Возвращает канонический символ монеты, обрабатывая псевдонимы.

    Args:
        symbol: Исходный символ или псевдоним монеты

    Returns:
        str: Канонический символ (например, 'BTC' для 'BITCOIN')
    """
    upper_symbol = symbol.upper().strip()

    # Сначала проверяем псевдонимы
    if upper_symbol in COINGECKO_SYMBOL_ALIASES:
        return COINGECKO_SYMBOL_ALIASES[upper_symbol]

    # Если это уже канонический символ, возвращаем как есть
    return upper_symbol


def parse_date_safe(date_str: str, provider_name: str = "Unknown") -> Optional[datetime]:
    """
    Безопасный парсинг дат из различных форматов API.

    Поддерживаемые форматы:
    - ISO 8601: "2024-01-15T10:30:00Z" или "2024-01-15T10:30:00+00:00"
    - AlphaVantage: "20240115T103000"
    - UNIX timestamp: числовые значения
    """
    if not date_str:
        return None

    try:
        # Попытка парсинга UNIX timestamp (число)
        if isinstance(date_str, (int, float)) or date_str.isdigit():
            timestamp = float(date_str)
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)

        # Попытка парсинга AlphaVantage формата
        if re.match(r'^\d{8}T\d{6}$', date_str):
            return datetime.strptime(date_str, '%Y%m%dT%H%M%S').replace(tzinfo=timezone.utc)

        # Попытка парсинга ISO 8601 с заменой 'Z' на '+00:00'
        iso_date = date_str.replace('Z', '+00:00')
        return datetime.fromisoformat(iso_date)

    except (ValueError, TypeError, OSError) as e:
        logger.warning(f"Не удалось распарсить дату '{date_str}' от {provider_name}: {e}")
        return None

def clean_html_for_telegram(text: str) -> str:
    """
    Очищает текст ответа AI, оставляя только разрешенные Telegram HTML-теги
    и экранируя специальные символы.
    """
    if not isinstance(text, str):
        return ""

    # 1. Список разрешенных тегов Telegram
    allowed_tags = {'b', 'i', 'u', 's', 'a', 'code', 'pre'}

    # 2. Экранируем основные HTML-символы, чтобы они не воспринимались как теги
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    # 3. "Возвращаем" только разрешенные теги из экранированного вида
    # Этот трюк позволяет сохранить валидные теги, но оставить все остальное безопасным
    for tag in allowed_tags:
        # Для открывающих тегов (включая тег 'a' с атрибутами)
        text = re.sub(rf'&lt;({tag})(\s+[^&]*)?&gt;', r'<\1\2>', text, flags=re.IGNORECASE)
        # для закрывающих тегов
        text = re.sub(rf'&lt;/({tag})&gt;', r'</\1>', text, flags=re.IGNORECASE)

    return text
