# beautifulsoup_methods/single_page_scraper.py

import re
import traceback

from bs4 import BeautifulSoup as bs

from logger_config import logger


def main() -> None:
    try:
        logger.info("Начало процесса веб-скрапинга")

        # Открываем HTML файл и читаем его содержимое
        with open("assets/index.html", "r", encoding="utf-8") as file:
            # Создаем объект BeautifulSoup для парсинга HTML, используя парсер lxml
            soup = bs(file.read(), features="lxml")

            print("### Метод title - извлекает содержимое тега <title> ###\n")
            ############################################################################################################
            # Извлекаем содержимое тега <title> и выводим его текстовое содержимое
            title = soup.title.text
            print(title)  # Вывод: Главная страница блога

            # Еще один способ извлечения содержимого тега <title> с использованием свойства string
            title = soup.title.string
            print(title)  # Вывод: Главная страница блога
            ############################################################################################################

            print("\n### Методы .find() и .find_all() ###\n")
            ############################################################################################################
            print("\n.find() - извлекает информацию из первого попавшегося элемента")
            # Метод .find() для извлечения текста первого тега <h1>
            page_h1 = soup.find("h1").text
            print(page_h1)

            print("\n.find_all() - извлекает все элементы, подходящие под условие, и сохраняет их в список")
            # Метод .find_all() для извлечения всех тегов <h1>
            page_all_h1 = soup.find_all("h1")
            for h1 in page_all_h1:
                print(h1.string)

            print("\n.find() - извлечение информации из элемента по классу")
            # Метод .find() для извлечения текста span внутри div с классом user__name
            user_name = soup.find("div", class_="user__name").find("span").text.strip()
            print(user_name)

            # Или другой способ, используя словарь для атрибутов
            print("\n.find() - извлечение информации из элемента по классу, используя словарь атрибутов")
            user_name = soup.find("div", {"class": "user__name"}).find("span").text.strip()
            print(user_name)

            # Извлечение всех span внутри div с классом user__info
            print("\n.find_all() - извлечение всех span внутри div с классом user__info")
            find_all_spans_in_user_info = soup.find("div", class_="user__info").find_all("span")
            for span in find_all_spans_in_user_info:
                print(span.text.strip())

            print("\nПолучаем ссылки - извлечение всех ссылок (a) внутри div с классом social__networks")
            # Извлечение всех ссылок внутри div с классом social__networks
            social_links = soup.find("div", {"class": "social__networks"}).find("ul").find_all("a")
            for link in social_links:
                link_text = link.text.strip()
                link_url = link.get("href")  # или link["href"]
                print(f"{link_text}: {link_url}")
            ############################################################################################################

            print("\n### Методы .find_parent() и .find_parents() ###\n")
            ############################################################################################################
            print("\n.find_parent() - извлечение первого родительского элемента")
            # Метод .find_parent() для извлечения первого родительского элемента
            post_div = soup.find("div", {"class": "post__text"}).find_parent()
            print(post_div)

            print("\n.find_parent() - извлечение первого родительского элемента по классу")
            # Метод .find_parent() с указанием класса родительского элемента
            post_div = soup.find("div", {"class": "post__text"}).find_parent("div", "user__post")
            print(post_div)

            print("\n.find_parents() - извлечение всех родительских элементов")
            # Метод .find_parents() для извлечения всех родительских элементов
            post_divs = soup.find("div", {"class": "post__text"}).find_parents()
            print(post_divs)

            print("\n.find_parents() - извлечение всех родительских элементов по классу")
            # Метод .find_parents() с указанием класса родительских элементов
            post_divs = soup.find("div", {"class": "post__text"}).find_parents("div", "user__post")
            print(post_divs)
            ############################################################################################################

            print("\n### Методы .next_element, .find_next и .previous_element ###\n")
            ############################################################################################################
            print("\n.next_element - извлечение следующего элемента")
            # Метод .next_element для извлечения следующего элемента
            next_el = soup.find("div", {"class": "post__title"}).next_element.next_element.text.strip()
            print(next_el)

            print("\n.find_next - извлечение следующего элемента с использованием .find_next()")
            # Метод .find_next() для извлечения следующего элемента
            next_el = soup.find("div", {"class": "post__title"}).find_next().text.strip()
            print(next_el)
            ############################################################################################################

            print("\n### Методы .find_next_sibling() и .find_previous_sibling() ###\n")
            ############################################################################################################
            print("\n.find_next_sibling() - извлечение следующего элемента на том же уровне")
            # Метод .find_next_sibling() для извлечения следующего элемента на том же уровне
            next_sib = soup.find("div", {"class": "post__title"}).find_next_sibling()
            print(next_sib)
            ############################################################################################################

            print("\n### Поиск элементов по тексту с использованием регулярных выражений ###\n")
            ############################################################################################################
            print("\nПоиск элемента h3 по регулярному выражению")
            # Поиск элемента h3 по регулярному выражению
            find_by_text = soup.find("h3", string=re.compile("будет")).text.strip()
            print(find_by_text)

            print("\nПоиск элемента div по регулярному выражению")
            # Поиск элемента div по регулярному выражению
            find_by_text = soup.find("div", string=re.compile("ipsum")).text.strip()
            print(find_by_text)

            print("\nПоиск всех элементов div по регулярному выражению")
            # Поиск всех элементов div по регулярному выражению
            find_by_text = soup.find_all("div", string=re.compile("([Uu]t)"))
            print(find_by_text)
            ############################################################################################################

    except Exception as e:
        detailed_error = traceback.format_exc()
        logger.error(f"Error occurred: {str(e)}\n{detailed_error}")
    finally:
        logger.info("Процесс веб-скрапинга завершен")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Приложение прервано пользователем")
    except Exception as error:
        detailed_error = traceback.format_exc()
        logger.error(f"Unexpected application error: {error}\n{detailed_error}")
