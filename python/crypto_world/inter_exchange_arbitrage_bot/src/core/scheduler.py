# inter_exchange_arbitrage_bot/src/core/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Создаем единый экземпляр планировщика для всего приложения
scheduler = AsyncIOScheduler()
