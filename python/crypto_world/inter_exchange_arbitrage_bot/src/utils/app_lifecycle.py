# inter_exchange_arbitrage_bot/src/utils/app_lifecycle.py

import asyncio
import time
from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert

import src.core.state as app_state
from src.bot.handlers import settings_handlers, scanner_handlers, admin_handlers, user_handlers, news_handlers
from src.bot.keyboards import get_main_menu_inline_keyboard
from src.bot.logic.greeting_logic import get_dynamic_greeting
from src.bot.middlewares.readiness_middleware import ReadinessMiddleware
from src.constants.api_constants import ARBITRAGE_SCAN_INTERVAL_SECONDS
from src.constants.system_constants import SCANNER_STATUS_STOPPED
from src.constants.system_constants import SYSTEM_STATE_MAIN_MENU_MESSAGE_ID
from src.core.config import config
from src.core.database import async_session_factory
from src.core.scheduler import scheduler
from src.lexicon.lexicon_ru import LEXICON_RU
from src.models.system_models import SystemState
from src.services.ai_trade_advisor_service import AITradeAdvisorService
from src.services.arbitrage_report_service import ArbitrageReportService
from src.services.balance_service import BalanceService
from src.services.density_chart_service import DensityChartService
from src.services.density_screener_service import DensityScreenerService
from src.services.dynamic_pairs_manager import dynamic_pairs_manager
from src.services.enhanced_ai_processor_service import EnhancedAIProcessorService
from src.services.market_data_service import MarketDataService
from src.services.market_intelligence_service import MarketIntelligenceService
from src.services.news_aggregator_service import NewsAggregatorService
from src.services.news_service import NewsService
from src.services.notifier_service import NotifierService
from src.services.proxy_manager import ProxyManager
from src.services.scanner_state_service import get_scanner_state_from_db
from src.services.service_manager import service_manager
from src.strategies.arbitrage_strategy import run_optimized_arbitrage_scan
from src.utils.logger import logger

try:
    from aiohttp_socks import ProxyConnector

    SOCKS_SUPPORTED = True
except ImportError:
    SOCKS_SUPPORTED = False
    logger.warning("Библиотека 'aiohttp-socks' не установлена. Поддержка SOCKS-прокси для бота будет отключена.")


class BotManager:
    """Менеджер для управления жизненным циклом Telegram-бота с поддержкой прокси."""

    def __init__(self):
        self.bot: Optional[Bot] = None
        self.dp: Optional[Dispatcher] = None
        self.polling_task: Optional[asyncio.Task] = None
        self._shutdown_complete = False

    async def _create_bot_session(self) -> AiohttpSession:
        """Создает сессию для бота, используя лучший доступный прокси."""
        if (
                config.network.tor_proxy_enabled and SOCKS_SUPPORTED and app_state.proxy_manager and app_state.proxy_manager.is_tor_available):
            logger.info(f"Настройка сессии бота для работы через TOR: {config.network.tor_proxy_url}")
            return AiohttpSession(proxy=config.network.tor_proxy_url)

        if app_state.proxy_manager and (healthy_proxies := app_state.proxy_manager.get_healthy_proxies()):
            proxy_url = f"http://{healthy_proxies[0]}"
            logger.info(f"Настройка сессии бота для работы через HTTP прокси: {proxy_url}")
            return AiohttpSession(proxy=proxy_url)

        logger.warning("Не найдено рабочих прокси. Telegram Bot будет работать через прямое соединение.")
        return AiohttpSession()

    async def initialize(self) -> bool:
        """Создает, настраивает и тестирует экземпляр бота. Возвращает True в случае успеха."""
        if self.bot:
            return True

        bot_session = await self._create_bot_session()

        app_state.bot_instance = Bot(
            token=config.tg_bot.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
            session=bot_session
        )
        self.bot = app_state.bot_instance

        try:
            # ПРОВЕРКА СОЕДИНЕНИЯ: Пытаемся получить информацию о боте
            await self.bot.get_me()
            logger.info(f"Успешное соединение с Telegram API через {bot_session.proxy or 'прямое соединение'}.")
        except Exception as e:
            logger.critical(f"КРИТИЧЕСКАЯ ОШИБКА: Не удалось подключиться к Telegram API. Ошибка: {e}")
            await bot_session.close()
            app_state.bot_instance = None
            self.bot = None
            return False

        self.dp = Dispatcher()
        self.dp.update.middleware(ReadinessMiddleware())

        self.dp.include_router(user_handlers.router)
        self.dp.include_router(settings_handlers.router)
        self.dp.include_router(scanner_handlers.router)
        self.dp.include_router(admin_handlers.router)
        self.dp.include_router(news_handlers.router)
        logger.info("Экземпляр бота, диспетчер и middleware успешно настроены.")
        return True

    def start_polling(self):
        """Запускает прослушивание сообщений в фоновом режиме."""
        if not self.bot or not self.dp:
            logger.error("Ошибка запуска polling: бот не был инициализирован.")
            return

        # Этот вызов остается асинхронным и уходит в фон
        app_state.bot_task = asyncio.create_task(self._run_polling())
        logger.info("Long polling для бота запущен в фоновом режиме.")

    async def _run_polling(self):
        try:
            await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot, handle_signals=False)
        except asyncio.CancelledError:
            logger.info("Задача polling была отменена.")
        except Exception as e:
            logger.critical(f"Критическая ошибка в цикле polling: {e}", exc_info=True)

    async def shutdown(self, timeout: float = 5.0):
        """
        Улучшенная версия: корректная проверка сессии и более надежная обработка исключений.
        """
        if self._shutdown_complete:
            logger.debug("BotManager уже остановлен, пропускаем...")
            return

        logger.info("Начинаю остановку Telegram бота...")

        try:
            # Сначала останавливаем polling через официальный метод aiogram
            if self.dp:
                try:
                    await asyncio.wait_for(self.dp.stop_polling(), timeout=timeout / 2)
                    logger.info("Dispatcher остановлен.")
                except asyncio.TimeoutError:
                    logger.warning(f"Таймаут остановки dispatcher за {timeout / 2}с.")
                except Exception as e:
                    logger.error(f"Ошибка остановки dispatcher: {e}")

            # Затем отменяем задачу polling, если она еще активна
            if self.polling_task and not self.polling_task.done():
                self.polling_task.cancel()
                try:
                    await asyncio.wait_for(self.polling_task, timeout=timeout / 2)
                    logger.info("Задача polling корректно завершена.")
                except asyncio.TimeoutError:
                    logger.warning(f"Задача polling не завершилась за {timeout / 2}с.")
                except asyncio.CancelledError:
                    logger.info("Задача polling была отменена.")

        except Exception as e:
            logger.error(f"Ошибка при завершении polling: {e}")
        finally:
            # Улучшенная проверка и закрытие HTTP-сессии бота
            if self.bot and hasattr(self.bot, 'session') and self.bot.session:
                try:
                    # Проверяем, что сессия еще не закрыта, с fallback значением True
                    if not getattr(self.bot.session, 'closed', True):
                        await asyncio.wait_for(self.bot.session.close(), timeout=2.0)
                        logger.info("Сессия aiogram Bot закрыта.")
                    else:
                        logger.debug("Сессия aiogram Bot уже была закрыта.")
                except asyncio.TimeoutError:
                    logger.warning("Таймаут при закрытии сессии бота")
                except Exception as e:
                    logger.error(f"Ошибка при закрытии сессии бота: {e}")

            self._shutdown_complete = True
            logger.info("BotManager полностью остановлен.")


bot_manager = BotManager()


async def initialize_app_services():
    """
    ФИНАЛЬНАЯ ВЕРСИЯ: Инициализирует все сервисы в правильной последовательности,
    гарантируя готовность зависимостей (прокси, экземпляр бота) перед их использованием.
    """
    logger.info("Фоновая инициализация сервисов запущена...")
    start_time = time.time()
    initialization_successful = False

    try:
        # --- ЭТАП 1: Инициализация ProxyManager и ОЖИДАНИЕ первого сканирования ---
        if config.network.proxy_sources or config.network.tor_proxy_enabled:
            logger.info("Инициализация ProxyManager...")
            app_state.proxy_manager = ProxyManager(config.network, app_state.httpx_session)
            await app_state.proxy_manager.run()
            await app_state.proxy_manager.wait_for_initial_scan(timeout=180.0)
        else:
            logger.info("Источники прокси и TOR не настроены, ProxyManager не будет запущен.")

        # --- ЭТАП 2: Синхронная инициализация и проверка экземпляра бота ---
        if not await bot_manager.initialize():
            raise ConnectionError("Не удалось инициализировать Telegram бота. Проверьте токен и сетевые настройки.")

        # --- ЭТАП 3: Асинхронный запуск прослушивания сообщений ---
        bot_manager.start_polling()

        # --- ЭТАП 4: Инициализация сервисов, зависимых от бота ---
        logger.info("Инициализация NotifierService и ArbitrageReportService...")
        app_state.notifier_service = NotifierService()
        app_state.report_service = ArbitrageReportService()

        # --- ЭТАП 5: Инициализация остальных сервисов приложения ---
        logger.info("Инициализация основных сервисов (AI, News, Market Intel)...")
        ai_processor = EnhancedAIProcessorService(config.ai_providers, app_state.httpx_session)
        news_fetcher = NewsService(config.news_providers, app_state.httpx_session)
        app_state.market_intel_service = MarketIntelligenceService(config.news_providers, app_state.httpx_session)
        market_data_fetcher = MarketDataService(
            http_session=app_state.httpx_session,
            market_intel_service=app_state.market_intel_service
        )
        app_state.ai_trade_advisor = AITradeAdvisorService(ai_processor)
        app_state.news_aggregator_service = NewsAggregatorService(
            news_service=news_fetcher,
            ai_service=ai_processor,
            market_data_service=market_data_fetcher,
            market_intel_service=app_state.market_intel_service
        )
        logger.info("Новостные и AI сервисы успешно инициализированы.")

        logger.info("Запуск инициализации ServiceManager...")
        await service_manager.initialize()
        logger.info("ServiceManager инициализирован успешно")

        logger.info("Инициализация DynamicPairsManager с зависимостями...")
        dynamic_pairs_manager.initialize(notifier=app_state.notifier_service, config_obj=config)

        logger.info("Запуск фонового обновления сервисов...")
        await service_manager.start_background_refresh()
        logger.info("Фоновое обновление запущено")

        if config.tg_bot.admin_ids:
            logger.info("Инициализация BalanceService...")
            app_state.balance_service = BalanceService(user_id=config.tg_bot.admin_ids[0])
            await asyncio.wait_for(app_state.balance_service.initialize(), timeout=30.0)
            logger.info("BalanceService инициализирован")

        logger.info("Инициализация DensityScreenerService...")
        app_state.density_screener_service = DensityScreenerService(service_manager.services)
        logger.info("DensityScreenerService инициализирован")

        logger.info("Инициализация DensityChartService...")
        app_state.density_chart_service = DensityChartService()
        logger.info("DensityChartService инициализирован")

        # --- ЭТАП 6: Настройка и запуск фоновых задач ---
        logger.info("Настройка планировщика задач...")
        scheduler.add_job(
            run_optimized_arbitrage_scan, "interval",
            seconds=ARBITRAGE_SCAN_INTERVAL_SECONDS, id="arbitrage_job", max_instances=1
        )
        logger.info("Задача арбитража добавлена в планировщик")

        initialization_successful = True
        app_state.is_ready_event.set()

        elapsed_time = time.time() - start_time
        logger.info(f"Все сервисы успешно инициализированы за {elapsed_time:.2f} секунд")

        scanner_initial_state = await get_scanner_state_from_db()
        scheduler.start()
        if scanner_initial_state == SCANNER_STATUS_STOPPED:
            scheduler.pause_job('arbitrage_job')
            logger.info("Сканер восстановлен в состоянии 'Остановлен'")
        else:
            logger.info("Сканер восстановлен в состоянии 'Запущен'")

        # --- ЭТАП 7: Финальное уведомление администраторов с исправленной логикой ---
        if config.tg_bot.admin_ids:
            async with async_session_factory() as session:
                for admin_id in config.tg_bot.admin_ids:
                    logger.debug(f"Обработка уведомления для админа {admin_id}")
                    greeting = get_dynamic_greeting(admin_id)
                    welcome_text = LEXICON_RU['system_ready_notification'].format(dynamic_greeting=greeting)
                    message_id_key = SYSTEM_STATE_MAIN_MENU_MESSAGE_ID.format(admin_id=admin_id)

                    stmt = select(SystemState.value).where(SystemState.key == message_id_key)
                    message_id_str = (await session.execute(stmt)).scalar_one_or_none()

                    should_send_new = True  # По умолчанию считаем, что нужно отправить новое сообщение
                    if message_id_str:
                        try:
                            await bot_manager.bot.edit_message_text(
                                text=welcome_text,
                                chat_id=admin_id,
                                message_id=int(message_id_str),
                                reply_markup=get_main_menu_inline_keyboard()
                            )
                            logger.info(f"Админ {admin_id}: сообщение {message_id_str} успешно обновлено.")
                            should_send_new = False  # Редактирование удалось, новое не нужно

                        except TelegramBadRequest as e:
                            if "message to edit not found" in str(e).lower():
                                logger.warning(
                                    f"Админ {admin_id}: сообщение {message_id_str} не найдено. Удаляю из БД.")
                                await session.execute(delete(SystemState).where(SystemState.key == message_id_key))
                            elif "message is not modified" in str(e).lower():
                                logger.info(f"Админ {admin_id}: сообщение {message_id_str} уже актуально.")
                                should_send_new = False  # Сообщение не изменилось, новое не нужно
                            else:
                                logger.error(f"Админ {admin_id}: непредвиденная ошибка API при редактировании: {e}")
                        except Exception as e:
                            logger.error(f"Админ {admin_id}: критическая ошибка при редактировании: {e}", exc_info=True)

                    if should_send_new:
                        logger.info(f"Админ {admin_id}: отправка нового главного меню.")
                        try:
                            sent_message = await bot_manager.bot.send_message(
                                chat_id=admin_id,
                                text=welcome_text,
                                reply_markup=get_main_menu_inline_keyboard()
                            )
                            stmt_update = insert(SystemState).values(key=message_id_key,
                                                                     value=str(sent_message.message_id))
                            stmt_update = stmt_update.on_conflict_do_update(
                                index_elements=['key'], set_={'value': stmt_update.excluded.value}
                            )
                            await session.execute(stmt_update)
                            logger.info(f"Админ {admin_id}: сохранено новое сообщение с ID: {sent_message.message_id}")
                        except Exception as e:
                            logger.error(f"Админ {admin_id}: не удалось отправить новое главное меню: {e}")

                await session.commit()  # Единый коммит в конце цикла по админам

    except (asyncio.TimeoutError, ConnectionError) as e:
        elapsed_time = time.time() - start_time
        logger.critical(f"Инициализация остановлена (прошло {elapsed_time:.2f}с): {e}")
    except Exception as e:
        elapsed_time = time.time() - start_time
        logger.critical(f"Критическая ошибка при инициализации (прошло {elapsed_time:.2f}с): {e}", exc_info=True)
    finally:
        if not initialization_successful:
            logger.critical("Инициализация провалена - арбитражные задачи не будут запускаться")


async def _wait_for_task_with_timeout(task: asyncio.Task, task_name: str, timeout: float):
    """Безопасно ожидает завершения задачи с таймаутом."""
    try:
        await asyncio.wait_for(task, timeout=timeout)
        logger.info(f"Задача {task_name} корректно завершена.")
    except asyncio.TimeoutError:
        logger.warning(f"Задача {task_name} не завершилась за {timeout}с.")
    except asyncio.CancelledError:
        logger.info(f"Задача {task_name} была отменена.")
    except Exception as e:
        logger.error(f"Ошибка при завершении {task_name}: {e}")


async def _shutdown_service_manager():
    """Безопасная остановка ServiceManager."""
    try:
        await asyncio.wait_for(service_manager.shutdown(), timeout=10.0)
    except asyncio.TimeoutError:
        logger.warning("Таймаут при остановке менеджера сервисов")
    except Exception as e:
        logger.error(f"Ошибка остановки менеджера сервисов: {e}")


async def _close_global_sessions():
    """Централизованно закрывает все глобальные HTTP-сессии."""
    sessions_to_close = [
        ('aiohttp_session', getattr(app_state, 'aiohttp_session', None)),
        ('httpx_session', getattr(app_state, 'httpx_session', None)),
        ('internal_httpx_session', getattr(app_state, 'internal_httpx_session', None)),
    ]

    for session_name, session in sessions_to_close:
        if not session:
            logger.debug(f"Сессия {session_name} не была инициализирована.")
            continue

        try:
            if session_name == 'aiohttp_session':
                if hasattr(session, 'closed') and not session.closed:
                    await asyncio.wait_for(session.close(), timeout=3.0)
                    logger.info(f"✅ Сессия {session_name} закрыта.")
            else:  # httpx sessions
                if hasattr(session, 'is_closed') and not session.is_closed:
                    await asyncio.wait_for(session.aclose(), timeout=3.0)
                    logger.info(f"✅ Сессия {session_name} закрыта.")
        except asyncio.TimeoutError:
            logger.warning(f"⚠️ Таймаут при закрытии {session_name}")
        except Exception as e:
            logger.error(f"❌ Ошибка при закрытии {session_name}: {e}")


async def shutdown_application():
    """Корректно останавливает все компоненты приложения параллельно."""
    logger.info("Начинаю graceful shutdown...")
    shutdown_tasks = []

    # Улучшенная остановка планировщика
    try:
        # APScheduler state: 0=STOPPED, 1=RUNNING, 2=PAUSED
        if hasattr(scheduler, 'state') and scheduler.state != 0:
            scheduler.shutdown(wait=False)
            logger.info("Планировщик остановлен.")
        else:
            logger.debug("Планировщик уже остановлен или не был запущен.")
    except Exception as e:
        logger.error(f"Ошибка остановки планировщика: {e}")

    # Централизованная отмена фоновых задач
    tasks_to_cancel = [
        ('recon_task', getattr(app_state, 'recon_task', None), 2.0),
        ('services_init_task', getattr(app_state, 'services_init_task', None), 3.0),
    ]

    for task_name, task, timeout in tasks_to_cancel:
        if task and not task.done():
            task.cancel()
            shutdown_tasks.append(
                asyncio.create_task(_wait_for_task_with_timeout(task, task_name, timeout))
            )

    # Добавляем остановку основных компонентов
    shutdown_tasks.extend([
        asyncio.create_task(bot_manager.shutdown()),
        asyncio.create_task(_shutdown_service_manager())
    ])

    if shutdown_tasks:
        await asyncio.gather(*shutdown_tasks, return_exceptions=True)

    # Закрываем глобальные HTTP-сессии в самом конце
    await _close_global_sessions()

    logger.info("Graceful shutdown завершен.")


async def periodic_api_usage_check():
    """Периодическая проверка оставшихся лимитов CoinGecko API."""
    if app_state.market_intel_service:
        usage_data = await app_state.market_intel_service.check_api_usage()
        if usage_data:
            remaining = usage_data.get('current_remaining_monthly_calls')
            if remaining is not None and remaining < 1000:  # Порог предупреждения
                warning_text = f"⚠️ ВНИМАНИЕ: Осталось менее {remaining} запросов к CoinGecko API в этом месяце!"
                logger.critical(warning_text)
                if app_state.notifier_service:
                    for admin_id in config.tg_bot.admin_ids:
                        await app_state.notifier_service.send_message(admin_id, warning_text)
