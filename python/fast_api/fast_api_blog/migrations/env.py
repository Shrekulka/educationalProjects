from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from database.database import Base
from alembic import context

# Это объект конфигурации Alembic, который предоставляет
# доступ к значениям в используемом файле .ini.
config = context.config

# Интерпретируем файл конфигурации для Python logging.
# Эта строка в основном настраивает регистраторы.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные вашей базы данных (Base.metadata)
target_metadata = Base.metadata

# Другие значения из конфигурации, определенные по требованиям env.py,
# могут быть получены:
# my_important_option = config.get_main_option("my_important_option")
# ... и т.д.


def run_migrations_offline() -> None:
    """Выполнение миграций в режиме 'offline'.

    Это настраивает контекст только с URL,
    и не с движком, хотя здесь также допустим
    движок. Пропуская создание движка
    нам даже не нужен DBAPI.

    Вызовы context.execute() здесь отправляют заданную строку
    в вывод скрипта.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Выполнение миграций в режиме 'online'.

    В этом сценарии нам нужно создать движок
    и связать соединение с контекстом.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
