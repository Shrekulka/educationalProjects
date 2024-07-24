# Instagram_scraper_instaloader/log.py

from typing import Dict, Any

from logger_config import logger
from utils import format_timestamp


def log_profile_data(profile_data: Dict[str, Any]) -> None:
    """
    Логирует расширенные данные профиля.

    Args:
        profile_data: Словарь с данными профиля.
    """
    # Проверяем, если словарь с данными профиля пустой
    if not profile_data:
        logger.error("Профильные данные пусты.")
        return

    # Инициализируем переменную для форматированной метки времени последнего поста
    formatted_last_post_timestamp = None

    # Проверяем, есть ли в данных метка времени последнего поста и является ли она целым числом
    if profile_data.get('last_post_timestamp') and isinstance(profile_data['last_post_timestamp'], int):
        # Форматируем метку времени последнего поста в читаемый вид
        formatted_last_post_timestamp = format_timestamp(profile_data['last_post_timestamp'])

    # Логируем информацию о профиле, используя форматированный текст
    logger.info(f"Profile info:                  {profile_data.get('username')}\n"
                f"User ID:                       {profile_data.get('user_id')}\n"
                f"Full name:                     {profile_data.get('full_name')}\n"
                f"Biography:                     {profile_data.get('biography')}\n"
                f"Is private:                    {profile_data.get('private')}\n"
                f"Is verified:                   {profile_data.get('verified')}\n"
                f"Is business account:           {profile_data.get('is_business_account')}\n"
                f"Business category:             {profile_data.get('business_category_name')}\n"
                f"Category:                      {profile_data.get('category_name')}\n"
                f"Posts count:                   {profile_data.get('posts_count')}\n"
                f"Followers:                     {profile_data.get('followers')}\n"
                f"Following:                     {profile_data.get('following')}\n"
                f"Profile picture URL:           {profile_data.get('profile_pic_url')}\n"
                f"External URL:                  {profile_data.get('external_url')}\n"
                f"Has highlight reels:           {profile_data.get('has_highlight_reels')}\n"
                f"Last post likes:               {profile_data.get('last_post_likes')}\n"
                f"Last post comments:            {profile_data.get('last_post_comments')}\n"
                f"Last post URL:                 {profile_data.get('last_post_url')}\n"
                f"Formatted last post timestamp: {formatted_last_post_timestamp}\n"
                f"IGTV count:                    {profile_data.get('igtv_count')}")
