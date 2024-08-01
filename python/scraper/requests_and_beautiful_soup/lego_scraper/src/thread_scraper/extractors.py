# lego_scraper/src/thread_scraper/extractors.py

from typing import List, Dict, Tuple, Optional

from bs4 import BeautifulSoup as bs

from config.settings import config
from utils.logger_config import logger


def extract_themes(themes_page_soup: bs) -> List[Dict[str, str]]:
    """
    Извлекает список тем из HTML-кода страницы тем.

    Функция находит все темы на странице и извлекает для каждой темы её название, описание и URL.
    Затем формирует список словарей, где каждый словарь содержит информацию о теме.

    Args:
        themes_page_soup (bs): Объект BeautifulSoup, представляющий HTML-код страницы с темами.

    Returns:
        List[Dict[str, str]]: Список словарей, где каждый словарь содержит информацию о теме,
                              включающую название, описание и URL.
    """
    # Находим раздел с темами на странице
    themes_section = themes_page_soup.find("section").ul

    # Находим все элементы списка, представляющие темы
    theme_items = themes_section.find_all("li")

    # Создаем пустой список для хранения информации о темах
    theme_list = []

    # Проходим по всем элементам списка тем
    for index, theme_item in enumerate(theme_items, start=1):
        # Извлекаем название темы
        title = theme_item.h2.span.text

        # Извлекаем описание темы
        description = theme_item.find("span", class_="CategoryLeafstyles__DescriptionAlternate-is33yg-13").text

        # Формируем URL темы, добавляя относительный путь к базовому URL
        url = config.BASE_URL + theme_item.a.get('href')

        # Добавляем информацию о теме в список
        theme_list.append({
            'title': title,
            'description': description,
            'url': url,
        })
        logger.info(f"\nТема №{index}:\nНазвание: '{title}'\nОписание: {description}\nurl: {url}")

    # Возвращаем список всех тем
    return theme_list


def extract_toy_count_and_pages(theme_page_soup: bs) -> Tuple[int, int]:
    """
    Извлекает количество игрушек и количество страниц с игрушками из HTML-кода страницы темы.

    Функция ищет элемент, содержащий общее количество игрушек, и рассчитывает количество страниц
    на основе этого числа. Возвращает кортеж, содержащий количество игрушек и количество страниц.

    Args:
        theme_page_soup (bs): Объект BeautifulSoup, представляющий HTML-код страницы с темой.

    Returns:
        Tuple[int, int]: Кортеж из двух целых чисел:
                         1. Количество игрушек (int)
                         2. Количество страниц (int)
    """
    try:
        # Находим элемент, содержащий общее количество игрушек, и извлекаем значение атрибута data-value
        number_of_toys = int(theme_page_soup.select_one("span[data-value]").get("data-value"))

        # Рассчитываем количество страниц на основе общего числа игрушек
        # 18 игрушек на одной странице, округление вверх
        number_of_pages = (number_of_toys + 17) // 18

        # Возвращаем количество игрушек и количество страниц
        return number_of_toys, number_of_pages

    except (AttributeError, ValueError):
        # Если произошла ошибка (не найден элемент или неверное значение), записываем предупреждение в лог
        logger.warning("Не удалось получить количество игрушек.")

        # Возвращаем 0 игрушек и 0 страниц в случае ошибки
        return 0, 0


def extract_toy_info(toy_attributes: List[str]) -> Dict[str, Optional[str]]:
    """
    Извлекает информацию о toy (игрушке) из списка атрибутов и возвращает словарь с данными об игрушке.

    Функция принимает список строк, представляющих атрибуты игрушки, и классифицирует их по типам:
    возраст, количество деталей и рейтинг. Возвращает словарь, содержащий соответствующие значения
    для каждого типа атрибута. Если атрибут не найден, возвращает None.

    Args:
        toy_attributes (List[str]): Список строк, содержащих атрибуты игрушки.
                                    Например, ['3+', '200 pieces', '4.5'].

    Returns:
        Dict[str, Optional[str]]: Словарь с ключами 'age', 'pieces', 'rating', где значения могут быть строками
                                   или None, если соответствующий атрибут не найден.
    """
    # Инициализируем словарь для хранения данных об игрушке
    toy_data = {'age': None, 'pieces': None, 'rating': None}

    # Проходим по каждому атрибуту в списке
    for attr in toy_attributes:
        # Если атрибут содержит знак '+', предполагаем, что это возраст
        if '+' in attr:
            toy_data['age'] = attr
        # Если атрибут содержит точку, предполагаем, что это рейтинг
        elif '.' in attr:
            toy_data['rating'] = attr
        # Если атрибут не содержит ни '+' ни '.', предполагаем, что это количество деталей
        else:
            toy_data['pieces'] = attr

    # Возвращаем словарь с извлеченными данными
    return toy_data


def extract_price(toy_element: bs) -> Tuple[Optional[str], Optional[str]]:
    """
    Извлекает цену и скидку из HTML-элемента игрушки.

    Функция ищет элементы, содержащие цену и скидку, в предоставленном HTML-элементе игрушки.
    Если соответствующие элементы найдены, функция возвращает текст их содержимого (отформатированный и очищенный от пробелов).
    Если элемент не найден, возвращает `None` для соответствующего значения.

    Args:
        toy_element (bs): HTML-элемент, представляющий игрушку.

    Returns:
        Tuple[Optional[str], Optional[str]]: Кортеж, содержащий цену и скидку. Если цена или скидка не найдены, возвращается `None`.
    """
    # Ищем контейнер, который содержит цену и скидку
    price_tag = toy_element.find("div", {"data-test": "product-leaf-price-row"})

    if price_tag:
        # Ищем элемент с текстом цены
        price = price_tag.find("span", {"data-test": "product-leaf-price"})
        # Ищем элемент с текстом скидки
        discount = price_tag.find("span", {"data-test": "product-leaf-discounted-price"})

        # Возвращаем цену и скидку, очищенные от пробелов, если они найдены
        return (price.text.strip() if price else None,
                discount.text.strip() if discount else None)

    # Если контейнер с ценой и скидкой не найден, возвращаем (None, None)
    return None, None


def extract_availability(toy_element: bs) -> Optional[str]:
    """
    Извлекает информацию о доступности товара из HTML-элемента игрушки.

    Функция ищет различные элементы в предоставленном HTML-элементе игрушки, которые могут указывать на
    доступность товара, такие как кнопка "Add to Bag", ссылки "Out of stock" и "Coming Soon".
    Возвращает текст первого найденного элемента, который соответствует одному из указанных типов доступности,
    или `None`, если ни один из этих элементов не найден.

    Args:
        toy_element (bs): HTML-элемент, представляющий игрушку, из которого нужно извлечь информацию о доступности.

    Returns:
        Optional[str]: Строка, содержащая информацию о доступности товара (например, текст кнопки или ссылки),
                       или `None`, если информация о доступности не найдена.
    """
    # Поиск кнопки "Add to Bag" или "Pre-order" в HTML-элементе
    add_to_bag_button = toy_element.find("button", {"data-test": "add-to-cart-skroll-cta"})
    if add_to_bag_button:
        # Если кнопка найдена, возвращаем её текст, очищенный от пробелов
        return add_to_bag_button.span.text.strip()

    # Поиск ссылки "Out of stock"
    out_of_stock_link = toy_element.find("a", {"data-test": "product-leaf-cta-out-of-stock"})
    if out_of_stock_link:
        # Если ссылка найдена, возвращаем её текст, очищенный от пробелов
        return out_of_stock_link.text.strip()

    # Поиск ссылки "Coming Soon"
    coming_soon_link = toy_element.find("a", {"data-test": "product-leaf-cta-coming-soon"})
    if coming_soon_link:
        # Если ссылка найдена, возвращаем её текст, очищенный от пробелов
        return coming_soon_link.text.strip()

    # Если ни один из указанных элементов не найден, возвращаем None
    return None


def extract_toys_from_page(toy_page_soup: bs, theme_name: str) -> List[Dict[str, Optional[str]]]:
    """
    Извлекает информацию об игрушках со страницы, представленной объектом BeautifulSoup.

    Функция проходит по всем элементам списка игрушек на странице, игнорирует рекламные блоки,
    и извлекает информацию о каждой игрушке, включая название, возрастное ограничение, количество деталей,
    рейтинг, цену, скидку и доступность. Возвращает список словарей с данными об игрушках.

    Args:
        toy_page_soup (bs): HTML-элемент страницы с игрушками, представленный объектом BeautifulSoup.
        theme_name (str): Название темы, к которой относится текущая страница с игрушками.

    Returns:
        List[Dict[str, Optional[str]]]: Список словарей, где каждый словарь содержит информацию об одной игрушке.
    """
    # Находим все элементы списка игрушек на странице
    toys = toy_page_soup.find_all("li", {"data-test": "product-item"})

    # Инициализация пустого списка для хранения данных об игрушках
    toy_data = []

    # Проходим по всем найденным игрушкам на странице
    for toy in toys:
        # Проверка, является ли элемент рекламным блоком по наличию классов
        if {"Grid_grid-item__FLJlN", "Grid_grid-disruptor__ilL_6"}.issubset(toy.get('class', [])):
            # Находим заголовок рекламного блока. Используем метод find для поиска элемента <h3> с указанным атрибутом
            # data-test.
            disruptor_title = toy.find('h3', {'data-test': 'disruptor-static-title'})
            logger.info(f"Рекламный блок пропущен: {disruptor_title.text if disruptor_title else 'не найден'}")

            # Переходим к следующему элементу в цикле, пропуская текущий рекламный блок.
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

            # Извлекаем текст из всех элементов <span> внутри attributes_div, удаляя пробелы. Если attributes_div не
            # найден, используем пустой список.
            toy_attributes = [i.text.strip() for i in attributes_div.find_all("span")] if attributes_div else []

            # Извлекаем информацию об игрушке из атрибутов
            toy_value = extract_toy_info(toy_attributes)

            # Извлекаем цену и скидку
            price, discount = extract_price(toy)

            # Извлекаем информацию о доступности
            availability = extract_availability(toy)

            # Создаем словарь с данными об игрушке
            toy_info = {
                'name': toy_name,
                'collection': theme_name,
                'age': toy_value['age'],
                'pieces': toy_value['pieces'],
                'rating': toy_value['rating'],
                'price': price,
                'discount': discount,
                'availability': availability,
            }
            # Добавляем данные об игрушке в список
            toy_data.append(toy_info)
            logger.info(f"Обработан товар: {toy_name}")

        except Exception as e:
            logger.error(f"Ошибка при обработке игрушки: {toy}\nОшибка: {str(e)}")
            logger.debug(f"HTML элемента:\n{toy}")

    # Логируем предупреждение, если не найдено ни одной игрушки
    if not toy_data:
        logger.warning(f"Не найдено игрушек в коллекции {theme_name}")

    # Возвращаем список с данными об игрушках
    return toy_data
