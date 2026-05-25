# inter_exchange_arbitrage_bot/src/lexicon/lexicon_ru.py
from src.constants.trading_constants import DENSITY_SCREENER_CONFIG

LEXICON_RU = {
    # =================================================================
    # =============== 👑 Admin Panel & Keyboards 👑 ===================
    # =================================================================

    # --- Тексты кнопок (с суффиксом _button) ---
    'admin_panel_button': '👑 Админ-панель',
    'pair_status_button': '📊 Статус пар (кэш)',
    'exclude_pair_button': '🚫 Исключить пару',
    'include_pair_button': '✅ Вернуть в сканер',
    'back_to_main_menu_button': '🏠 Главное меню',
    'back_to_admin_panel_button': '⬅️ Назад в админ-панель',
    'back_to_settings_button': '⬅️ Назад в Настройки',
    'back_to_statistics_button': '⬅️ Назад к статистике',
    'refresh_button': '🔄 Обновить',
    'all_assets_button': '📊 Все активы',
    'tracked_assets_button': '⭐ Избранные',
    'settings_button': '⚙️ Настройки',
    'my_coins_button': '✨ Мои монеты',
    'add_coin_button': '➕ Добавить монеты',
    'remove_coin_button': '🗑️ Удалить монету',
    'scanner_settings_button': '📈 Настройки сканера',
    'pagination_back_button': '⬅️ Назад',
    'pagination_forward_button': 'Вперед ➡️',
    'confirm_button': '✅ Сохранить',
    'select_button': '✅ Выбрать',
    'cancel_button': '🚫 Отмена',
    'clear_search_button': '🔄 Сбросить поиск',
    'remove_selected_button': '🗑️ Удалить выбранные',
    'cancel_button_pressed': 'Действие отменено.',
    'scanner_status_button': '📈 Сканер',
    'report_menu_button': '📊 Отчет по сделкам',
    'start_scanner_button': '▶️ Запустить сканер',
    'stop_scanner_button': '⏹️ Остановить сканер',
    'check_status_button_short': '🟢 Статус: Запущен',
    'check_status_button_long': '🔴 Статус: Остановлен',
    'stop_scanner_button_short': '⏹️ Остановить',
    'start_scanner_button_short': '▶️ Запустить',
    'change_trade_amount_button': '✍️ Изменить сумму сделки',
    'change_profit_threshold_button': '✍️ Изменить порог прибыльности',
    'reset_trade_amount_button': '🔄 Сбросить сумму к значению по умолчанию (${default_amount:.2f})',
    'reset_profit_threshold_button': '🔄 Сбросить порог к значению по умолчанию ({default_threshold:.2f}%)',
    'no_excluded_pairs_button': "📝 Нет исключенных пар",
    'exchange_header_button': "🏢 {exchange}",
    'include_pair_symbol_button': "✅ {symbol}",
    'back_to_admin_panel': '⬅️ Назад в админ-панель',

    # =================================================================
    # =============== ⚙️ API & SYSTEM (backend) ⚙️ ===================
    # =================================================================

    # --- Общие сообщения и ошибки API ---
    'api_is_running': "🤖 <b><u>Машина для печати денег онлайн!</u></b> 💰 API работает как швейцарские часы. <i>⚡ Сканирую пульс рынка... все системы готовы к памп!</i>",
    'api_error_key_not_configured': "💥 <b>Критический сбой!</b> Ключ API не настроен. <i>Кто-то забыл покормить роботов...</i>",
    'api_error_invalid_credentials': "🚫 <b>Доступ запрещен!</b> Неверные учетные данные. <i>Вы точно из нашей банды трейдеров?</i>",
    'api_error_balance_service_not_ready': "⏳ <b>Сервис балансов грузится...</b> Роботы еще не проснулись. <i>Дайте им пару секунд на кофе!</i> ☕",
    'api_error_invalid_balance_mode': "❌ <b>Неверный режим!</b> Используйте 'tracked' (избранные) или 'all' (весь портфель). <i>Определитесь уже!</i>",
    'api_error_report_generation': "📊 <b>Глюк генератора отчетов!</b> <i>Роботы-аналитики ушли на перерыв.</i>",
    'api_error_asset_collection': "💼 <b>Сбой сбора активов!</b> <i>Кто-то рассыпал все монетки...</i>",
    'api_error_generic': "💥 <b>Внутренняя ошибка сервера:</b> <code>{error}</code> <i>Вызываем техподдержку!</i>",
    'api_msg_pair_excluded': "🚫 Пара <code>{symbol}</code> на <b>{exchange}</b> отправлена в <i>черный список</i>.",
    'api_msg_pair_included': "✅ Пара <code>{symbol}</code> на <b>{exchange}</b> <i>реабилитирована</i> и возвращена в игру!",
    'cache_is_empty': (
        'ℹ️ <b>Кэш девственно чист</b> 🤖\n\n'
        '<i>Это нормально при первом запуске или после перезагрузки. '
        'Данные по активным парам появятся здесь автоматически после первого цикла сканирования. '
        'Роботы уже работают! 🔄</i>'
    ),

    # --- Логи API ---
    'log_internal_api_key_not_set': "🚨 КРИТИЧЕСКАЯ ОШИБКА: INTERNAL_API_KEY не настроен в конфигурации (.env). Кто-то забыл ключи дома!",
    'log_invalid_api_key_attempt': "🔐 Попытка взлома админ-панели с неверным API ключом: {api_key_preview}... Хакеры что ли?",
    'log_admin_request_authorized': "👑 Успешная авторизация VIP-трейдера. Добро пожаловать в элиту!",
    'log_assets_fetch_failed': "📉 Не удалось получить активы с {exchange_id} для эндпоинта /assets. Биржа лагает!",
    'log_assets_endpoint_error': "💥 Ошибка на эндпоинте /assets: {e}",
    'log_balance_report_error': "📊 Ошибка при генерации отчета о балансах: {e}",

    # --- Сканер (API-часть) ---
    'scanner_started': "🚀 <b><u>ПОЕХАЛИ ДЕЛАТЬ ИКСЫ!</u></b> 💎 Сканер активирован и уже <i>нюхает неэффективности рынка</i> как охотничья собака! <b>Пора зарабатывать!</b> 💰📈",
    'scanner_stopped': "🛑 <b><u>Фиксируем профит и чиллим!</u></b> 😎 Сканер припаркован. <i>Надеюсь, все успели словить памп на низах?</i> 🌙✨",
    'job_not_found': "🤷‍♂️ <i>Кажется, кто-то словил <b>ликвидацию...</b></i> 💀 Задачу сканера не найти. <code>Error 444: Job Not Found</code>. <b>Срочно зовем разрабов!</b> 🛠️",
    'api_error_scheduler_start': "⚙️ <b>Планировщик глючит!</b> Не удалось запустить задачу. <i>Роботы бастуют?</i>",
    'status_running': "📈 <b><u>ПОЛНЫЙ ГАЗ!</u></b> 🟢 Сканер <i>скальпирует спреды</i> и охотится за арбитражными окнами как зверь! <b>To the moon!</b> 🚀🌕",
    'status_stopped': "☕️ <b>Релакс-режим включен.</b> 🛋️ Рынок флэтит, сканер ушел <i>пить матчу и читать charts</i>. <b>Ждём волну!</b> 🌊",
    'current_status': "📊 <b>Состояние нашего <u>кибер-трейдера</u>:</b> {status}",

    # --- Логи сканера и планировщика (API-часть) ---
    'log_started_api': "👨‍💻 [API] 📈 Сигнал 'ЛОНГ' получен! Активирую протоколы сканирования. <i>Let the games begin!</i> 🎮",
    'log_stopped_api': "👨‍💻 [API] 📉 Сигнал 'ШОРТ' получен! Перевожу сканер в режим HODL. <i>Все системы под контролем, сэр!</i> 🎖️",
    'log_scheduler_resumed': "⏰ Планировщик: задача сканирования возобновлена. Роботы вернулись к работе!",
    'log_scheduler_already_active': "⏰ Планировщик: задача сканирования уже была активна. Роботы не спали!",
    'log_scheduler_resume_error': "🚨 Критическая ошибка при возобновлении задачи планировщика: {error}",
    'log_scheduler_paused': "⏸️ Планировщик: задача сканирования поставлена на паузу. Роботы ушли на перерыв.",
    'log_scheduler_already_paused': "⏸️ Планировщик: задача сканирования уже была на паузе. Роботы уже отдыхали!",
    'log_scheduler_pause_error': "❌ Ошибка при постановке задачи на паузу: {error}",

    # --- Health Check ---
    'health_status_ok': "✅ <b><u>Все зелёное!</u></b> 🟢📈 Система <i>памп-готова</i>! <b>Быки правят бал!</b> 🐂💪",
    'health_status_degraded': "⚠️ <b><u>Мини-коррекция!</u></b> 📉 Один сервис <i>словил стоп-лосс</i>, но мы <b>держим позицию!</b> 💎🙌",
    'service_healthy': "👍 <b>Сигнал на ПОКУПКУ!</b> 📈💚",
    'service_unhealthy': "👎 <b>Медведи атакуют!</b> 📉🔴",
    'ready_for_arbitrage_true': "💎🙌 <b><u>ДА!</u></b> Готов ловить ракеты и делать иксы! 🚀💰",
    'ready_for_arbitrage_false': "📉 <b>Пока нет...</b> Рынок слишком тонкий. <i>Ждем жирненькую волатильность!</i> ⚡",
    'health_check_title': "🩺 <b><u>Технический анализ всех систем:</u></b> 📊🔍\n\n",
    'health_check_summary': "<b>📈 Общий тренд:</b> {status}\n",
    'health_check_services_count': "<b>💼 Активы в портфеле:</b> {healthy_count} из {total_count} <i>показывают рост</i>.\n",
    'health_check_details_title': "<b>🔍 Разбор по каждому активу:</b>\n",
    'health_check_service_line': "— <i>{service_name}:</i> {service_status}\n",
    'health_check_readiness': "\n<b>🎯 Готовность к арбитражу:</b> {is_ready}",

    # =================================================================
    # =============== 🤖 TELEGRAM BOT 🤖 ==============================
    # =================================================================

    # --- Общие сообщения и ошибки ---
    'main_menu_greeting': (
        "<b><u>💎 Ваш Персональный Арбитражный Ассистент 💎</u></b>\n\n"
        "🚀 Я готов к поиску и исполнению <i><b>прибыльных сделок</b></i>! "
        "Давайте делать иксы вместе! 📈💰\n\n"
        "<i><b>🎯 Краткий мануал по разделам:</b></i>\n\n"
        "💰 <b>Баланс:</b>\n"
        "   └─ <i>Проверяйте свой портфель на всех биржах (весь депо или только избранные алмазы).</i> 💎\n\n"
        "📈 <b>Сканер:</b>\n"
        "   └─ <i>Запускайте и останавливайте основной движок поиска арбитражных окон для памп!</i> 🚀\n\n"
        "🛡️ <b>Скринер плотностей:</b>\n"
        "   └─ <i>Используйте рентген рынка, чтобы видеть \"стенки\" китов 🐋 и находить сильные уровни для входа/выхода.</i>\n\n"
        "📊 <b>Отчеты:</b>\n"
        "   └─ <i>Анализируйте свой P&L и историю сделок (краткая сводка или детальная статистика по каждому трейду).</i> 📈💵\n\n"
        "⚙️ <b>Настройки:</b>\n"
        "   └─ <i>Управляйте списком отслеживаемых монет и настройте жадность-индекс (сумма позиции, порог профита).</i> 🎛️\n\n"
        "👑 <b>VIP Админ-панель:</b>\n"
        "   └─ <i>Получайте детальную аналитику по парам и ручное управление исключениями для профи!</i> 🎯"
    ),
    'system_ready_notification': (
        "🚀 <b><u>Система Полностью Активирована!</u></b> 🚀\n\n"
        "{dynamic_greeting}!\n\n"
        "Ваш персональный арбитражный ассистент онлайн и готов к поиску прибыльных связок. 💎\n\n"
        "<i>Все сервисы запущены, биржи подключены, сканер ожидает ваших команд.</i>\n\n"
        "<b>Вперед, к новым высотам!</b> 📈💰"
    ),
    'system_initializing_alert': '⏳ Пожалуйста, подождите, сервисы подготавливаются для продуктивной работы...',
    'back_to_main_menu': '🏠 Главное меню',
    'bot_error_telegram': "❌ <b>Телеграм лагает!</b> <i>Попробуйте позже, когда Дуров починит сервера.</i> 🤖",
    'bot_error_menu_load_critical': "💥 <b><u>КРИТИЧЕСКИЙ КРАШ!</u></b> 🚨 Не могу загрузить панель управления. <i>Что-то серьезно сломалось в матрице!</i>",
    'bot_error_critical': "💥 <b><u>МЕГА-СБОЙ!</u></b> ⚡ При выполнении команды что-то взорвалось как ракета Илона Маска! <i>Срочно смотрим логи!</i> 🚀💥",
    'invalid_format_error': (
        "❌ <b>Некорректный формат символа торговой пары!</b>\n\n"
        "✅ <b>Правильные примеры:</b>\n"
        "• <code>BTC/USDT</code>\n"
        "• <code>ETH/BTC</code>\n\n"
        "❌ <b>Неправильные примеры:</b>\n"
        "• <code>btc-usdt</code> (нужен слэш /)\n"
        "• <code>BTC</code> (нужна вторая валюта)\n\n"
        "Попробуйте еще раз:"
    ),
    'bot_menu_not_modified': "ℹ️ <b>Рынок без изменений.</b> Меню актуально как курс биткоина! 📊",
    'bot_partial_fill_alert': (
        "🚨 <b><u>АЛЕРТ! ЧАСТИЧНОЕ ИСПОЛНЕНИЕ!</u></b> ⚠️💀\n\n"
        "💥 <b>Дисбаланс позиций</b> по паре <b><u>{symbol}</u></b>! "
        "Кто-то <i>съел ликвидность быстрее нас!</i> 😱\n"
        "🛠️ <b>Требуется срочная ручная проверка</b> и корректировка на биржах!\n\n"
        "<b><u>📋 Детали трейда:</u></b>\n"
        "🟢 <b>Покупка ({buy_exchange}):</b>\n"
        "   - Исполнено: <code>{buy_filled:.8f} {coin}</code>\n"
        "   - Потрачено: <code>${buy_cost:,.2f}</code> 💸\n"
        "🔴 <b>Продажа ({sell_exchange}):</b>\n"
        "   - Исполнено: <code>{sell_filled:.8f} {coin}</code>\n"
        "   - Получено: <code>${sell_revenue:,.2f}</code> 💰\n\n"
        "⚖️ <b><u>Дисбаланс позиции:</u></b> <code>{imbalance:.8f} {coin}</code> 📊"
    ),

    # --- Сканер (Bot-часть) ---
    'bot_scanner_menu_text': (
        "<b><u>🚀 Центр управления полетами к Луне 🌙</u></b>\n\n"
        "<b>📊 Текущий статус:</b> {status}\n\n"
        "<i>💡 Отсюда вы отдаете приказы своей армии роботов: "
        "отправить ботов <b>в бой за иксы</b> 💎 или вернуть на базу "
        "для отдыха и анализа рынка! 📈</i>"
    ),
    'heartbeat_message_text': (
        "❤️‍🔥 Сканер в работе.\n\n"
        "Продолжаю активный поиск арбитражных возможностей. "
        "Как только появится подходящая сделка, вы сразу получите уведомление."
    ),
    'bot_status_active_full': "🟢 <b><u>В РЫНКЕ!</u></b> 📈 Ищет профитные связки <i>как настоящий дегенерат!</i> 💎🙌",
    'bot_status_stopped_full': "🔴 <b>На заборе сидит.</b> ☕ Чиллит и ждет <i>вашего сигнала к действию!</i> ⏳",
    'bot_scanner_already_running': "🚀 <b>Куда торопимся?</b> Бот уже <i>летит to the moon</i> на полной скорости! 🌙✨",
    'bot_scanner_already_stopped': "☕️ <b>Бот и так релаксит!</b> 😎 Дайте парню <i>допить кофе и проанализировать charts</i>! 📊",
    'bot_scanner_start_success': "✅ Лонг открыт!\nБот отправлен делать иксы на спредах! 🚀💰",
    'bot_scanner_stop_success': "🛑 <b><u>Фиксируем профит!</u></b> 💰 Бот успешно припаркован. <i>Время подсчитать наварку!</i> 🧮✨",
    'bot_scanner_status_not_changed_warning': "⚠️ <b>Что-то странное...</b> 🤔 Команда ушла, но бот не отчитался об изменении статуса. <i>Возможно, API тупит. Проверьте логи!</i> 📋",
    'bot_scanner_start_fail_api': "❌ <b><u>СВЯЗЬ ПОТЕРЯНА!</u></b> 📡 Не удалось запустить сканер. <i>Проверьте, не сдох ли API сервер!</i> 🤖💀",
    'bot_scanner_stop_fail_api': "❌ <b><u>РОБОТ НЕ ОТВЕЧАЕТ!</u></b> 📻 Не удалось остановить сканер. <i>API завис или что-то еще хуже!</i> ⚙️💥",
    'bot_scanner_status_fetch_fail': "❌ <b>Нет связи с базой!</b> 📡 Не могу достучаться до API для проверки статуса. <i>Похоже на обрыв связи или DDoS!</i> 🌐💥",
    'bot_scanner_check_status_template': "<b>Текущее положение дел:</b> {status}",
    'bot_scanner_check_status_running': "🟢 <b>В рынке!</b>",
    'bot_scanner_check_status_stopped': "🔴 <b>На заборе.</b>",

    # --- Админ-панель (Bot-часть) ---
    'admin_panel_header': (
        '👑 <b><u>VIP Кабинет Трейдера</u></b> 💎\n\n'
        'Здесь вы управляете <i><b>своей торговой империей</b></i> 🏰 и решаете, '
        'какие пары достойны <b>вашего драгоценного внимания</b>! 🎯💰\n\n'
        '<i>💡 <b>Фича для профи:</b> временно блокируйте 🚫 "мусорные" активы '
        '(низкая ликвидность, зависшие ордера) и возвращайте их в игру ✅ '
        'когда рынок созреет для памп!</i> 🚀'
    ),
    'prompt_exclude_pair': (
        '1️⃣ <b><u>Шаг 1: Выбор биржи для исключения</u></b> 🎯\n\n'
        '<i>💡 Бот перестанет сканировать выбранную пару только на этой бирже. '
        'На остальных она продолжит мониториться для поиска арбитража!</i> 📊'
    ),
    'prompt_enter_symbol_exclude': (
        '2️⃣ <b><u>Шаг 2: Ввод тикера для блэклиста</u></b> ✍️\n\n'
        '📝 Теперь просто отправьте в чат тикер пары, которую нужно <b>исключить из игры</b>.\n\n'
        '<i>💡 Правильные примеры:</i> <code>BTC/USDT</code>, <code>ETH/USDT</code>, <code>SOL/USDT</code> 🪙'
    ),
    'prompt_include_pair': (
        '1️⃣ <b>Шаг 1: Выбор биржи для включения</b>\n\n'
        '<i>Выберите биржу, на которой вы хотите снова начать '
        'сканировать ранее исключенную пару.</i>'
    ),
    'prompt_enter_symbol_include': (
        '2️⃣ <b>Шаг 2: Ввод тикера для включения</b>\n\n'
        '✍️ Отправьте в чат тикер пары, которую нужно вернуть в сканирование.\n\n'
        '<i>Например:</i> `ETH/USDT`'
    ),
    'include_success': (
        '✅ <b>Пара возвращена!</b>\n\n'
        'Пара `{symbol}` на бирже <b>{exchange}</b> будет снова проверена в следующем цикле сканирования.'
    ),
    'exclude_success': (
        '✅ <b><u>Пара отправлена в изгнание!</u></b> 🚫\n\n'
        'Пара <code><b>{symbol}</b></code> на бирже <b><u>{exchange}</u></b> '
        'больше не будет участвовать в поиске арбитража. <i>До свидания, неудачница!</i> 👋'
    ),
    'include_success_formatted': "✅ <b><u>Реабилитация прошла успешно!</u></b> 🎉\nПара <code><b>{symbol}</b></code> на <b><u>{exchange}</u></b> <i>возвращена в бой</i> и готова делать иксы! 💎🚀",
    'include_pair_header': (
        '🔄 <b><u>Центр реабилитации торговых пар</u></b> 📋\n\n'
        '<i>💡 Ниже представлен ваш "черный список" 🖤 — пары, которые вы исключили вручную. '
        'Выберите, какие из <b>опальных активов</b> нужно ✅ снова начать отслеживать '
        'и дать им второй шанс на успех!</i> 🎯💰'
    ),
    'info_no_excluded_pairs': (
        '✅ <b><u>Черный список пуст!</u></b> 🤍\n\n'
        '<i>💎 Это значит, что бот сканирует все торговые пары, которые считает активными. '
        'Исключений, добавленных вручную, нет. <b>Все активы в игре!</b></i> 🎮💰'
    ),
    'info_pair_already_excluded': "ℹ️ <b>Уже в черном списке!</b> 🖤\nПара <code><b>{symbol}</b></code> на бирже <b><u>{exchange}</u></b> уже находится в изгнании. <i>Дважды исключить нельзя!</i> 😄",
    'error_no_exchange_selected': "❌ <b>Ошибка выбора!</b> 🤔 Биржа не была выбрана. <i>Попробуйте еще раз, но аккуратнее!</i>",
    'error_empty_symbol': "❌ <b>Пустой тикер!</b> 📝 Символ торговой пары не указан. <i>Напишите что-нибудь!</i>",
    'error_invalid_symbol_format': (
        "❌ <b><u>Некорректный формат тикера!</u></b> 📝❌\n\n"
        "✅ <b>Правильные примеры:</b> 👇\n"
        "• <code>BTC/USDT</code> 🪙\n"
        "• <code>ETH/BTC</code> ⚡\n"
        "• <code>SOL/USDT</code> ☀️\n\n"
        "❌ <b>Неправильные примеры:</b> 👇\n"
        "• <code>btc-usdt</code> <i>(нужен слэш /)</i>\n"
        "• <code>BTC</code> <i>(нужна вторая валюта)</i>\n\n"
        "🔄 <b>Попробуйте еще раз:</b>"
    ),
    'error_symbol_too_long': "❌ <b>Тикер слишком длинный!</b> 📏 Максимум {max_length} символов.\n<i>Попробуйте покороче:</i>",
    'error_api_negative_response': "❌ <b><u>API сказал НЕТ!</u></b> 🚫\nНе удалось <b>{action}</b>. <i>Сервер вернул отрицательный ответ. Может, он в плохом настроении?</i> 🤖😾",
    'error_internal': "❌ <b><u>Внутренняя ошибка!</u></b> ⚙️💥 <i>Что-то пошло не так в недрах системы...</i>",
    'error_invalid_callback_format': "❌ <b>Битый запрос!</b> 🔧 Некорректный формат callback данных. <i>Попробуйте еще раз!</i>",
    'error_data_outdated': "❌ <b>Устаревшие данные!</b> ⏰ Данные протухли или биржа не найдена. <i>Время обновить информацию!</i>",
    'info_list_is_empty': "📝 <b>Список пуст!</b> Список {status_text} пар для <b>{exchange}</b> <i>абсолютно пустой</i>. 🗂️",
    'info_informational_button': "ℹ️ <b>Информационная кнопка.</b> <i>Просто для красоты!</i> ✨",
    'pair_list_header': "<b><u>{status_rus} пары на {exchange}</u></b> 📊\n<i>Страница {page} из {total_pages} (всего найдено: {total_items})</i>\n\n",
    'status_type_temp_unavailable': "недоступных",
    'status_type_admin_excluded': "исключенных",
    'header_temp_unavailable': "Временно недоступные",
    'header_admin_excluded': "Исключенные администратором",
    'cache_stats_header': (
        '📊 <b><u>Картина рынка глазами робота</u></b> 🤖👁️\n\n'
        '<i>📡 Это живая статистика по торговым парам в реальном времени. '
        'Она показывает, какие активы 👀 бот видит на каждой бирже и 🎯 готов '
        'сканировать на наличие арбитражных возможностей для заработка!</i> 💰📈'
    ),
    'admin_report_exchange_header': "\n🔹 <b><u>{exchange}:</u></b>",
    'admin_report_active_line': "  - ✅ <b>Активных:</b> <code>{count}</code> 🟢",
    'admin_report_temp_unavailable_line': "  - ⚠️ <b>Временно недоступных:</b> <code>{count}</code> 🟡",
    'admin_report_admin_excluded_line': "  - 🚫 <b>Исключено вручную:</b> <code>{count}</code> 🔴",
    'admin_report_pairs_preview_line': "     ↳ <i>{pairs_preview}</i>",
    'show_all_unavailable_button': "📋 Все недоступные на {exchange} ({count})",
    'show_all_excluded_button': "📋 Все исключенные на {exchange} ({count})",
    'action_include_pair': "включить пару",
    'action_exclude_pair': "исключить пару",

    # --- Логи Админ-панели (Bot-часть) ---
    'log_admins_notification_sent': "📨 Уведомления о состоянии сканера разосланы всем VIP-трейдерам.",
    'log_admins_notification_error': "📨💥 Ошибка фонового уведомления администраторов: {error}",
    'log_cache_stats_updated': "📊 Статистика кэша обновлена для VIP-администратора.",
    'log_invalid_callback_data': "❌ Некорректный callback для списка пар: {callback_data}. Ошибка: {error}",
    'log_callback_parse_error': "🔧 Ошибка парсинга callback_data для включения пары: {error} | data: {callback_data}",

    # =================================================================
    # =============== 📊 ОТЧЕТЫ ПО СДЕЛКАМ 📊 ======================
    # =================================================================

    # --- Меню отчетов ---
    'report_menu_header': '📊 <b><u>P&L Отчеты за последние {hours} часов</u></b> 💰📈\n\n<i>Выберите тип анализа, который вас интересует:</i> 🎯',
    'report_summary_button': '📈 Краткая сводка',
    'report_detailed_button': '📄 Детальный анализ',

    # --- Сводный отчет ---
    'report_summary_title': "📊 <b><u>ПиЭл за {period} ч.</u></b> 📈💰\n",
    'report_no_data': "📭 <b>Пустота...</b> За указанный период не было зафиксировано <i>ни одной попытки заработать</i>. Может, стоит запустить сканер? 🤔💭",
    'report_summary_profit_label': "Общий профит",
    'report_summary_loss_label': "Общий слив",
    'report_summary_profit_emoji': "💰",
    'report_summary_loss_emoji': "💸",
    'report_summary_total_attempts': "<b>🎯 Всего попыток заработать:</b> {total_attempts}\n",
    'report_summary_details_header': "<b>Детализация:</b>",
    'report_summary_successful_line': "  ✅ <b>Успешных:</b> {count} (Профит: <code>+${profit:,.2f}</code>)",
    'report_summary_unprofitable_line': "  ⚠️ <b>Исполнено, но убыточно:</b> {count} (Убыток: <code>-${loss:,.2f}</code>)",
    'report_summary_failed_line': "  ❌ <b>Не исполнено:</b> {count}",
    'report_summary_failure_reasons_header': "<b>Причины неудач:</b>",

    # --- Детальный отчет ---
    'report_detailed_title': "📊 <b><u>Детальный отчет по сделкам за {period} ч.</u></b> 💰📈\n",
    'report_detailed_successful_header': "✅ <b>Успешные сделки: {count}</b> (Общий профит: <code>+${profit:,.2f}</code>)",
    'report_detailed_unprofitable_header': "⚠️ <b>Исполнено, но убыточно: {count}</b> (Общий убыток: <code>-${loss:,.2f}</code>)",
    'report_detailed_failed_header': "❌ <b>Не исполнено: {count}</b> ({reasons_summary})",
    'report_item_executed_template': (
        "  {icon} <b>{coin}</b> <a href=\"#\">{timestamp}</a>\n"
        "    ├─ Route: {route}\n"
        "    ├─ Объем: <code>${trade_value:,.2f}</code>\n"
        "    ├─ Спред: <code>{spread:,.2f}%</code>\n"
        "    └─ <b>{result_label}:</b> <code>{result_value}</code>"
    ),
    'report_item_failed_template': (
        "  📉 <b>{coin}</b> <a href=\"#\">{timestamp}</a>\n"
        "    ├─ Route: {route}\n"
        "    ├─ Потенц. спред: <code>{spread:,.2f}%</code>\n"
        "    └─ <b>Причина:</b> {reason}"
    ),
    'report_item_balance_issue_line': "      └─ <i>На {exchange} не хватило {currency}: нужно <code>{needed:,.4f}</code>, было <code>{available:,.4f}</code></i>",
    'report_item_profit_label': "Профит",
    'report_item_loss_label': "Убыток",
    'report_item_profit_icon': "📈",
    'report_item_loss_icon': "⚠️",
    'report_item_unknown_currency': "???",

    # --- Причины неудач (для отчетов) ---
    'failure_reason_insufficient_balance': "💸 <b>Слив депо</b> <i>(недостаток средств)</i>",
    'failure_reason_execution_failed': "🤖 <b>Роботы глючат</b> <i>(ошибка исполнения)</i>",
    'failure_reason_critical_error': "💥 <b>Критическая ошибка</b> <i>(внутренний сбой)</i>",
    'failure_reason_unprofitable_trade': "📉 <b>Сделка в минус</b> <i>(исполнено, но убыточно)</i>",
    'failure_reason_unknown': "🤷‍♂️ <b>Неизвестная ошибка</b> <i>(хз что случилось)</i>",

    # =================================================================
    # =============== 📈 СТРАТЕГИЯ & ЛОГИ СТРАТЕГИИ 📈 ================
    # =================================================================

    'log_strategy_init': "Стратегия арбитража инициализирована для {user_id} с суммой сделки ${trade_amount:.2f}, порогом {profit_threshold:.2%} и сервисами: {services}",
    'log_no_tracked_coins': "Нет отслеживаемых монет для сканирования.",
    'log_starting_search': "Начинаю поиск возможностей по {count} монетам.",
    'log_dynamic_pairs_check': "🔍 Динамическое определение доступных торговых пар...",
    'log_no_available_pairs': "❌ Не найдено доступных торговых пар для арбитража.",
    'log_pairs_found': "📊 Найдено {pairs_count} пар, {combinations_count} потенциальных комбинаций.",
    'log_fetching_order_books': "📚 Сбор стаканов ордеров для доступных пар...",
    'log_order_books_fetched': "📊 Стаканы получены за {fetch_time:.2f}с ({request_count} запросов).",
    'log_order_books_result': "📊 Результат получения стаканов: успешно {successful}, неудачно {failed}.",
    'log_no_opportunities_found': "Подходящих возможностей не найдено в этом цикле.",
    'log_attempting_execution': "🏆 Попытка исполнения: {symbol} (спред: {net_spread:.2%}, оценка: {score:.4f})",
    'log_execution_success': "✅ Сделка успешно выполнена.",
    'log_execution_failed_trying_next': "⚠️ Не удалось исполнить {symbol}, пробую следующую...",
    'log_execution_failed_no_more': "Не удалось исполнить ни одной возможности в этом цикле.",
    'log_market_details_missing': "Не удалось получить детали рынка для {symbol} из кэша ccxt, сделка отменена.",
    'log_invalid_precision': "Получено недопустимое значение точности для {symbol}. Сделка отменена.",
    'log_invalid_precision_exponent': "Получена некорректная (нечисловая) точность для {symbol}. Сделка отменена.",
    'log_amount_zero_after_format': "Количество для торговли {symbol} после форматирования равно нулю. Сделка отменена.",
    'log_executing_arbitrage': "Исполнение арбитража: {symbol}",
    'log_executing_buy': "Покупка: {amount:.{precision}f} {coin} на {exchange} за ~${trade_value:.2f}",
    'log_executing_sell': "Продажа: {amount:.{precision}f} {coin} с {exchange}",
    'log_opportunity_found': "✅ Найдена потенциальная возможность: {symbol} на {buy_ex} -> {sell_ex}, спред: {net_spread:.2%}",
    'log_unprofitable_opportunity_found': (
        "\n"
        "📉 Возможность по {symbol} ({buy_ex} → {sell_ex}) пропущена:\n"
        "   ├─ Спред: {net_spread:.2%} (Порог: {profit_threshold:.2%})\n"
        "   ├─ Цены (Покупка/Продажа): {buy_price:.4f} / {sell_price:.4f}\n"
        "   └─ Проскальзывание (Покупка/Продажа): {buy_slip:.2f}% / {sell_slip:.2f}%"
    ),
    'log_skip_buy_incapable': "Пропуск {symbol} ({buy_ex} → {sell_ex}): биржа {buy_ex} не может покупать (недостаточно USDT).",
    'log_skip_buy_liquidity': "Пропуск {symbol} ({buy_ex} → {sell_ex}): недостаточная ликвидность для ПОКУПКИ на {buy_ex} (доступно: ${available_liquidity:.2f} / нужно: ${required_amount:.2f}).",
    'log_skip_sell_balance': "Пропуск {symbol} ({buy_ex} → {sell_ex}): недостаточно {coin} на {sell_ex} для ПРОДАЖИ (нужно: {required:.6f}, доступно: {available:.6f}).",
    'log_skip_sell_liquidity': "Пропуск {symbol} ({buy_ex} → {sell_ex}): недостаточная ликвидность для ПРОДАЖИ на {sell_ex} (доступно: {available_liquidity:.6f} {coin} / нужно: {required_amount:.6f} {coin}).",
    'log_precision_info': "Precision для {symbol}: buy={buy_decimals}, sell={sell_decimals}, итоговая={precision_digits}",
    'log_amount_formatting_info': "Форматирование количества: {raw_amount:.8f} -> {formatted_amount:.{precision}f} (точность: {precision} зн.)",
    'log_trade_attempt': "Попытка выполнения арбитража по паре {symbol} с суммой ${amount:.2f}",
    'log_trade_pre_check_start': "Этап 0: Проверка и сохранение начальных балансов...",
    'log_trade_balances_missing': "Отсутствуют предзагруженные балансы, запрашиваю актуальные...",
    'log_trade_balance_fetch_error': "Ошибка получения баланса с {exchange}: {error}",
    'log_trade_insufficient_usdt': "ОТМЕНА: Недостаточно {currency} на {exchange}. Нужно {needed:.2f}, есть {available:.2f}",
    'log_trade_adjusting_trade_amount': "Корректировка торговой суммы: ${old_amount:.2f} -> ${new_amount:.2f}",
    'log_trade_insufficient_coin': "ОТМЕНА: Недостаточно {coin} на {exchange}. Нужно {needed:.6f}, есть {available:.6f}",
    'log_trade_adjusting_coin_amount': "Корректировка количества монет: {old_amount:.6f} -> {new_amount:.6f}",
    'log_trade_balances_ok': "Балансы перед сделкой проверены и достаточны.",
    'log_trade_starting_orders': "Этап 1: Запуск ордеров...",
    'log_trade_orders_processed': "Ордера обработаны за {time:.3f}с.",
    'log_trade_analyzing_results': "Этап 2: Анализ результатов ордеров (через API и балансы)...",
    'log_trade_api_incomplete_fill': "Анализ API показал неполное исполнение. Запуск валидации через балансы...",
    'log_trade_buy_confirmed_by_balance': "Покупка на {exchange} ПОДТВЕРЖДЕНА через баланс.",
    'log_trade_sell_confirmed_by_balance': "Продажа на {exchange} ПОДТВЕРЖДЕНА через баланс.",
    'log_trade_secondary_validation_failed': "Не удалось получить балансы для вторичной валидации.",
    'log_trade_fully_successful': "АРБИТРАЖ ПОЛНОСТЬЮ УСПЕШЕН: +${profit:.4f}",
    'log_trade_executed_unprofitable': "СДЕЛКА ИСПОЛНЕНА, НО УБЫТОЧНА: ${profit:.4f}",
    'log_trade_execution_failed': "АРБИТРАЖ НЕ ИСПОЛНЕН: ордера не исполнились.",
    'log_trade_critical_error': "Критическая ошибка при выполнении арбитража по {symbol}: {error}",
    'log_get_min_limits_error': "Ошибка получения минимальных лимитов: {error}",
    'log_get_min_coin_error': "Ошибка получения минимального количества: {error}",
    'log_loading_fees': "Загрузка торговых комиссий...",
    'log_fees_fetch_failed': "⚠️ Не удалось получить комиссии для {exchange_id} через API: {error}",
    'log_api_fees_loaded': "✅ Загружены комиссии через API для {exchange_id}: {fees}",
    'log_default_fees_applied': "📋 Для {exchange_id} применены комиссии по умолчанию: {fees}",
    'log_debug_opportunity_check': "Проверка комбинации: покупка на {buy_ex}, продажа на {sell_ex}",
    'log_balance_too_low_for_buy': "Пропуск {buy_ex}: недостаточно USDT для покупки (нужно > ${required_amount:.2f}).",
    'log_buy_analysis_failed': "Пропуск: анализ стакана на покупку для {symbol} на {exchange} не дал результата.",
    'log_sell_liquidity_too_low': "Пропуск: недостаточная ликвидность на продажу на {sell_ex} (доступно {available:.6f} из {required:.6f}).",
    'log_balance_too_low_for_sell': "Пропуск: недостаточно {coin} на {sell_ex} для продажи (нужно {required:.6f}).",

    # --- Отчеты о сделках (Bot-часть) ---
    'opportunity_execution_summary': (
        "🚀 <b><u>Найдена и выбрана лучшая возможность!</u></b>\n"
        "<b>Пара:</b> {symbol}\n"
        "<b>Чистый спред:</b> <code>{net_spread:.2%}</code> (Порог: {profit_threshold:.2%})\n"
        "<b>Оценка:</b> <code>{score:.4f}</code>\n"
        "\n"
        "🟢 <b>Покупка на {buy_exchange_name}:</b>\n"
        "   • <i>Количество:</i> <code>{amount:.{precision}f} {coin}</code>\n"
        "   • <i>Средняя цена (план):</i> <code>{buy_price:.6f}</code>\n"
        "   • <i>Проскальзывание:</i> <code>{buy_slippage:.2f}%</code>\n"
        "\n"
        "🔴 <b>Продажа на {sell_exchange_name}:</b>\n"
        "   • <i>Средняя цена (план):</i> <code>{sell_price:.6f}</code>\n"
        "   • <i>Проскальзывание:</i> <code>{sell_slippage:.2f}%</code>"
    ),
    'report_trade_final_header': "📄 <b><u>Результат сделки:</u></b>",
    'report_trade_critical_error': "🚨 <b><u>КРИТИЧЕСКАЯ ОШИБКА</u></b>\n<b>Детали:</b> <code>{error}</code>",
    'report_trade_final_success': (
            "\n\n" + "─" * 20 + "\n"
                                "🎯 <b><u>АРБИТРАЖ ЗАВЕРШЕН УСПЕШНО</u></b>\n"
                                "💰 <b>Финансовый результат:</b>\n"
                                "   • <i>Чистая прибыль:</i> <code>+${profit:,.{precision}f}</code>\n"
                                "   • <i>ROI:</i> <code>+{roi:,.2f}%</code>"
    ),
    'report_trade_final_unprofitable': (
            "\n\n" + "─" * 20 + "\n"
                                "⚠️ <b><u>СДЕЛКА ИСПОЛНЕНА, НО УБЫТОЧНА</u></b>\n"
                                "💸 <b>Финансовый результат:</b>\n"
                                "   • <i>Чистый убыток:</i> <code>-${loss:,.{precision}f}</code>\n"
                                "   • <i>ROI:</i> <code>{roi:,.2f}%</code>\n"
                                "\n<i>Причина: проскальзывание и комиссии превысили спред.</i>"
    ),
    'report_trade_final_failed': (
            "\n\n" + "─" * 20 + "\n"
                                "❌ <b><u>АРБИТРАЖ НЕ ВЫПОЛНЕН</u></b>\n"
                                "<b>Причина:</b> Неполное или неудачное исполнение ордеров."
    ),
    'report_trade_failed_diagnostics_header': "\n🔍 <b>Диагностика:</b>",
    'report_trade_failed_buy_line': "• Покупка: исполнено {filled:.6f}/{planned:.6f}",
    'report_trade_failed_sell_line': "• Продажа: исполнено {filled:.6f}/{planned:.6f}",
    'report_balance_issue_header': "⚠️ <b>Результат по паре {symbol}:</b> Сделка отменена.",
    'report_balance_issue_usdt_reason': "<b>Причина:</b> Недостаточно {currency} на {exchange}.",
    'report_balance_issue_usdt_details': "<i>(Нужно: <code>${needed:,.2f}</code>, Доступно: <code>${available:,.2f}</code>)</i>",
    'report_balance_issue_coin_reason': "<b>Причина:</b> Недостаточно {currency} на {exchange}.",
    'report_balance_issue_coin_details': "<i>(Нужно: <code>{needed:,.6f}</code>, Доступно: <code>{available:,.6f}</code>)</i>",
    'report_order_line_success': "✅ <b>{op_type} ({exchange}):</b> <code>{filled:,.6f} {coin}</code> за <code>${cost:,.2f}</code> ({fill_percent:.1f}%)",
    'report_order_line_avg_price': "   • <i>Средняя цена:</i> <code>${avg_price:,.6f}</code>",
    'report_order_line_api_error': "❌ <b>{op_type} ({exchange}):</b> Ошибка API",
    'report_order_line_api_error_details': "   • <i>Детали:</i> <code>{error}</code>",
    'report_order_line_failed': "⚠️ <b>{op_type} ({exchange}):</b> Неудачное исполнение",
    'report_order_line_failed_details': "   • <i>Исполнено:</i> <code>{filled:,.6f}/{planned:,.6f}</code> ({fill_percent:.1f}%)",

    # =================================================================
    # =============== ⚙️ ПРОЧИЕ ЛОГИ ⚙️ ===============================
    # =================================================================
    'fee_log_success': "✅ Загружены комиссии для {exchange} (метод: {method}): {fees}",
    'fee_log_default': "📋 Для {exchange} применены комиссии по умолчанию: {fees}",
    'fee_log_error': "❌ Критическая ошибка при получении комиссий для {exchange}: {error}",
    'fee_log_unreasonable_value': "⚠️ Неразумное значение комиссии {fee_type} для {exchange}: {value}. Использую дефолт.",
    'fee_log_invalid_value': "⚠️ Некорректное значение комиссии {fee_type} для {exchange}: {value}. Использую дефолт.",

    # =================================================================
    # =============== 🕵️‍♂️ РАЗВЕДКА (Reconnaissance) 🕵️‍♂️ ================
    # =================================================================

    # --- Сообщения для пользователя (Telegram) ---
    'recon_already_running_user_message': "🛰️ <b>Разведка уже запущена!</b>\n\n<i>Пожалуйста, дождитесь завершения текущего сканирования.</i>",
    'recon_timeout_user_message': "🛰️❌ <b>Ошибка!</b>\n\n<i>Операция разведки заняла слишком много времени и была прервана.</i>",
    'recon_critical_error_user_message': "🛰️❌ <b>Критическая ошибка!</b>\n\n<i>Произошел непредвиденный сбой во время разведки.</i>",
    'recon_progress_callback_header': "🛰️ <b>Идет разведка...</b>\n\n<i>{status_text}</i>",

    # --- Тексты для progress_callback ---
    'recon_progress_no_healthy_services': "❌ Нет активных бирж",
    'recon_progress_gathering_assets': "🔍 Собираю активы из кэша...",
    'recon_progress_assets_not_found': "❌ Не удалось получить список активов",
    'recon_progress_assets_found': "💰 Найдено {count} активов для анализа",
    'recon_progress_analysis_complete': "🎯 Анализ завершен! Найдено возможностей: {count}",

    # --- Детали для ошибок API (HTTPException и return) ---
    'api_error_no_admins': "ADMIN_IDS не настроены в конфигурации.",
    'api_error_balance_service_missing': "Сервис балансов (BalanceService) не был инициализирован.",
    'api_error_recon_timeout': "Операция разведки превысила установленный таймаут.",
    'api_recon_no_healthy_services': "Нет активных бирж.",

    # --- Сообщения для логгера ---
    'log_recon_already_running': "Попытка запустить новую разведку, пока предыдущая еще выполняется. Запрос отклонен.",
    'log_recon_endpoint_error': "Ошибка в эндпоинте /reconnaissance: {e}",
    'log_recon_timeout': "Операция разведки превысила таймаут в {timeout} секунд!",
    'log_recon_unexpected_error': "Непредвиденная ошибка в /reconnaissance вне блокировки: {e}",
    'log_recon_progress_update_failed': "Не удалось обновить сообщение прогресса: {e_progress}",

    # =================================================================
    # =============== 🛡️ DENSITY SCREENER (backend & bot) ===============
    # =================================================================

    # --- Тексты кнопок (с суффиксом _button) ---
    'density_screener_button': '🛡️ Скринер плотностей',
    'scan_top_100_button': f"📈 Топ-{DENSITY_SCREENER_CONFIG['TOP_COINS_BY_CAP_LIMIT']} по капитализации",
    'scan_favorites_button': '⭐ Только мои избранные',
    'select_custom_button': '✍️ Выбрать монеты вручную',
    'scan_selected_button': '✅ Сканировать выбранные',
    'back_to_screener_menu_button': '⬅️ В меню скринера',

    # --- Заголовки и сообщения ---
    'density_screener_header': '🛡️ <b>Скринер плотностей</b>',
    'density_screener_description': 'Выберите, какие активы вы хотите просканировать на наличие крупных лимитных заявок (стен):',
    'density_screener_select_custom_header': '✍️ <b>Выберите монетки  для сканирования плотностей.</b>\n\nМожно выбрать несколько или найти нужную через поиск.',
    'density_screener_no_densities_found': 'Крупных заявок по выбранным активам не обнаружено.',
    'density_screener_loading_top_100': '⏳ Загружаю список топ-100 монет...',
    'density_screener_loading_favorites': '⏳ Загружаю список ваших избранных монет...',
    'density_screener_loading_all_assets': '⏳ Загружаю список всех доступных монет...',
    'density_screener_starting_scan': '✅ Отлично! Запускаю сканирование для выбранных монет...',
    'density_screener_no_favorites': '⭐ У вас нет избранных монет. Добавьте их в настройках.',
    'density_screener_scan_failed_assets': '❌ Не удалось получить список монет для анализа.',
    'density_screener_menu_text': (
        "🛡️ <b>Скринер Плотности — Рентген Рынка</b> 🛡️\n\n"
        "Этот инструмент — ваш личный радар для обнаружения крупных лимитных ордеров (<b>«стенок»</b>), оставленных китами 🐋.\n\n"
        "Анализ этих уровней помогает предсказать возможные развороты цены и найти сильные зоны поддержки/сопротивления.\n\n"
        "👇 <b>Выберите режим сканирования:</b>\n\n"
        "📈 <b>Топ-100 по капитализации</b>\n"
        "   └ <i>Быстрый анализ самых ликвидных и известных монет рынка.</i>\n\n"
        "⭐ <b>Только мои избранные</b>\n"
        "   └ <i>Проверка только тех монет, что вы добавили в свой персональный watchlist.</i>\n\n"
        "✍️ <b>Выбрать монеты вручную</b>\n"
        "   └ <i>Точечный поиск по конкретным активам, которые вас интересуют прямо сейчас.</i>"
    ),

    'news_button': '📰 Новости',
    'news_menu_header': '📰 <b>Новостной агрегатор</b>\n\nВыберите монеты для получения последних новостей. Данные о <b>Bitcoin</b> всегда включаются в отчет.',
    'top_10_coins_button': '📈 Топ-10 по капитализации',
    'my_favorite_coins_button': '⭐ Мои избранные',
    'select_coins_manually_button': '✍️ Выбрать вручную',
    'back_to_news_menu_button': '⬅️ В меню новостей',
    'getting_news_progress': '⏳ Собираю, перевожу и анализирую новости с помощью AI... Это может занять длительное время',
    'no_news_found': '🤷‍♂️ Новостей по вашему запросу не найдено.',
    'news_api_error': '❌ Не удалось получить новости. Сервер API вернул ошибку или недоступен. Попробуйте позже.',
    'select_coins_for_news_header': '<b>Выберите монеты, по которым хотите получить новости.</b>\n\n'
                                    '<i>Данные загружены с бирж: {exchanges_text}</i>\n\n'
                                    'Вы можете переключать страницы или просто <b>отправить сообщение с названием монеты (тикер), чтобы найти её.</b>',
    'news_manual_selection_search_results': (
        '🔎 <b>Результаты поиска по «{}»:</b>\n\n'
        'Отметьте интересующие монеты и нажмите <b>\'✅ Выбрать\'</b>.\n\n'
        '<i>Для нового поиска — просто отправьте сообщение.\n'
        'Чтобы увидеть полный список — нажмите <b>\'🔄 Сбросить поиск\'</b>.</i>'
    ),
    'news_no_favorites': 'ℹ️ У вас пока нет избранных монет. Добавьте их в меню "Настройки" -> "Мои монеты".',

    # Сообщения для middleware готовности системы
    'system_initializing_message': '⏳ Система инициализируется. Пожалуйста, подождите несколько секунд и попробуйте снова.',

}

# LEXICON_RU = {
#
#     # =================================================================
#     # =============== ⚙️ API & SYSTEM (backend) ⚙️ ===================
#     # =================================================================
#
#     # --- Общие сообщения и ошибки API ---
#     'api_is_running': "🤖 <b>Машина для печати денег онлайн!</b> API работает. <i>Проверяю пульс рынка... и своих сервисов.</i>",
#     'api_error_key_not_configured': "Внутренняя ошибка сервера: ключ API не настроен.",
#     'api_error_invalid_credentials': "Не удалось подтвердить учетные данные.",
#     'api_error_balance_service_not_ready': "Сервис балансов еще не готов. Повторите попытку позже.",
#     'api_error_invalid_balance_mode': "Недопустимый режим запроса баланса. Используйте 'tracked' или 'all'.",
#     'api_error_report_generation': "Внутренняя ошибка при формировании отчета.",
#     'api_error_asset_collection': "Внутренняя ошибка при сборе списка активов.",
#     'api_error_generic': "Внутренняя ошибка сервера: {error}",
#     'api_msg_pair_excluded': "Пара {symbol} на {exchange} исключена.",
#     'api_msg_pair_included': "Пара {symbol} на {exchange} возвращена в сканирование.",
#     'cache_is_empty': (
#         'ℹ️ <b>Кэш еще пуст</b>\n\n'
#         '<i>Это нормально при первом запуске или после перезагрузки API. '
#         'Данные по активным парам появятся здесь автоматически после первого цикла сканирования.</i>'
#     ),
#
#     # --- Логи API ---
#     'log_internal_api_key_not_set': "КРИТИЧЕСКАЯ ОШИБКА: INTERNAL_API_KEY не настроен в конфигурации (.env).",
#     'log_invalid_api_key_attempt': "Попытка доступа к админ-панели с неверным API ключом: {api_key_preview}...",
#     'log_admin_request_authorized': "Успешная авторизация административного запроса.",
#     'log_assets_fetch_failed': "Не удалось получить активы с {exchange_id} для эндпоинта /assets",
#     'log_assets_endpoint_error': "Ошибка на эндпоинте /assets: {e}",
#     'log_balance_report_error': "Ошибка при генерации отчета о балансах: {e}",
#
#     # --- Сканер (API-часть) ---
#     'scanner_started': "🚀 <b>Начинаем памп!</b> Сканер активирован и уже <i>ищет неэффективности рынка.</i> Пора делать иксы! 💰",
#     'scanner_stopped': "🛑 <b>Фиксируем прибыль!</b> Сканер остановлен. <i>Надеюсь, все успели закупиться на низах?</i> 😉",
#     'job_not_found': "🤷‍♂️ <i>Кажется, кто-то поймал ликвидацию...</i> Задачу сканера не найти. <code>Error 404: Job Not Found</code>. Надо звать разработчика!",
#     'api_error_scheduler_start': "Внутренняя ошибка: не удалось запустить задачу планировщика.",
#     'status_running': "📈 <b>В рынке!</b> Сканер <i>скальпирует спреды</i> и ищет арбитражные окна. To the moon! 🌕",
#     'status_stopped': "☕️ <b>На заборе.</b> Рынок боковой, сканер ушел пить кофе. <i>Ждём волатильности!</i>",
#     'current_status': "📊 <b>Состояние нашего кибер-трейдера:</b> {status}",
#
#     # --- Логи сканера и планировщика (API-часть) ---
#     'log_started_api': "👨‍💻 [API] Сигнал 'лонг'. Активирую протоколы сканирования. <i>Let the game begin!</i>",
#     'log_stopped_api': "👨‍💻 [API] Сигнал 'шорт'. Перевожу сканер в режим HODL. <i>Все системы под контролем.</i>",
#     'log_scheduler_resumed': "Планировщик: задача сканирования возобновлена.",
#     'log_scheduler_already_active': "Планировщик: задача сканирования уже была активна.",
#     'log_scheduler_resume_error': "Критическая ошибка при возобновлении задачи планировщика: {error}",
#     'log_scheduler_paused': "Планировщик: задача сканирования поставлена на паузу.",
#     'log_scheduler_already_paused': "Планировщик: задача сканирования уже была на паузе.",
#     'log_scheduler_pause_error': "Ошибка при постановке задачи на паузу: {error}",
#
#     # --- Health Check ---
#     'health_status_ok': "✅ <b>Зелёные свечи по всем фронтам!</b> Система в идеальном состоянии. <i>Все быки на месте.</i> 🐂",
#     'health_status_degraded': "⚠️ <b>Началась коррекция!</b> Система работает, но один из сервисов <i>словил стоп-лосс.</i> Торгуем с осторожностью. 🐻",
#     'service_healthy': "👍 <b>Сигнал на покупку!</b>",
#     'service_unhealthy': "👎 <b>Медведи прорвались!</b>",
#     'ready_for_arbitrage_true': "💎🙌 <b>Да, готов ловить ракеты!</b>",
#     'ready_for_arbitrage_false': "📉 <b>Нет, рынок слишком тонкий.</b>",
#     'health_check_title': "🩺 <b>Технический анализ системы:</b>\n\n",
#     'health_check_summary': "<b>Общий тренд:</b> {status}\n",
#     'health_check_services_count': "<b>Активы в портфеле:</b> {healthy_count} из {total_count} показывают рост.\n",
#     'health_check_details_title': "<b>Разбор по каждому активу:</b>\n",
#     'health_check_service_line': "— <i>{service_name}:</i> {service_status}\n",
#     'health_check_readiness': "\n<b>Готовность к арбитражу:</b> {is_ready}",
#
#     # =================================================================
#     # =============== 🤖 TELEGRAM BOT 🤖 ==============================
#     # =================================================================
#
#     # --- Общие сообщения и ошибки ---
#     'main_menu_greeting': (
#         "<b><u>Ваш Персональный Арбитражный Ассистент</u></b>\n\n"
#         "Я готов к поиску и исполнению прибыльных сделок! 🚀\n\n"
#         "<i><b>Краткая инструкция по разделам:</b></i>\n\n"
#         "💰 <b>Баланс:</b>\n"
#         "   └─ <i>Проверяйте активы на всех биржах (общий список или только избранные монеты).</i>\n\n"
#         "📈 <b>Сканер:</b>\n"
#         "   └─ <i>Запускайте и останавливайте основной цикл поиска арбитражных возможностей.</i>\n\n"
#         "⚙️ <b>Настройки:</b>\n"
#         "   └─ <i>Управляйте списком отслеживаемых монет и ключевыми параметрами сканера (сумма сделки, порог прибыли).</i>\n\n"
#         "📊 <b>Отчеты:</b>\n"
#         "   └─ <i>Анализируйте историю сделок и финансовые результаты (доступны краткая сводка и детальный разбор).</i>\n\n"
#         "👑 <b>Админ-панель:</b>\n"
#         "   └─ <i>Получайте детальную статистику по парам и вручную управляйте исключениями.</i>"
#     ),
#     'back_to_main_menu': '🏠 Главное меню',
#     'bot_error_telegram': "❌ Ошибка на стороне Telegram. Попробуйте позже.",
#     'bot_error_menu_load_critical': "💥 <b>Крах!</b> Не могу загрузить панель управления. Что-то серьезно сломалось.",
#     'bot_error_critical': "💥 <b>Критический сбой!</b> При выполнении команды что-то взорвалось. Срочно в логи!",
#     'bot_menu_not_modified': "ℹ️ Рынок без изменений. Меню актуально.",
#     'bot_partial_fill_alert': (
#         "‼️ <b>КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ: ЧАСТИЧНОЕ ИСПОЛНЕНИЕ</b> ‼️\n\n"
#         "Произошла разбалансировка позиций по паре <b>{symbol}</b>. "
#         "Требуется срочная ручная проверка и корректировка на биржах!\n\n"
#         "<b><u>Детали Сделки:</u></b>\n"
#         "🟢 <b>Покупка ({buy_exchange}):</b>\n"
#         "   - Исполнено: <code>{buy_filled:.8f} {coin}</code>\n"
#         "   - Потрачено: <code>${buy_cost:,.2f}</code>\n"
#         "🔴 <b>Продажа ({sell_exchange}):</b>\n"
#         "   - Исполнено: <code>{sell_filled:.8f} {coin}</code>\n"
#         "   - Получено: <code>${sell_revenue:,.2f}</code>\n\n"
#         "🚨 <b>Дисбаланс Позиции:</b> <code>{imbalance:.8f} {coin}</code>"
#     ),
#
#     # --- Сканер (Bot-часть) ---
#     'bot_scanner_menu_text': (
#         "<b>Центр управления полетами 🚀</b>\n\n"
#         "<b>Текущее состояние:</b> {status}\n\n"
#         "<i>Отсюда вы отдаете приказы: отправить бота в бой за иксы или вернуть на базу для отдыха.</i>"
#     ),
#     'bot_status_active_full': "🟢 <b>В рынке!</b> Ищет профитные связки.",
#     'bot_status_stopped_full': "🔴 <b>На заборе.</b> Ждет вашего сигнала.",
#     'bot_scanner_already_running': "🚀 Куда торопишься? Бот уже летит to the moon!",
#     'bot_scanner_already_stopped': "☕️ Бот и так чиллит. Дайте ему отдохнуть.",
#     'bot_scanner_start_success': "✅ Принято! Бот отправлен на поиски арбитражных окон!",
#     'bot_scanner_stop_success': "🛑 <b>Фиксируем профит!</b> Бот успешно припаркован.",
#     'bot_scanner_status_not_changed_warning': "⚠️ <b>Странно...</b> Команда ушла, но бот не отчитался об изменении статуса. Возможно, API лагает. Проверьте логи.",
#     'bot_scanner_start_fail_api': "❌ <b>Связь потеряна!</b> Не удалось запустить сканер. Проверьте, работает ли API.",
#     'bot_scanner_stop_fail_api': "❌ <b>Не отвечает!</b> Не удалось остановить сканер. Проверьте, работает ли API.",
#     'bot_scanner_status_fetch_fail': "❌ Не могу достучаться до API, чтобы узнать статус. Похоже на обрыв связи.",
#
#     # --- Админ-панель (Bot-часть) ---
#     'admin_panel_header': (
#         '👑 <b>Административная панель</b>\n\n'
#         'Здесь вы можете 🔧 вручную влиять на то, какие торговые пары будет сканировать бот.\n\n'
#         '<i>Это полезно, чтобы временно исключить 🚫 "проблемные" активы (например, с низкой ликвидностью или зависшими ордерами) и вернуть их в работу ✅ позже.</i>'
#     ),
#     'prompt_exclude_pair': (
#         '1️⃣ <b>Шаг 1: Выбор биржи для исключения</b>\n\n'
#         '<i>Бот перестанет сканировать выбранную пару только на этой бирже. '
#         'На остальных она продолжит отслеживаться.</i>'
#     ),
#     'prompt_enter_symbol_exclude': (
#         '2️⃣ <b>Шаг 2: Ввод тикера для исключения</b>\n\n'
#         '✍️ Теперь просто отправьте в чат тикер пары, которую нужно исключить.\n\n'
#         '<i>Например:</i> `BTC/USDT`'
#     ),
#     'exclude_success': (
#         '✅ <b>Пара исключена!</b>\n\n'
#         'Пара `{symbol}` на бирже <b>{exchange}</b> больше не будет участвовать в поиске арбитража.'
#     ),
#     'include_success_formatted': "✅ <b>Успешно!</b>\nПара `{symbol}` на <b>{exchange}</b> возвращена в сканирование.",
#     'include_pair_header': (
#         '🔄 <b>Возврат пар в сканирование</b>\n\n'
#         '<i>Ниже представлен ваш "черный список" 📋 — пары, которые вы исключили вручную. '
#         'Выберите, какие из них нужно ✅ снова начать отслеживать.</i>'
#     ),
#     'info_no_excluded_pairs': (
#         '✅ <b>Список исключений пуст</b>\n\n'
#         '<i>Это значит, что бот сканирует все торговые пары, которые считает активными. '
#         'Исключений, добавленных вручную, нет.</i>'
#     ),
#     'info_pair_already_excluded': "ℹ️ <b>Уже сделано!</b>\nПара `{symbol}` на бирже <b>{exchange}</b> уже находится в списке исключений.",
#     'error_no_exchange_selected': "❌ Произошла ошибка: биржа не была выбрана. Попробуйте снова.",
#     'error_empty_symbol': "❌ Пустой символ торговой пары. Попробуйте снова.",
#     'error_invalid_symbol_format': (
#         "❌ <b>Некорректный формат символа торговой пары!</b>\n\n"
#         "✅ <b>Правильные примеры:</b>\n"
#         "• <code>BTC/USDT</code>\n"
#         "• <code>ETH/BTC</code>\n\n"
#         "❌ <b>Неправильные примеры:</b>\n"
#         "• <code>btc-usdt</code> (нужен слэш /)\n"
#         "• <code>BTC</code> (нужна вторая валюта)\n\n"
#         "Попробуйте еще раз:"
#     ),
#     'error_symbol_too_long': "❌ Символ торговой пары слишком длинный. Максимум {max_length} символ.\nПопробуйте снова:",
#     'error_api_negative_response': "❌ <b>Ошибка!</b>\nНе удалось {action}. API вернуло отрицательный ответ.",
#     'error_internal': "❌ <b>Внутренняя ошибка.</b>",
#     'error_invalid_callback_format': "❌ Ошибка: некорректный формат запроса.",
#     'error_data_outdated': "❌ Ошибка: данные устарели или биржа не найдена.",
#     'info_list_is_empty': "📝 Список {status_text} пар для {exchange} пуст.",
#     'info_informational_button': "ℹ️ Это информационная кнопка.",
#     'pair_list_header': "<b>{status_rus} пары на {exchange}</b>\n<i>Страница {page} из {total_pages} (всего: {total_items})</i>\n\n",
#     'status_type_temp_unavailable': "недоступных",
#     'status_type_admin_excluded': "исключенных",
#     'header_temp_unavailable': "Временно недоступные",
#     'header_admin_excluded': "Исключенные администратором",
#     'cache_stats_header': (
#         '📊 <b>Картина Рынка Глазами Бота</b>\n\n'
#         '<i>📡 Это живая статистика по торговым парам. Она показывает, какие активы 👀 бот видит на каждой бирже и 🎯 готов сканировать на наличие арбитражных возможностей.</i>\n'
#     ),
#     'admin_report_exchange_header': "\n🔹 <b>{exchange}:</b>",
#     'admin_report_active_line': "  - ✅ Активных: `{count}`",
#     'admin_report_temp_unavailable_line': "  - ⚠️ Временно недоступных: `{count}`",
#     'admin_report_admin_excluded_line': "  - 🚫 Исключено вручную: `{count}`",
#     'admin_report_pairs_preview_line': "     ↳ {pairs_preview}",
#     'show_all_unavailable_button': "📋 Все недоступные на {exchange} ({count})",
#     'show_all_excluded_button': "📋 Все исключенные на {exchange} ({count})",
#     'action_include_pair': "включить пару",
#     'action_exclude_pair': "исключить пару",
#
#     # --- Логи Админ-панели (Bot-часть) ---
#     'log_admins_notification_sent': "Уведомления о состоянии сканера разосланы всем администраторам.",
#     'log_admins_notification_error': "Ошибка фонового уведомления администраторов: {error}",
#     'log_cache_stats_updated': "Статистика кэша обновлена для администратора.",
#     'log_invalid_callback_data': "Некорректный callback для списка пар: {callback_data}. Ошибка: {error}",
#     'log_callback_parse_error': "Ошибка парсинга callback_data для включения пары: {error} | data: {callback_data}",
#
#     # =================================================================
#     # =============== 📊 ОТЧЕТЫ 📊 =====================================
#     # =================================================================
#
#     # --- Меню отчетов ---
#     'report_menu_header': '📊 <b>Отчеты по сделкам за {hours} часа</b>\n\nВыберите тип отчета, который вас интересует.',
#     'report_summary_button': '📈 Сводка',
#     'report_detailed_button': '📄 Детально',
#
#     # --- Сводный отчет ---
#     'report_summary_title': "📊 <b>Расширенный отчет за {period} ч.</b>\n",
#     'report_no_data': "📭 За указанный период не было зафиксировано ни одной сделки.",
#     'report_summary_profit_label': "Общий профит",
#     'report_summary_loss_label': "Общий убыток",
#     'report_summary_profit_emoji': "💰",
#     'report_summary_loss_emoji': "💸",
#     'report_summary_total_attempts': "<b>Всего попыток:</b> {total_attempts}\n",
#     'report_summary_details_header': "<b>Детализация:</b>",
#     'report_summary_successful_line': "  ✅ <b>Успешных:</b> {count} (Профит: <code>+${profit:,.2f}</code>)",
#     'report_summary_unprofitable_line': "  ⚠️ <b>Исполнено, но убыточно:</b> {count} (Убыток: <code>-${loss:,.2f}</code>)",
#     'report_summary_failed_line': "  ❌ <b>Не исполнено:</b> {count}",
#     'report_summary_failure_reasons_header': "<b>Причины неудач:</b>",
#
#     # --- Детальный отчет ---
#     'report_detailed_title': "📊 <b>Детальный отчет по сделкам за {period} ч.</b>\n",
#     'report_detailed_successful_header': "✅ <b>Успешные сделки: {count}</b> (Общий профит: <code>+${profit:,.2f}</code>)",
#     'report_detailed_unprofitable_header': "⚠️ <b>Исполнено, но убыточно: {count}</b> (Общий убыток: <code>-${loss:,.2f}</code>)",
#     'report_detailed_failed_header': "❌ <b>Не исполнено: {count}</b> ({reasons_summary})",
#     'report_item_executed_template': (
#         "  {icon} <b>{coin}</b> <a href=\"#\">{timestamp}</a>\n"
#         "    ├─ Route: {route}\n"
#         "    ├─ Объем: <code>${trade_value:,.2f}</code>\n"
#         "    ├─ Спред: <code>{spread:,.2f}%</code>\n"
#         "    └─ <b>{result_label}:</b> <code>{result_value}</code>"
#     ),
#     'report_item_failed_template': (
#         "  📉 <b>{coin}</b> <a href=\"#\">{timestamp}</a>\n"
#         "    ├─ Route: {route}\n"
#         "    ├─ Потенц. спред: <code>{spread:,.2f}%</code>\n"
#         "    └─ <b>Причина:</b> {reason}"
#     ),
#     'report_item_balance_issue_line': "      └─ <i>На {exchange} не хватило {currency}: нужно <code>{needed:,.4f}</code>, было <code>{available:,.4f}</code></i>",
#     'report_item_profit_label': "Профит",
#     'report_item_loss_label': "Убыток",
#     'report_item_profit_icon': "📈",
#     'report_item_loss_icon': "⚠️",
#     'report_item_unknown_currency': "???",
#
#     # --- Причины неудач (для отчетов) ---
#     'failure_reason_insufficient_balance': "Недостаток средств",
#     'failure_reason_execution_failed': "Ошибка исполнения",
#     'failure_reason_critical_error': "Критическая ошибка",
#     'failure_reason_unprofitable_trade': "Исполнено, но убыточно",
#     'failure_reason_unknown': "Неизвестная ошибка",
#
#     # =================================================================
#     # =============== 📈 СТРАТЕГИЯ & ЛОГИ СТРАТЕГИИ 📈 ================
#     # =================================================================
#
#     'log_strategy_init': "Стратегия арбитража инициализирована для {user_id} с суммой сделки ${trade_amount:.2f}, порогом {profit_threshold:.2%} и сервисами: {services}",
#     'log_no_tracked_coins': "Нет отслеживаемых монет для сканирования.",
#     'log_starting_search': "Начинаю поиск возможностей по {count} монетам.",
#     'log_dynamic_pairs_check': "🔍 Динамическое определение доступных торговых пар...",
#     'log_no_available_pairs': "❌ Не найдено доступных торговых пар для арбитража.",
#     'log_pairs_found': "📊 Найдено {pairs_count} пар, {combinations_count} потенциальных комбинаций.",
#     'log_fetching_order_books': "📚 Сбор стаканов ордеров для доступных пар...",
#     'log_order_books_fetched': "📊 Стаканы получены за {fetch_time:.2f}с ({request_count} запросов).",
#     'log_order_books_result': "📊 Результат получения стаканов: успешно {successful}, неудачно {failed}.",
#     'log_no_opportunities_found': "Подходящих возможностей не найдено в этом цикле.",
#     'log_attempting_execution': "🏆 Попытка исполнения: {symbol} (спред: {net_spread:.2%}, оценка: {score:.4f})",
#     'log_execution_success': "✅ Сделка успешно выполнена.",
#     'log_execution_failed_trying_next': "⚠️ Не удалось исполнить {symbol}, пробую следующую...",
#     'log_execution_failed_no_more': "Не удалось исполнить ни одной возможности в этом цикле.",
#     'log_market_details_missing': "Не удалось получить детали рынка для {symbol} из кэша ccxt, сделка отменена.",
#     'log_invalid_precision': "Получено недопустимое значение точности для {symbol}. Сделка отменена.",
#     'log_invalid_precision_exponent': "Получена некорректная (нечисловая) точность для {symbol}. Сделка отменена.",
#     'log_amount_zero_after_format': "Количество для торговли {symbol} после форматирования равно нулю. Сделка отменена.",
#     'log_executing_arbitrage': "Исполнение арбитража: {symbol}",
#     'log_executing_buy': "Покупка: {amount:.{precision}f} {coin} на {exchange} за ~${trade_value:.2f}",
#     'log_executing_sell': "Продажа: {amount:.{precision}f} {coin} с {exchange}",
#     'log_opportunity_found': "✅ Найдена потенциальная возможность: {symbol} на {buy_ex} -> {sell_ex}, спред: {net_spread:.2%}",
#     'log_unprofitable_opportunity_found': (
#         "\n"
#         "📉 Возможность по {symbol} ({buy_ex} → {sell_ex}) пропущена:\n"
#         "   ├─ Спред: {net_spread:.2%} (Порог: {profit_threshold:.2%})\n"
#         "   ├─ Цены (Покупка/Продажа): {buy_price:.4f} / {sell_price:.4f}\n"
#         "   └─ Проскальзывание (Покупка/Продажа): {buy_slip:.2f}% / {sell_slip:.2f}%"
#     ),
#     'log_skip_buy_incapable': "Пропуск {symbol} ({buy_ex} → {sell_ex}): биржа {buy_ex} не может покупать (недостаточно USDT).",
#     'log_skip_buy_liquidity': "Пропуск {symbol} ({buy_ex} → {sell_ex}): недостаточная ликвидность для ПОКУПКИ на {buy_ex} (доступно: ${available_liquidity:.2f} / нужно: ${required_amount:.2f}).",
#     'log_skip_sell_balance': "Пропуск {symbol} ({buy_ex} → {sell_ex}): недостаточно {coin} на {sell_ex} для ПРОДАЖИ (нужно: {required:.6f}, доступно: {available:.6f}).",
#     'log_skip_sell_liquidity': "Пропуск {symbol} ({buy_ex} → {sell_ex}): недостаточная ликвидность для ПРОДАЖИ на {sell_ex} (доступно: {available_liquidity:.6f} {coin} / нужно: {required_amount:.6f} {coin}).",
#     'log_precision_info': "Precision для {symbol}: buy={buy_decimals}, sell={sell_decimals}, итоговая={precision_digits}",
#     'log_amount_formatting_info': "Форматирование количества: {raw_amount:.8f} -> {formatted_amount:.{precision}f} (точность: {precision} зн.)",
#     'log_trade_attempt': "Попытка выполнения арбитража по паре {symbol} с суммой ${amount:.2f}",
#     'log_trade_pre_check_start': "Этап 0: Проверка и сохранение начальных балансов...",
#     'log_trade_balances_missing': "Отсутствуют предзагруженные балансы, запрашиваю актуальные...",
#     'log_trade_balance_fetch_error': "Ошибка получения баланса с {exchange}: {error}",
#     'log_trade_insufficient_usdt': "ОТМЕНА: Недостаточно {currency} на {exchange}. Нужно {needed:.2f}, есть {available:.2f}",
#     'log_trade_adjusting_trade_amount': "Корректировка торговой суммы: ${old_amount:.2f} -> ${new_amount:.2f}",
#     'log_trade_insufficient_coin': "ОТМЕНА: Недостаточно {coin} на {exchange}. Нужно {needed:.6f}, есть {available:.6f}",
#     'log_trade_adjusting_coin_amount': "Корректировка количества монет: {old_amount:.6f} -> {new_amount:.6f}",
#     'log_trade_balances_ok': "Балансы перед сделкой проверены и достаточны.",
#     'log_trade_starting_orders': "Этап 1: Запуск ордеров...",
#     'log_trade_orders_processed': "Ордера обработаны за {time:.3f}с.",
#     'log_trade_analyzing_results': "Этап 2: Анализ результатов ордеров (через API и балансы)...",
#     'log_trade_api_incomplete_fill': "Анализ API показал неполное исполнение. Запуск валидации через балансы...",
#     'log_trade_buy_confirmed_by_balance': "Покупка на {exchange} ПОДТВЕРЖДЕНА через баланс.",
#     'log_trade_sell_confirmed_by_balance': "Продажа на {exchange} ПОДТВЕРЖДЕНА через баланс.",
#     'log_trade_secondary_validation_failed': "Не удалось получить балансы для вторичной валидации.",
#     'log_trade_fully_successful': "АРБИТРАЖ ПОЛНОСТЬЮ УСПЕШЕН: +${profit:.4f}",
#     'log_trade_executed_unprofitable': "СДЕЛКА ИСПОЛНЕНА, НО УБЫТОЧНА: ${profit:.4f}",
#     'log_trade_execution_failed': "АРБИТРАЖ НЕ ИСПОЛНЕН: ордера не исполнились.",
#     'log_trade_critical_error': "Критическая ошибка при выполнении арбитража по {symbol}: {error}",
#     'log_get_min_limits_error': "Ошибка получения минимальных лимитов: {error}",
#     'log_get_min_coin_error': "Ошибка получения минимального количества: {error}",
#
#     # --- Отчеты о сделках (Bot-часть) ---
#     'opportunity_execution_summary': (
#         "🚀 <b>Найдена и выбрана лучшая возможность!</b>\n"
#         "<b>Пара:</b> {symbol}\n"
#         "<b>Чистый спред:</b> <code>{net_spread:.2%}</code> (Порог: {profit_threshold:.2%})\n"
#         "<b>Оценка:</b> <code>{score:.4f}</code>\n"
#         "\n"
#         "🟢 <b>Покупка на {buy_exchange_name}:</b>\n"
#         "   • <i>Количество:</i> <code>{amount:.{precision}f} {coin}</code>\n"
#         "   • <i>Средняя цена (план):</i> <code>{buy_price:.6f}</code>\n"
#         "   • <i>Проскальзывание:</i> <code>{buy_slippage:.2f}%</code>\n"
#         "\n"
#         "🔴 <b>Продажа на {sell_exchange_name}:</b>\n"
#         "   • <i>Средняя цена (план):</i> <code>{sell_price:.6f}</code>\n"
#         "   • <i>Проскальзывание:</i> <code>{sell_slippage:.2f}%</code>"
#     ),
#     'report_trade_final_header': "📄 <b>Результат сделки:</b>",
#     'report_trade_critical_error': "🚨 <b>КРИТИЧЕСКАЯ ОШИБКА</b>\n<b>Детали:</b> <code>{error}</code>",
#     'report_trade_final_success': (
#             "\n\n" + "─" * 20 + "\n"
#                                 "🎯 <b>АРБИТРАЖ ЗАВЕРШЕН УСПЕШНО</b>\n"
#                                 "💰 <b>Финансовый результат:</b>\n"
#                                 "   • <i>Чистая прибыль:</i> <code>+${profit:,.{precision}f}</code>\n"
#                                 "   • <i>ROI:</i> <code>+{roi:,.2f}%</code>"
#     ),
#     'report_trade_final_unprofitable': (
#             "\n\n" + "─" * 20 + "\n"
#                                 "⚠️ <b>СДЕЛКА ИСПОЛНЕНА, НО УБЫТОЧНА</b>\n"
#                                 "💸 <b>Финансовый результат:</b>\n"
#                                 "   • <i>Чистый убыток:</i> <code>-${loss:,.{precision}f}</code>\n"
#                                 "   • <i>ROI:</i> <code>{roi:,.2f}%</code>\n"
#                                 "\n<i>Причина: проскальзывание и комиссии превысили спред.</i>"
#     ),
#     'report_trade_final_failed': (
#             "\n\n" + "─" * 20 + "\n"
#                                 "❌ <b>АРБИТРАЖ НЕ ВЫПОЛНЕН</b>\n"
#                                 "<b>Причина:</b> Неполное или неудачное исполнение ордеров."
#     ),
#     'report_trade_failed_diagnostics_header': "\n🔍 <b>Диагностика:</b>",
#     'report_trade_failed_buy_line': "• Покупка: исполнено {filled:.6f}/{planned:.6f}",
#     'report_trade_failed_sell_line': "• Продажа: исполнено {filled:.6f}/{planned:.6f}",
#     'report_balance_issue_header': "⚠️ <b>Результат по паре {symbol}:</b> Сделка отменена.",
#     'report_balance_issue_usdt_reason': "<b>Причина:</b> Недостаточно {currency} на {exchange}.",
#     'report_balance_issue_usdt_details': "<i>(Нужно: <code>${needed:,.2f}</code>, Доступно: <code>${available:,.2f}</code>)</i>",
#     'report_balance_issue_coin_reason': "<b>Причина:</b> Недостаточно {currency} на {exchange}.",
#     'report_balance_issue_coin_details': "<i>(Нужно: <code>{needed:,.6f}</code>, Доступно: <code>{available:,.6f}</code>)</i>",
#     'report_order_line_success': "✅ <b>{op_type} ({exchange}):</b> <code>{filled:,.6f} {coin}</code> за <code>${cost:,.2f}</code> ({fill_percent:.1f}%)",
#     'report_order_line_avg_price': "   • <i>Средняя цена:</i> <code>${avg_price:,.6f}</code>",
#     'report_order_line_api_error': "❌ <b>{op_type} ({exchange}):</b> Ошибка API",
#     'report_order_line_api_error_details': "   • <i>Детали:</i> <code>{error}</code>",
#     'report_order_line_failed': "⚠️ <b>{op_type} ({exchange}):</b> Неудачное исполнение",
#     'report_order_line_failed_details': "   • <i>Исполнено:</i> <code>{filled:,.6f}/{planned:,.6f}</code> ({fill_percent:.1f}%)",
#
#     # =================================================================
#     # =============== ⚙️ ПРОЧИЕ ЛОГИ ⚙️ ===============================
#     # =================================================================
#     'fee_log_success': "✅ Загружены комиссии для {exchange} (метод: {method}): {fees}",
#     'fee_log_default': "📋 Для {exchange} применены комиссии по умолчанию: {fees}",
#     'fee_log_error': "❌ Критическая ошибка при получении комиссий для {exchange}: {error}",
#     'fee_log_unreasonable_value': "⚠️ Неразумное значение комиссии {fee_type} для {exchange}: {value}. Использую дефолт.",
#     'fee_log_invalid_value': "⚠️ Некорректное значение комиссии {fee_type} для {exchange}: {value}. Использую дефолт.",
# }


# LEXICON_RU = {
#
#     # =================================================================
#     # =============== 🤖 BOT HANDLERS (Telegram) 🤖 ===================
#     # =================================================================
#
#     # --- Главное меню ---
#     'main_menu_greeting': (
#         "<b><u>Ваш Персональный Арбитражный Ассистент</u></b>\n\n"
#         "Я готов к поиску и исполнению прибыльных сделок! 🚀\n\n"
#         "<i><b>Краткая инструкция по разделам:</b></i>\n\n"
#         "💰 <b>Баланс:</b>\n"
#         "   └─ <i>Проверяйте активы на всех биржах (общий список или только избранные монеты).</i>\n\n"
#         "📈 <b>Сканер:</b>\n"
#         "   └─ <i>Запускайте и останавливайте основной цикл поиска арбитражных возможностей.</i>\n\n"
#         "⚙️ <b>Настройки:</b>\n"
#         "   └─ <i>Управляйте списком отслеживаемых монет и ключевыми параметрами сканера (сумма сделки, порог прибыли).</i>\n\n"
#         "📊 <b>Отчеты:</b>\n"
#         "   └─ <i>Анализируйте историю сделок и финансовые результаты (доступны краткая сводка и детальный разбор).</i>\n\n"
#         "👑 <b>Админ-панель:</b>\n"
#         "   └─ <i>Получайте детальную статистику по парам и вручную управляйте исключениями.</i>"
#     ),
#
#     # =================================================================
#     # =============== ⚙️ API ROUTERS (backend) ⚙️ =====================
#     # =================================================================
#
#     # --- Сообщения для эндпоинтов ---
#     'scanner_started': "🚀 <b>Начинаем памп!</b> Сканер активирован и уже <i>ищет неэффективности рынка.</i> Пора делать иксы! 💰",
#     'scanner_stopped': "🛑 <b>Фиксируем прибыль!</b> Сканер остановлен. <i>Надеюсь, все успели закупиться на низах?</i> 😉",
#     'job_not_found': "🤷‍♂️ <i>Кажется, кто-то поймал ликвидацию...</i> Задачу сканера не найти. <code>Error 404: Job Not Found</code>. Надо звать разработчика!",
#
#     # --- Статусы сканера ---
#     'status_running': "📈 <b>В рынке!</b> Сканер <i>скальпирует спреды</i> и ищет арбитражные окна. To the moon! 🌕",
#     'status_stopped': "☕️ <b>На заборе.</b> Рынок боковой, сканер ушел пить кофе. <i>Ждём волатильности!</i>",
#
#     # --- Шаблоны для форматирования ---
#     'current_status': "📊 <b>Состояние нашего кибер-трейдера:</b> {status}",
#
#     # --- Сообщения для логгера (чтобы логи было интереснее читать) ---
#     'log_started_api': "👨‍💻 [API] Сигнал 'лонг'. Активирую протоколы сканирования. <i>Let the game begin!</i>",
#     'log_stopped_api': "👨‍💻 [API] Сигнал 'шорт'. Перевожу сканер в режим HODL. <i>Все системы под контролем.</i>",
#     'log_admins_notification_sent': "Уведомления о состоянии сканера разосланы всем администраторам.",
#     'log_admins_notification_error': "Ошибка фонового уведомления администраторов: {error}",
#     'log_scheduler_resumed': "Планировщик: задача сканирования возобновлена.",
#     'log_scheduler_already_active': "Планировщик: задача сканирования уже была активна.",
#     'log_scheduler_resume_error': "Критическая ошибка при возобновлении задачи планировщика: {error}",
#     'log_scheduler_paused': "Планировщик: задача сканирования поставлена на паузу.",
#     'log_scheduler_already_paused': "Планировщик: задача сканирования уже была на паузе.",
#     'log_scheduler_pause_error': "Ошибка при постановке задачи на паузу: {error}",
#
#     # --- Сообщения для корневого эндпоинта ("/") ---
#     'api_is_running': "🤖 <b>Машина для печати денег онлайн!</b> API работает. <i>Проверяю пульс рынка... и своих сервисов.</i>",
#
#     # --- Сообщения и статусы для health_check ("/health") ---
#     'health_status_ok': "✅ <b>Зелёные свечи по всем фронтам!</b> Система в идеальном состоянии. <i>Все быки на месте.</i> 🐂",
#     'health_status_degraded': "⚠️ <b>Началась коррекция!</b> Система работает, но один из сервисов <i>словил стоп-лосс.</i> Торгуем с осторожностью. 🐻",
#
#     'service_healthy': "👍 <b>Сигнал на покупку!</b>",
#     'service_unhealthy': "👎 <b>Медведи прорвались!</b>",
#
#     'ready_for_arbitrage_true': "💎🙌 <b>Да, готов ловить ракеты!</b>",
#     'ready_for_arbitrage_false': "📉 <b>Нет, рынок слишком тонкий.</b>",
#
#     # --- Шаблоны для health_check ---
#     'health_check_title': "🩺 <b>Технический анализ системы:</b>\n\n",
#     'health_check_summary': "<b>Общий тренд:</b> {status}\n",
#     'health_check_services_count': "<b>Активы в портфеле:</b> {healthy_count} из {total_count} показывают рост.\n",
#     'health_check_details_title': "<b>Разбор по каждому активу:</b>\n",
#     'health_check_service_line': "— <i>{service_name}:</i> {service_status}\n",
#     'health_check_readiness': "\n<b>Готовность к арбитражу:</b> {is_ready}",
#
#     # =================================================================
#     # =============== 🤖 BOT HANDLERS (Telegram) 🤖 ===================
#     # =================================================================
#
#     # --- Меню управления сканером ---
#     'bot_scanner_menu_text': (
#         "<b>Центр управления полетами 🚀</b>\n\n"
#         "<b>Текущее состояние:</b> {status}\n\n"
#         "<i>Отсюда вы отдаете приказы: отправить бота в бой за иксы или вернуть на базу для отдыха.</i>"
#     ),
#
#     'bot_status_active_full': "🟢 <b>В рынке!</b> Ищет профитные связки.",
#     'bot_status_stopped_full': "🔴 <b>На заборе.</b> Ждет вашего сигнала.",
#
#     # --- Ответы на действия со сканером (Alerts) ---
#     'bot_scanner_already_running': "🚀 Куда торопишься? Бот уже летит to the moon!",
#     'bot_scanner_already_stopped': "☕️ Бот и так чиллит. Дайте ему отдохнуть.",
#     'bot_scanner_start_success': "✅ Принято! Бот отправлен на поиски арбитражных окон!",
#     'bot_scanner_stop_success': "🛑 <b>Фиксируем профит!</b> Бот успешно припаркован.",
#
#     # --- Ответы для проверки статуса (Alerts) ---
#     'bot_scanner_check_status_template': "<b>Текущее положение дел:</b> {status}",
#     'bot_scanner_check_status_running': "🟢 <b>В рынке!</b>",
#     'bot_scanner_check_status_stopped': "🔴 <b>На заборе.</b>",
#
#     # --- Предупреждения и ошибки (Alerts) ---
#     'bot_menu_not_modified': "ℹ️ Рынок без изменений. Меню актуально.",
#     'bot_scanner_status_not_changed_warning': "⚠️ <b>Странно...</b> Команда ушла, но бот не отчитался об изменении статуса. Возможно, API лагает. Проверьте логи.",
#     'bot_scanner_start_fail_api': "❌ <b>Связь потеряна!</b> Не удалось запустить сканер. Проверьте, работает ли API.",
#     'bot_scanner_stop_fail_api': "❌ <b>Не отвечает!</b> Не удалось остановить сканер. Проверьте, работает ли API.",
#     'bot_scanner_status_fetch_fail': "❌ Не могу достучаться до API, чтобы узнать статус. Похоже на обрыв связи.",
#
#     'bot_error_telegram': "❌ Ошибка на стороне Telegram. Попробуйте позже.",
#     'bot_error_menu_load_critical': "💥 <b>Крах!</b> Не могу загрузить панель управления. Что-то серьезно сломалось.",
#     'bot_error_critical': "💥 <b>Критический сбой!</b> При выполнении команды что-то взорвалось. Срочно в логи!",
#
#     'bot_partial_fill_alert': (
#         "‼️ <b>КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ: ЧАСТИЧНОЕ ИСПОЛНЕНИЕ</b> ‼️\n\n"
#         "Произошла разбалансировка позиций по паре <b>{symbol}</b>. "
#         "Требуется срочная ручная проверка и корректировка на биржах!\n\n"
#         "<b><u>Детали Сделки:</u></b>\n"
#         "🟢 <b>Покупка ({buy_exchange}):</b>\n"
#         "   - Исполнено: <code>{buy_filled:.8f} {coin}</code>\n"
#         "   - Потрачено: <code>${buy_cost:,.2f}</code>\n"
#         "🔴 <b>Продажа ({sell_exchange}):</b>\n"
#         "   - Исполнено: <code>{sell_filled:.8f} {coin}</code>\n"
#         "   - Получено: <code>${sell_revenue:,.2f}</code>\n\n"
#         "🚨 <b>Дисбаланс Позиции:</b> <code>{imbalance:.8f} {coin}</code>"
#     ),
#     # Админ-панель
#     'admin_panel_header': (
#         '👑 <b>Административная панель</b>\n\n'
#         'Здесь вы можете 🔧 вручную влиять на то, какие торговые пары будет сканировать бот.\n\n'
#         '<i>Это полезно, чтобы временно исключить 🚫 "проблемные" активы (например, с низкой ликвидностью или зависшими ордерами) и вернуть их в работу ✅ позже.</i>'
#     ),
#     'prompt_exclude_pair': (
#         '1️⃣ <b>Шаг 1: Выбор биржи для исключения</b>\n\n'
#         '<i>Бот перестанет сканировать выбранную пару только на этой бирже. '
#         'На остальных она продолжит отслеживаться.</i>'
#     ),
#     'prompt_include_pair': (
#         '1️⃣ <b>Шаг 1: Выбор биржи для включения</b>\n\n'
#         '<i>Выберите биржу, на которой вы хотите снова начать '
#         'сканировать ранее исключенную пару.</i>'
#     ),
#     'prompt_enter_symbol_exclude': (
#         '2️⃣ <b>Шаг 2: Ввод тикера для исключения</b>\n\n'
#         '✍️ Теперь просто отправьте в чат тикер пары, которую нужно исключить.\n\n'
#         '<i>Например:</i> `BTC/USDT`'
#     ),
#     'prompt_enter_symbol_include': (
#         '2️⃣ <b>Шаг 2: Ввод тикера для включения</b>\n\n'
#         '✍️ Отправьте в чат тикер пары, которую нужно вернуть в сканирование.\n\n'
#         '<i>Например:</i> `ETH/USDT`'
#     ),
#     'exclude_success': (
#         '✅ <b>Пара исключена!</b>\n\n'
#         'Пара `{symbol}` на бирже <b>{exchange}</b> больше не будет участвовать в поиске арбитража.'
#     ),
#     'include_success': (
#         '✅ <b>Пара возвращена!</b>\n\n'
#         'Пара `{symbol}` на бирже <b>{exchange}</b> будет снова проверена в следующем цикле сканирования.'
#     ),
#     'invalid_format_error': (
#         "❌ <b>Некорректный формат символа торговой пары!</b>\n\n"
#         "✅ <b>Правильные примеры:</b>\n"
#         "• <code>BTC/USDT</code>\n"
#         "• <code>ETH/BTC</code>\n\n"
#         "❌ <b>Неправильные примеры:</b>\n"
#         "• <code>btc-usdt</code> (нужен слэш /)\n"
#         "• <code>BTC</code> (нужна вторая валюта)\n\n"
#         "Попробуйте еще раз:"
#     ),
#     'cache_is_empty': (
#         'ℹ️ <b>Кэш еще пуст</b>\n\n'
#         '<i>Это нормально при первом запуске или после перезагрузки API. '
#         'Данные по активным парам появятся здесь автоматически после первого цикла сканирования.</i>'
#     ),
#     'cache_stats_header': (
#         '📊 <b>Картина Рынка Глазами Бота</b>\n\n'
#         '<i>📡 Это живая статистика по торговым парам. Она показывает, какие активы 👀 бот видит на каждой бирже и 🎯 готов сканировать на наличие арбитражных возможностей.</i>\n'
#     ),
#     'back_to_admin_panel': '⬅️ Назад в админ-панель',
#     'back_to_main_menu': '🏠 Главное меню',
#
#     # === НОВЫЙ БЛОК: Отчеты по сделкам ===
#     'report_menu_header': '📊 <b>Отчеты по сделкам за {hours} часа</b>\n\nВыберите тип отчета, который вас интересует.',
#     'report_summary_button': '📈 Сводка',
#     'report_detailed_button': '📄 Детально',
#
#     # =================================================================
#     # =============== 📊 REPORT FORMATTER STRINGS 📊 ==================
#     # =================================================================
#
#     # --- Заголовки отчетов ---
#     'report_summary_title': "📊 <b>Расширенный отчет за {period} ч.</b>\n",
#     'report_detailed_title': "📊 <b>Детальный отчет по сделкам за {period} ч.</b>\n",
#     'report_no_data': "📭 За указанный период не было зафиксировано ни одной сделки.",
#
#     # --- Общая статистика в сводном отчете ---
#     'report_summary_profit_label': "Общий профит",
#     'report_summary_loss_label': "Общий убыток",
#     'report_summary_profit_emoji': "💰",
#     'report_summary_loss_emoji': "💸",
#     'report_summary_total_attempts': "<b>Всего попыток:</b> {total_attempts}\n",
#     'report_summary_details_header': "<b>Детализация:</b>",
#
#     # --- Строки детализации в сводном отчете ---
#     'report_summary_successful_line': "  ✅ <b>Успешных:</b> {count} (Профит: <code>+${profit:,.2f}</code>)",
#     'report_summary_unprofitable_line': "  ⚠️ <b>Исполнено, но убыточно:</b> {count} (Убыток: <code>-${loss:,.2f}</code>)",
#     'report_summary_failed_line': "  ❌ <b>Не исполнено:</b> {count}",
#     'report_summary_failure_reasons_header': "<b>Причины неудач:</b>",
#
#     # --- Заголовки секций в детальном отчете ---
#     'report_detailed_successful_header': "✅ <b>Успешные сделки: {count}</b> (Общий профит: <code>+${profit:,.2f}</code>)",
#     'report_detailed_unprofitable_header': "⚠️ <b>Исполнено, но убыточно: {count}</b> (Общий убыток: <code>-${loss:,.2f}</code>)",
#     'report_detailed_failed_header': "❌ <b>Не исполнено: {count}</b> ({reasons_summary})",
#
#     # --- Шаблоны для отдельных записей в детальном отчете ---
#     'report_item_executed_template': (
#         "  {icon} <b>{coin}</b> <a href=\"#\">{timestamp}</a>\n"
#         "    ├─ Route: {route}\n"
#         "    ├─ Объем: <code>${trade_value:,.2f}</code>\n"
#         "    ├─ Спред: <code>{spread:,.2f}%</code>\n"
#         "    └─ <b>{result_label}:</b> <code>{result_value}</code>"
#     ),
#     'report_item_failed_template': (
#         "  📉 <b>{coin}</b> <a href=\"#\">{timestamp}</a>\n"
#         "    ├─ Route: {route}\n"
#         "    ├─ Потенц. спред: <code>{spread:,.2f}%</code>\n"
#         "    └─ <b>Причина:</b> {reason}"
#     ),
#     'report_item_balance_issue_line': "      └─ <i>На {exchange} не хватило {currency}: нужно <code>{needed:,.4f}</code>, было <code>{available:,.4f}</code></i>",
#
#     # --- Иконки и метки для детального отчета ---
#     'report_item_profit_label': "Профит",
#     'report_item_loss_label': "Убыток",
#     'report_item_profit_icon': "📈",
#     'report_item_loss_icon': "⚠️",
#
#     # Заполнитель для неизвестной валюты
#     'report_item_unknown_currency': "???",
#
#     # --- Тексты для причин неудач (для reason_map) ---
#     'failure_reason_insufficient_balance': "Недостаток средств",
#     'failure_reason_execution_failed': "Ошибка исполнения",
#     'failure_reason_critical_error': "Критическая ошибка",
#     'failure_reason_unprofitable_trade': "Исполнено, но убыточно",
#     'failure_reason_unknown': "Неизвестная ошибка",
#
#     # =================================================================
#     # =============== 📈 ARBITRAGE STRATEGY LOGS 📈 ===================
#     # =================================================================
#     'log_strategy_init': "Стратегия арбитража инициализирована для {user_id} с суммой сделки ${trade_amount:.2f}, порогом {profit_threshold:.2%} и сервисами: {services}",
#     'log_no_tracked_coins': "Нет отслеживаемых монет для сканирования.",
#     'log_starting_search': "Начинаю поиск возможностей по {count} монетам.",
#     'log_loading_fees': "Загрузка торговых комиссий...",
#     'log_dynamic_pairs_check': "🔍 Динамическое определение доступных торговых пар...",
#     'log_no_available_pairs': "❌ Не найдено доступных торговых пар для арбитража.",
#     'log_pairs_found': "📊 Найдено {pairs_count} пар, {combinations_count} потенциальных комбинаций.",
#     'log_fetching_order_books': "📚 Сбор стаканов ордеров для доступных пар...",
#     'log_order_books_fetched': "📊 Стаканы получены за {fetch_time:.2f}с ({request_count} запросов).",
#     'log_order_books_result': "📊 Результат получения стаканов: успешно {successful}, неудачно {failed}.",
#     'log_no_opportunities_found': "Подходящих возможностей не найдено в этом цикле.",
#     'log_attempting_execution': "🏆 Попытка исполнения: {symbol} (спред: {net_spread:.2%}, оценка: {score:.4f})",
#     'log_execution_success': "✅ Сделка успешно выполнена.",
#     'log_execution_failed_trying_next': "⚠️ Не удалось исполнить {symbol}, пробую следующую...",
#     'log_execution_failed_no_more': "Не удалось исполнить ни одной возможности в этом цикле.",
#     'log_market_details_missing': "Не удалось получить детали рынка для {symbol} из кэша ccxt, сделка отменена.",
#     'log_invalid_precision': "Получено недопустимое значение точности для {symbol}. Сделка отменена.",
#     'log_invalid_precision_exponent': "Получена некорректная (нечисловая) точность для {symbol}. Сделка отменена.",
#     'log_amount_zero_after_format': "Количество для торговли {symbol} после форматирования равно нулю. Сделка отменена.",
#     'log_executing_arbitrage': "Исполнение арбитража: {symbol}",
#     'log_executing_buy': "Покупка: {amount:.{precision}f} {coin} на {exchange} за ~${trade_value:.2f}",
#     'log_executing_sell': "Продажа: {amount:.{precision}f} {coin} с {exchange}",
#     'log_fees_fetch_failed': "⚠️ Не удалось получить комиссии для {exchange_id} через API: {error}",
#     'log_api_fees_loaded': "✅ Загружены комиссии через API для {exchange_id}: {fees}",
#     'log_default_fees_applied': "📋 Для {exchange_id} применены комиссии по умолчанию: {fees}",
#     'log_debug_opportunity_check': "Проверка комбинации: покупка на {buy_ex}, продажа на {sell_ex}",
#     'log_balance_too_low_for_buy': "Пропуск {buy_ex}: недостаточно USDT для покупки (нужно > ${required_amount:.2f}).",
#     'log_buy_analysis_failed': "Пропуск: анализ стакана на покупку для {symbol} на {exchange} не дал результата.",
#     'log_sell_liquidity_too_low': "Пропуск: недостаточная ликвидность на продажу на {sell_ex} (доступно {available:.6f} из {required:.6f}).",
#     'log_balance_too_low_for_sell': "Пропуск: недостаточно {coin} на {sell_ex} для продажи (нужно {required:.6f}).",
#     'log_opportunity_found': "✅ Найдена потенциальная возможность: {symbol} на {buy_ex} -> {sell_ex}, спред: {net_spread:.2%}",
#     'log_unprofitable_opportunity_found': (
#         "\n"
#         "📉 Возможность по {symbol} ({buy_ex} → {sell_ex}) пропущена:\n"
#         "   ├─ Спред: {net_spread:.2%} (Порог: {profit_threshold:.2%})\n"
#         "   ├─ Цены (Покупка/Продажа): {buy_price:.4f} / {sell_price:.4f}\n"
#         "   └─ Проскальзывание (Покупка/Продажа): {buy_slip:.2f}% / {sell_slip:.2f}%"
#     ),
#     'log_skip_buy_incapable': "Пропуск {symbol} ({buy_ex} → {sell_ex}): биржа {buy_ex} не может покупать (недостаточно USDT).",
#     'log_skip_buy_liquidity': "Пропуск {symbol} ({buy_ex} → {sell_ex}): недостаточная ликвидность для ПОКУПКИ на {buy_ex} (доступно: ${available_liquidity:.2f} / нужно: ${required_amount:.2f}).",
#     'log_skip_sell_balance': "Пропуск {symbol} ({buy_ex} → {sell_ex}): недостаточно {coin} на {sell_ex} для ПРОДАЖИ (нужно: {required:.6f}, доступно: {available:.6f}).",
#     'log_skip_sell_liquidity': "Пропуск {symbol} ({buy_ex} → {sell_ex}): недостаточная ликвидность для ПРОДАЖИ на {sell_ex} (доступно: {available_liquidity:.6f} {coin} / нужно: {required_amount:.6f} {coin}).",
#     'log_precision_info': "Precision для {symbol}: buy={buy_decimals}, sell={sell_decimals}, итоговая={precision_digits}",
#     'log_amount_formatting_info': "Форматирование количества: {raw_amount:.8f} -> {formatted_amount:.{precision}f} (точность: {precision} зн.)",
#
#     # Шаблон для отчета о найденной и исполняемой возможности
#     'opportunity_execution_summary': (
#         "🚀 <b>Найдена и выбрана лучшая возможность!</b>\n"
#         "<b>Пара:</b> {symbol}\n"
#         "<b>Чистый спред:</b> <code>{net_spread:.2%}</code> (Порог: {profit_threshold:.2%})\n"
#         "<b>Оценка:</b> <code>{score:.4f}</code>\n"
#         "\n"
#         "🟢 <b>Покупка на {buy_exchange_name}:</b>\n"
#         "   • <i>Количество:</i> <code>{amount:.{precision}f} {coin}</code>\n"
#         "   • <i>Средняя цена (план):</i> <code>{buy_price:.6f}</code>\n"
#         "   • <i>Проскальзывание:</i> <code>{buy_slippage:.2f}%</code>\n"
#         "\n"
#         "🔴 <b>Продажа на {sell_exchange_name}:</b>\n"
#         "   • <i>Средняя цена (план):</i> <code>{sell_price:.6f}</code>\n"
#         "   • <i>Проскальзывание:</i> <code>{sell_slippage:.2f}%</code>"
#     ),
#     'log_trade_attempt': "Попытка выполнения арбитража по паре {symbol} с суммой ${amount:.2f}",
#     'log_trade_pre_check_start': "Этап 0: Проверка и сохранение начальных балансов...",
#     'log_trade_balances_missing': "Отсутствуют предзагруженные балансы, запрашиваю актуальные...",
#     'log_trade_balance_fetch_error': "Ошибка получения баланса с {exchange}: {error}",
#     'log_trade_insufficient_usdt': "ОТМЕНА: Недостаточно {currency} на {exchange}. Нужно {needed:.2f}, есть {available:.2f}",
#     'log_trade_adjusting_trade_amount': "Корректировка торговой суммы: ${old_amount:.2f} -> ${new_amount:.2f}",
#     'log_trade_insufficient_coin': "ОТМЕНА: Недостаточно {coin} на {exchange}. Нужно {needed:.6f}, есть {available:.6f}",
#     'log_trade_adjusting_coin_amount': "Корректировка количества монет: {old_amount:.6f} -> {new_amount:.6f}",
#     'log_trade_balances_ok': "Балансы перед сделкой проверены и достаточны.",
#     'log_trade_starting_orders': "Этап 1: Запуск ордеров...",
#     'log_trade_orders_processed': "Ордера обработаны за {time:.3f}с.",
#     'log_trade_analyzing_results': "Этап 2: Анализ результатов ордеров (через API и балансы)...",
#     'log_trade_api_incomplete_fill': "Анализ API показал неполное исполнение. Запуск валидации через балансы...",
#     'log_trade_buy_confirmed_by_balance': "Покупка на {exchange} ПОДТВЕРЖДЕНА через баланс.",
#     'log_trade_sell_confirmed_by_balance': "Продажа на {exchange} ПОДТВЕРЖДЕНА через баланс.",
#     'log_trade_secondary_validation_failed': "Не удалось получить балансы для вторичной валидации.",
#     'log_trade_fully_successful': "АРБИТРАЖ ПОЛНОСТЬЮ УСПЕШЕН: +${profit:.4f}",
#     'log_trade_executed_unprofitable': "СДЕЛКА ИСПОЛНЕНА, НО УБЫТОЧНА: ${profit:.4f}",
#     'log_trade_execution_failed': "АРБИТРАЖ НЕ ИСПОЛНЕН: ордера не исполнились.",
#     'log_trade_critical_error': "Критическая ошибка при выполнении арбитража по {symbol}: {error}",
#
#     # --- Логирование в других методах ---
#     'log_get_min_limits_error': "Ошибка получения минимальных лимитов: {error}",
#     'log_get_min_coin_error': "Ошибка получения минимального количества: {error}",
#
#     # --- Шаблоны отчетов для пользователя ---
#     'report_trade_final_header': "📄 <b>Результат сделки:</b>",
#     'report_trade_critical_error': "🚨 <b>КРИТИЧЕСКАЯ ОШИБКА</b>\n<b>Детали:</b> <code>{error}</code>",
#
#     # --- Шаблон для успешной сделки ---
#     'report_trade_final_success': (
#             "\n\n" + "─" * 20 + "\n"
#                                 "🎯 <b>АРБИТРАЖ ЗАВЕРШЕН УСПЕШНО</b>\n"
#                                 "💰 <b>Финансовый результат:</b>\n"
#                                 "   • <i>Чистая прибыль:</i> <code>+${profit:,.{precision}f}</code>\n"
#                                 "   • <i>ROI:</i> <code>+{roi:,.2f}%</code>"
#     ),
#
#     # --- Шаблон для убыточной, но исполненной сделки ---
#     'report_trade_final_unprofitable': (
#             "\n\n" + "─" * 20 + "\n"
#                                 "⚠️ <b>СДЕЛКА ИСПОЛНЕНА, НО УБЫТОЧНА</b>\n"
#                                 "💸 <b>Финансовый результат:</b>\n"
#                                 "   • <i>Чистый убыток:</i> <code>-${loss:,.{precision}f}</code>\n"
#                                 "   • <i>ROI:</i> <code>{roi:,.2f}%</code>\n"
#                                 "\n<i>Причина: проскальзывание и комиссии превысили спред.</i>"
#     ),
#
#     # --- Шаблон для полностью проваленной сделки ---
#     'report_trade_final_failed': (
#             "\n\n" + "─" * 20 + "\n"
#                                 "❌ <b>АРБИТРАЖ НЕ ВЫПОЛНЕН</b>\n"
#                                 "<b>Причина:</b> Неполное или неудачное исполнение ордеров."
#     ),
#     'report_trade_failed_diagnostics_header': "\n🔍 <b>Диагностика:</b>",
#     'report_trade_failed_buy_line': "• Покупка: исполнено {filled:.6f}/{planned:.6f}",
#     'report_trade_failed_sell_line': "• Продажа: исполнено {filled:.6f}/{planned:.6f}",
#
#     # --- Шаблоны для отчета о проблеме с балансом (_create_balance_issue_report) ---
#     'report_balance_issue_header': "⚠️ <b>Результат по паре {symbol}:</b> Сделка отменена.",
#     'report_balance_issue_usdt_reason': "<b>Причина:</b> Недостаточно {currency} на {exchange}.",
#     'report_balance_issue_usdt_details': "<i>(Нужно: <code>${needed:,.2f}</code>, Доступно: <code>${available:,.2f}</code>)</i>",
#     'report_balance_issue_coin_reason': "<b>Причина:</b> Недостаточно {currency} на {exchange}.",
#     'report_balance_issue_coin_details': "<i>(Нужно: <code>{needed:,.6f}</code>, Доступно: <code>{available:,.6f}</code>)</i>",
#
#     # --- Шаблоны для форматирования строки ордера (_format_order_report_line) ---
#     'report_order_line_success': "✅ <b>{op_type} ({exchange}):</b> <code>{filled:,.6f} {coin}</code> за <code>${cost:,.2f}</code> ({fill_percent:.1f}%)",
#     'report_order_line_avg_price': "   • <i>Средняя цена:</i> <code>${avg_price:,.6f}</code>",
#     'report_order_line_api_error': "❌ <b>{op_type} ({exchange}):</b> Ошибка API",
#     'report_order_line_api_error_details': "   • <i>Детали:</i> <code>{error}</code>",
#     'report_order_line_failed': "⚠️ <b>{op_type} ({exchange}):</b> Неудачное исполнение",
#     'report_order_line_failed_details': "   • <i>Исполнено:</i> <code>{filled:,.6f}/{planned:,.6f}</code> ({fill_percent:.1f}%)",
#
#     # =================================================================
#     # =============== ⚙️ FEE FETCHING LOGS (Internal) ⚙️ ================
#     # =================================================================
#     'fee_log_success': "✅ Загружены комиссии для {exchange} (метод: {method}): {fees}",
#     'fee_log_default': "📋 Для {exchange} применены комиссии по умолчанию: {fees}",
#     'fee_log_error': "❌ Критическая ошибка при получении комиссий для {exchange}: {error}",
#     'fee_log_unreasonable_value': "⚠️ Неразумное значение комиссии {fee_type} для {exchange}: {value}. Использую дефолт.",
#     'fee_log_invalid_value': "⚠️ Некорректное значение комиссии {fee_type} для {exchange}: {value}. Использую дефолт.",
#
#     # БЛОК ДЛЯ ОШИБОК API
#     'api_error_balance_service_not_ready': "Сервис балансов еще не готов. Повторите попытку позже.",
#     'api_error_invalid_balance_mode': "Недопустимый режим запроса баланса. Используйте 'tracked' или 'all'.",
#     'api_error_report_generation': "Внутренняя ошибка при формировании отчета.",
#     'api_error_asset_collection': "Внутренняя ошибка при сборе списка активов.",
#     'log_internal_api_key_not_set': "КРИТИЧЕСКАЯ ОШИБКА: INTERNAL_API_KEY не настроен в конфигурации (.env).",
#     'log_invalid_api_key_attempt': "Попытка доступа к админ-панели с неверным API ключом: {api_key_preview}...",
#     'log_admin_request_authorized': "Успешная авторизация административного запроса.",
#
#     # --- Сообщения об ошибках для клиента API ---
#     'api_error_key_not_configured': "Внутренняя ошибка сервера: ключ API не настроен.",
#     'api_error_invalid_credentials': "Не удалось подтвердить учетные данные.",
#
#     # =================================================================
#     # =============== 👑 Admin Panel & Keyboards 👑 ===================
#     # =================================================================
#
#     # --- Тексты кнопок (с суффиксом _button) ---
#     'admin_panel_button': '👑 Админ-панель',
#     'pair_status_button': '📊 Статус пар (кэш)',
#     'exclude_pair_button': '🚫 Исключить пару',
#     'include_pair_button': '✅ Вернуть в сканер',
#     'back_to_main_menu_button': '🏠 Главное меню',
#     'back_to_admin_panel_button': '⬅️ Назад в админ-панель',
#     'back_to_settings_button': '⬅️ Назад в Настройки',
#     'back_to_statistics_button': '⬅️ Назад к статистике',
#     'refresh_button': '🔄 Обновить',
#     'all_assets_button': '📊 Все активы',
#     'tracked_assets_button': '⭐ Избранные',
#     'settings_button': '⚙️ Настройки',
#     'my_coins_button': '✨ Мои монеты',
#     'add_coin_button': '➕ Добавить монеты',
#     'remove_coin_button': '🗑️ Удалить монету',
#     'scanner_settings_button': '📈 Настройки сканера',
#     'pagination_back_button': '⬅️ Назад',
#     'pagination_forward_button': 'Вперед ➡️',
#     'confirm_add_coins_button': '✅ Сохранить',
#     'cancel_button': '🚫 Отмена',
#     'clear_search_button': '🔄 Сбросить поиск',
#     'confirm_remove_coins_button': '🗑️ Удалить выбранные',
#     'scanner_status_button': '📈 Сканер',
#     'report_menu_button': '📊 Отчет по сделкам',
#     'start_scanner_button': '▶️ Запустить сканер',
#     'stop_scanner_button': '⏹️ Остановить сканер',
#     'check_status_button_short': '🟢 Статус: Запущен',
#     'check_status_button_long': '🔴 Статус: Остановлен',
#     'stop_scanner_button_short': '⏹️ Остановить',
#     'start_scanner_button_short': '▶️ Запустить',
#     'change_trade_amount_button': '✍️ Изменить сумму сделки',
#     'change_profit_threshold_button': '✍️ Изменить порог прибыльности',
#     'reset_trade_amount_button': '🔄 Сбросить сумму к значению по умолчанию (${default_amount:.2f})',
#     'reset_profit_threshold_button': '🔄 Сбросить порог к значению по умолчанию ({default_threshold:.2f}%)',
#     'no_excluded_pairs_button': "📝 Нет исключенных пар",
#     'exchange_header_button': "🏢 {exchange}",
#     'include_pair_symbol_button': "✅ {symbol}",
#
#     # --- Тексты для форматирования отчета в админ-панели ---
#     'info_pair_already_excluded': "ℹ️ <b>Уже сделано!</b>\nПара `{symbol}` на бирже <b>{exchange}</b> уже находится в списке исключений.",
#     'admin_report_exchange_header': "\n🔹 <b>{exchange}:</b>",
#     'admin_report_active_line': "  - ✅ Активных: `{count}`",
#     'admin_report_temp_unavailable_line': "  - ⚠️ Временно недоступных: `{count}`",
#     'admin_report_admin_excluded_line': "  - 🚫 Исключено вручную: `{count}`",
#     'admin_report_pairs_preview_line': "     ↳ {pairs_preview}",
#
#     # --- Тексты для кнопок в get_cache_stats_keyboard ---
#     'show_all_unavailable_button': "📋 Все недоступные на {exchange} ({count})",
#     'show_all_excluded_button': "📋 Все исключенные на {exchange} ({count})",
#
#     # =================================================================
#     # =============== 👑 Admin Panel Handlers 👑 =====================
#     # =================================================================
#
#     'log_cache_stats_updated': "Статистика кэша обновлена для администратора.",
#     'log_invalid_callback_data': "Некорректный callback для списка пар: {callback_data}. Ошибка: {error}",
#     'log_callback_parse_error': "Ошибка парсинга callback_data для включения пары: {error} | data: {callback_data}",
#
#     # --- Сообщения об ошибках ---
#     'error_invalid_callback_format': "❌ Ошибка: некорректный формат запроса.",
#     'error_data_outdated': "❌ Ошибка: данные устарели или биржа не найдена.",
#     'error_no_exchange_selected': "❌ Произошла ошибка: биржа не была выбрана. Попробуйте снова.",
#     'error_empty_symbol': "❌ Пустой символ торговой пары. Попробуйте снова.",
#     'error_invalid_symbol_format': (
#         "❌ <b>Некорректный формат символа торговой пары!</b>\n\n"
#         "✅ <b>Правильные примеры:</b>\n"
#         "• <code>BTC/USDT</code>\n"
#         "• <code>ETH/BTC</code>\n\n"
#         "❌ <b>Неправильные примеры:</b>\n"
#         "• <code>btc-usdt</code> (нужен слэш /)\n"
#         "• <code>BTC</code> (нужна вторая валюта)\n\n"
#         "Попробуйте еще раз:"
#     ),
#     'error_symbol_too_long': "❌ Символ торговой пары слишком длинный. Максимум {max_length} символ.\nПопробуйте снова:",
#     'error_api_negative_response': "❌ <b>Ошибка!</b>\nНе удалось {action}. API вернуло отрицательный ответ.",
#     'error_internal': "❌ <b>Внутренняя ошибка.</b>",
#
#     # --- Сообщения об успехе ---
#     'include_success_formatted': "✅ <b>Успешно!</b>\nПара `{symbol}` на <b>{exchange}</b> возвращена в сканирование.",
#
#     # --- Информационные сообщения ---
#     'info_list_is_empty': "📝 Список {status_text} пар для {exchange} пуст.",
#     'info_no_excluded_pairs': (
#         '✅ <b>Список исключений пуст</b>\n\n'
#         '<i>Это значит, что бот сканирует все торговые пары, которые считает активными. '
#         'Исключений, добавленных вручную, нет.</i>'
#     ),
#     'info_informational_button': "ℹ️ Это информационная кнопка.",
#
#     # --- Заголовки и тексты меню ---
#     'include_pair_header': (
#         '🔄 <b>Возврат пар в сканирование</b>\n\n'
#         '<i>Ниже представлен ваш "черный список" 📋 — пары, которые вы исключили вручную. '
#         'Выберите, какие из них нужно ✅ снова начать отслеживать.</i>'
#     ),
#     'pair_list_header': "<b>{status_rus} пары на {exchange}</b>\n<i>Страница {page} из {total_pages} (всего: {total_items})</i>\n\n",
#
#     'status_type_temp_unavailable': "недоступных",
#     'status_type_admin_excluded': "исключенных",
#     'header_temp_unavailable': "Временно недоступные",
#     'header_admin_excluded': "Исключенные администратором",
#
#     # =================================================================
#     # =============== ⚙️ SYSTEM ROUTER LOGS & MESSAGES ⚙️ ================
#     # =================================================================
#     'log_assets_fetch_failed': "Не удалось получить активы с {exchange_id} для эндпоинта /assets",
#     'log_assets_endpoint_error': "Ошибка на эндпоинте /assets: {e}",
#     'log_balance_report_error': "Ошибка при генерации отчета о балансах: {e}",
#
#     # --- Сообщения для ответов API ---
#     'api_msg_pair_excluded': "Пара {symbol} на {exchange} исключена.",
#     'api_msg_pair_included': "Пара {symbol} на {exchange} возвращена в сканирование.",
#     'api_error_generic': "Внутренняя ошибка сервера: {error}",
#
# }
