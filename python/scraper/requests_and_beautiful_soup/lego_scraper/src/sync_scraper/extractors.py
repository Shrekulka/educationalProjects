# lego_scraper/src/sync_scraper/extractors.py

from typing import List, Dict, Tuple, Optional

from bs4 import BeautifulSoup as bs

from config.settings import config
from utils.logger_config import logger


def get_themes(themes_page_soup: bs) -> List[Dict[str, str]]:
    """
    Извлекает список тем с их названиями, описаниями и URL-адресами с страницы с темами.

    Args:
        themes_page_soup (bs): Объект BeautifulSoup, содержащий HTML-код страницы с темами.

    Returns:
        List[Dict[str, str]]: Список словарей, где каждый словарь содержит информацию о теме:
            - 'title': название темы,
            - 'description': описание темы,
            - 'url': URL темы.
    """
    # Находим раздел с темами на странице и его список
    themes_section = themes_page_soup.find("section").ul

    # Извлекаем все элементы тем (li)
    theme_items = themes_section.find_all("li")

    # Получаем общее количество тем и записываем в лог
    total_themes = len(theme_items)
    logger.info(f"Найдено: {total_themes} тем!")

    # Инициализируем список для хранения данных о темах
    themes = []

    # Инициализируем индекс темы
    theme_index = 0

    # Перебираем каждый элемент темы
    for theme_item in theme_items:
        # Увеличиваем индекс темы
        theme_index += 1

        # Извлекаем название темы
        title = theme_item.h2.span.text

        # Извлекаем описание темы
        description = theme_item.find("span", class_="CategoryLeafstyles__DescriptionAlternate-is33yg-13").text

        # Формируем URL темы
        url = config.BASE_URL + theme_item.a.get('href')

        # Записываем информацию о теме в лог
        logger.info(f"\nТема №{theme_index}:\nНазвание: '{title}'\nОписание: {description}\nurl: {url}")

        # Формируем словарь с данными о теме
        theme = {
            'title': title,
            'description': description,
            'url': url,
        }

        # Добавляем словарь в список тем
        themes.append(theme)

    # Возвращаем список тем
    return themes


def get_toys_page(theme_page_soup: bs) -> Tuple[int, int]:
    """
    Извлекает общее количество игрушек и количество страниц с игрушками из HTML-кода страницы темы.

    Args:
        theme_page_soup (bs): Объект BeautifulSoup, содержащий HTML-код страницы темы.

    Returns:
        Tuple[int, int]: Кортеж, содержащий два значения:
            - Общее количество игрушек (int),
            - Общее количество страниц (int).
    """
    try:
        # Извлечение количества игрушек из элемента span с атрибутом data-value
        total_toys = int(theme_page_soup.select("span[data-value]")[0].get("data-value"))

        # Расчет количества страниц (округление вверх)
        # Делим общее количество игрушек на количество игрушек на странице (18), округляем вверх
        total_pages = (total_toys + 17) // 18

    except (IndexError, ValueError):
        # Если возникла ошибка при извлечении данных, устанавливаем количество игрушек и страниц в 0 при ошибке
        logger.warning("Не удалось получить количество игрушек.")
        total_toys = 0
        total_pages = 0

    # Возвращаем общее количество игрушек и количество страниц
    return total_toys, total_pages


def get_toy_info(toy_attributes: List[str]) -> Dict[str, Optional[str]]:
    """
    Извлекает информацию о возрасте, количестве деталей и рейтинге игрушек из списка атрибутов.

    Args:
        toy_attributes (List[str]): Список строк, представляющих атрибуты игрушки.

    Returns:
        Dict[str, Optional[str]]: Словарь, содержащий информацию об игрушке:
            - 'age' (Optional[str]): Возрастная категория (если имеется).
            - 'pieces' (Optional[str]): Количество деталей (если имеется).
            - 'rating' (Optional[str]): Рейтинг (если имеется).
    """
    # Инициализация словаря с атрибутами игрушки, изначально все значения равны None
    toy_data = {
        'age': None,
        'pieces': None,
        'rating': None
    }

    # Перебор всех атрибутов игрушки
    for attr in toy_attributes:
        # Проверка, содержит ли атрибут символ '+', что указывает на возраст
        if '+' in attr:
            toy_data['age'] = attr
        # Проверка, содержит ли атрибут символ '.', что указывает на рейтинг
        elif '.' in attr:
            toy_data['rating'] = attr
        # Если атрибут не содержит ни '+' ни '.', предполагаем, что это количество деталей
        else:
            toy_data['pieces'] = attr

    # Возвращаем словарь с извлеченной информацией об игрушке
    return toy_data


def get_price(toy_element: bs) -> Tuple[Optional[str], Optional[str]]:
    """
    Извлекает цену и скидку из HTML-элемента игрушки.

    Args:
        toy_element (bs): HTML-элемент, представляющий игрушку, с информацией о цене.

    Returns:
        Tuple[Optional[str], Optional[str]]: Кортеж, содержащий цену и скидку:
            - price (Optional[str]): Цена игрушки, если она найдена.
            - discount (Optional[str]): Скидка на игрушку, если она найдена.
    """
    # Инициализация переменных для хранения цены и скидки
    price = None
    discount = None

    # Поиск div элемента, содержащего информацию о цене
    price_tag = toy_element.find("div", {"data-test": "product-leaf-price-row"})

    if price_tag:
        # Поиск элемента span с ценой
        price_span = price_tag.find("span", {"data-test": "product-leaf-price"})
        if price_span:
            # Извлечение текста из span и удаление лишних пробелов
            price = price_span.text.strip()

        # Поиск элемента span со скидкой
        discount_span = price_tag.find("span", {"data-test": "product-leaf-discounted-price"})
        if discount_span:
            # Извлечение текста из span и удаление лишних пробелов
            discount = discount_span.text.strip()

    # Возвращение кортежа с ценой и скидкой
    return price, discount


def get_availability(toy_element: bs) -> Optional[str]:
    """
    Извлекает информацию о доступности товара из HTML-элемента игрушки.

    Args:
        toy_element (bs): HTML-элемент, представляющий игрушку, с информацией о доступности.

    Returns:
        Optional[str]: Строка, содержащая информацию о доступности игрушки:
            - "Add to Bag" если кнопка "Добавить в корзину" присутствует,
            - "Out of Stock" если ссылка "Нет в наличии" присутствует,
            - "Coming Soon" если ссылка "Скоро в продаже" присутствует,
            - `None`, если ни одна из этих опций не найдена.
    """
    # Поиск кнопки "Add to Bag" (Добавить в корзину) или "Pre-order" (Предзаказ)
    add_to_bag_button = toy_element.find("button", {"data-test": "add-to-cart-skroll-cta"})
    if add_to_bag_button:
        # Если кнопка найдена, возвращаем текст, очищенный от пробелов
        return add_to_bag_button.span.text.strip()

    # Поиск ссылки "Out of Stock" (Нет в наличии)
    out_of_stock_link = toy_element.find("a", {"data-test": "product-leaf-cta-out-of-stock"})
    if out_of_stock_link:
        # Если ссылка найдена, возвращаем текст, очищенный от пробелов
        return out_of_stock_link.text.strip()

    # Поиск ссылки "Coming Soon" (Скоро в продаже)
    coming_soon_link = toy_element.find("a", {"data-test": "product-leaf-cta-coming-soon"})
    if coming_soon_link:
        # Если ссылка найдена, возвращаем текст, очищенный от пробелов
        return coming_soon_link.text.strip()

    # Если ни один из указанных элементов не найден, возвращаем None
    return None


def get_toys_data(toy_page_soup: bs, theme_name: str = "Marvel") -> List[Dict[str, Optional[str]]]:
    """
    Извлекает данные об игрушках из HTML-страницы.

    Эта функция анализирует HTML-страницу, находит все элементы, соответствующие игрушкам,
    и извлекает из них информацию, такую как название, возраст, количество деталей,
    рейтинг, цена, скидка и доступность.

    Args:
        toy_page_soup (BeautifulSoup): Объект BeautifulSoup, представляющий HTML-страницу с игрушками.
        theme_name (str, optional): Название темы (коллекции) игрушек. По умолчанию "Marvel".

    Returns:
        List[Dict[str, Optional[str]]]: Список словарей, каждый из которых содержит информацию об одной игрушке.
        Если игрушки не найдены, возвращается пустой список.

    Raises:
        Exception: Любые исключения, возникшие при обработке отдельной игрушки,
                   логируются, но не прерывают обработку остальных игрушек.
    """
    # Находим все элементы списка, соответствующие игрушкам
    toys = toy_page_soup.find_all("li", {"data-test": "product-item"})

    # Создаем пустой список для хранения данных об игрушках
    toy_data = []

    # Проходим по всем найденным игрушкам на странице
    for toy in toys:
        # Проверка, является ли элемент рекламным блоком
        if {"Grid_grid-item__FLJlN", "Grid_grid-disruptor__ilL_6"}.issubset(toy.get('class', [])):
            # Если это рекламный блок, ищем заголовок рекламного блока
            disruptor_title = toy.find('h3', {'data-test': 'disruptor-static-title'})
            # Если заголовок найден, логируем его
            if disruptor_title:
                logger.info(f"Рекламный блок пропущен: {disruptor_title.text}")
            # Если заголовок не найден, логируем его
            else:
                logger.info("Рекламный блок пропущен, но заголовок не найден.")
            # Переходим к следующему элементу, пропуская текущий рекламный блок
            continue

        try:
            # Находим тег h3 с названием игрушки
            toy_name_tag = toy.find("h3")
            # Если тег h3 не найден, пропускаем текущую игрушку
            if not toy_name_tag:
                continue

            # Извлекаем название игрушки и удаляем лишние пробелы
            toy_name: str = toy_name_tag.text.strip()

            # Поиск атрибутов игрушки (возраст, количество деталей, рейтинг)
            attributes_div = toy.find("div", {"data-test": "product-leaf-attributes-row"})

            # Если атрибуты найдены, извлекаем их из всех тегов span внутри attributes_div
            if attributes_div:
                toy_attributes = [i.text.strip() for i in attributes_div.find_all("span")]
                toy_value = get_toy_info(toy_attributes=toy_attributes)

            # Если атрибуты не найдены, задаем значения по умолчанию
            else:
                toy_value = {'age': None, 'pieces': None, 'rating': None}

            # Получение цены и скидки
            price, discount = get_price(toy_element=toy)

            # Получение информации о доступности
            availability = get_availability(toy)

            # Формирование словаря с информацией об игрушке
            toy_info = {
                'name': toy_name,
                'collection': theme_name,
                'age': toy_value['age'],
                'pieces': toy_value['pieces'],
                'rating': toy_value['rating'],
                'price': price,
                'discount': discount,
                'availability': availability
            }

            # Добавление информации об игрушке в общий список
            toy_data.append(toy_info)
            logger.info(f"Обработан товар: {toy_name}")

        except Exception as e:
            # Логирование ошибок при обработке отдельной игрушки
            logger.error(f"Ошибка при обработке игрушки: {toy}\nОшибка: {str(e)}")
            logger.debug(f"HTML элемента:\n{toy}")

    # Если данные об игрушках не найдены, возвращаем пустой список
    if not toy_data:
        logger.warning(f"Не найдено игрушек в коллекции {theme_name}")
        return []

    # Возвращаем список с данными об игрушках
    return toy_data
