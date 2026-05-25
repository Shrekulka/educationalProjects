# src/bot/states/user_states.py

from aiogram.fsm.state import StatesGroup, State


class SettingsState(StatesGroup):
    """
    Состояния для процесса настройки монет пользователя.
    """
    # Пользователь нажал "Добавить монету", бот ждет тикер
    waiting_for_coin_to_add = State()

    # Пользователь нажал "Удалить монету", бот ждет тикер
    waiting_for_coin_to_remove = State()

    # Состояние для добавления монет
    selecting_coins_to_add = State()

    # Cостояние для удаления монет
    selecting_coins_to_remove = State()

    waiting_for_trade_amount = State()

    waiting_for_profit_threshold = State()


class ReportState(StatesGroup):
    """Состояние для отслеживания сообщений в отчетах."""
    viewing = State()


class AdminState(StatesGroup):
    """Состояния для административной панели."""
    choosing_exchange_for_exclude = State()  # Шаг 1: Выбор биржи для исключения
    waiting_for_symbol_to_exclude = State()  # Шаг 2: Ввод символа для исключения

    choosing_exchange_for_include = State()  # Шаг 1: Выбор биржи для включения
    waiting_for_symbol_to_include = State()  # Шаг 2: Ввод символа для включения
    viewing_pair_list = State()


class DensityScreenerState(StatesGroup):
    """Состояния для процесса выбора монет для скринера плотностей."""
    selecting_coins = State()  # Пользователь находится в меню выбора монет


class NewsState(StatesGroup):
    # Состояние для выбора монет вручную через UI с пагинацией и поиском
    selecting_coins_for_news = State()
