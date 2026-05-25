# inter_exchange_arbitrage_bot/src/constants/system_constants.py

"""
Константы, описывающие ключи и значения для хранения глобальных состояний системы в базе данных.
"""

# === Ключи состояний (таблица system_states) ===
# Ключ для хранения текущего состояния сканера (запущен/остановлен).
SYSTEM_STATE_SCANNER_STATUS = "scanner_status"

# ШАБЛОН КЛЮЧА: Для хранения ID последнего heartbeat-сообщения для каждого админа.
# Будет использоваться как 'heartbeat_message_id_123456789'
SYSTEM_STATE_HEARTBEAT_MESSAGE_ID = "heartbeat_message_id_{admin_id}"


# === Возможные значения состояний ===
# Значение, означающее, что сканер активен.
SCANNER_STATUS_RUNNING = "running"
# Значение, означающее, что сканер остановлен.
SCANNER_STATUS_STOPPED = "stopped"

# ШАБЛОН КЛЮЧА: Для хранения ID главного меню для каждого админа.
# Будет использоваться как 'main_menu_message_id_123456789'
SYSTEM_STATE_MAIN_MENU_MESSAGE_ID = "main_menu_message_id_{admin_id}"