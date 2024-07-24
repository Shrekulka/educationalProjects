# Instagram_scraper_instaloader/profile.py

import asyncio
import random
import traceback
from typing import List, Dict, Any

from instaloader import Profile, Instaloader

from config import InstagramProfileSettings, config, SEMAPHORE
from logger_config import logger


async def get_profile_data(username: str) -> Dict[str, Any]:
    """
    Асинхронно получает расширенные данные профиля для одного пользователя Instagram.
    Args:
        username: Имя пользователя Instagram для получения данных профиля.
    Returns:
        Словарь с данными профиля.
    """
    # Используем семафор для ограничения количества одновременных запросов
    async with SEMAPHORE:
        try:
            # Инициализируем Instaloader для работы с Instagram API
            L = Instaloader()
        except Exception as e:
            logger.error(f"Ошибка при инициализации Instaloader: {str(e)}\n{traceback.format_exc()}")
            return {}

        try:
            # Получаем объект профиля Instagram по имени пользователя
            profile = Profile.from_username(L.context, username)
        except Exception as e:
            logger.error(f"Ошибка при получении профиля {username}: {str(e)}\n{traceback.format_exc()}")
            return {}

        try:
            # Получаем данные о последнем посте профиля
            posts = profile.get_posts()

            # Получаем первый пост из генератора
            last_post = next(posts, None)

            # Количество лайков последнего поста
            last_post_likes = last_post.likes if last_post else None

            # Количество комментариев последнего поста
            last_post_comments = last_post.comments if last_post else None

            # URL последнего поста
            last_post_url = last_post.url if last_post else None

            # Метка времени последнего поста
            last_post_timestamp = last_post.date_utc.timestamp() if last_post else None

            # Создаем объект настроек профиля с полученными данными
            profile_settings = InstagramProfileSettings(
                username=profile.username,
                user_id=profile.userid,
                full_name=profile.full_name,
                biography=profile.biography,
                private=profile.is_private,
                verified=profile.is_verified,
                is_business_account=profile.is_business_account,
                business_category_name=getattr(profile, 'business_category_name', None),
                category_name=getattr(profile, 'category_name', None),
                posts_count=profile.mediacount,
                followers=profile.followers,
                following=profile.followees,
                profile_pic_url=profile.profile_pic_url,
                external_url=profile.external_url,
                has_highlight_reels=profile.has_highlight_reels,
                last_post_likes=last_post_likes,
                last_post_comments=last_post_comments,
                last_post_url=last_post_url,
                last_post_timestamp=last_post_timestamp,
                igtv_count=profile.igtvcount
            )

            # Возвращаем данные профиля в виде словаря
            return profile_settings.dict()

        except Exception as e:
            logger.error(f"Ошибка при получении данных профиля {username}: {str(e)}\n{traceback.format_exc()}")
            return {}


async def get_all_profile_data(usernames: List[str]) -> List[Dict[str, Any]]:
    """
    Асинхронно получает данные профилей для списка пользователей Instagram.
    Args:
        usernames: Список имен пользователей Instagram для получения данных профилей.
    Returns:
        Список словарей с данными профилей.
    """
    profile_data_list = []  # Инициализируем список для хранения данных профилей

    for username in usernames:
        # Получаем данные профиля для каждого имени пользователя
        profile_data = await get_profile_data(username)

        # Добавляем данные профиля в список
        profile_data_list.append(profile_data)

        # Определяем случайную задержку перед следующим запросом
        delay = random.uniform(config.min_delay, config.max_delay)

        logger.info(f"Задержка перед следующим запросом: {delay:.2f} секунд")

        # Выполняем асинхронную задержку
        await asyncio.sleep(delay)

    return profile_data_list  # Возвращаем список данных профилей
