# website_page_templates/flsite.py


import traceback
from typing import List, Dict, Union, Tuple
from flask import Flask, render_template, url_for, request, flash, redirect, session, abort, Response
from config import VALID_USERNAME, VALID_PASSWORD
from logger import logger

# Это укажет Flask где искать статику.
import os
os.environ["FLASK_STATIC"] = "./static"

# Инициализация Flask-приложения
app: Flask = Flask(__name__)

# Указываем Flask использовать папку 'static' для статических файлов (CSS, изображения и т. д.).
app.static_folder = 'static'

# Загружаем конфигурацию из файла 'config.py' для управления настройками приложения.
app.config.from_pyfile('config.py')

# Меню для использования в шаблонах
menu: List[Dict[str, Union[str, str]]] = [
    {"name": "Установка", "url": "install-flask"},
    {"name": "Первое приложение", "url": "first-app"},
    {"name": "Обратная связь", "url": "contact"}]


# Определение маршрутов для приложения

# Маршрут для главной страницы
# Оба эти маршрута связаны с одной и той же функцией-обработчиком и обрабатывают запросы к главной странице приложения.
@app.route("/")
@app.route("/index")
def index() -> str:
    """
    Обработчик маршрута для главной страницы.

    Returns:
        str: HTML-страница с использованием шаблона "index.html",
             в которую передается переменная меню (menu).
    """
    # Выводим в консоль URL для страницы "index", сгенерированный с использованием функции url_for.
    # Это полезно для отладки и отслеживания, какие URL создаются в приложении.
    print(f"URL for page 'index': {url_for('index')}")

    # Возвращаем HTML-страницу, сгенерированную из шаблона "index.html",
    # и передаем в шаблон переменную меню (menu), которая будет использоваться для построения меню на странице.
    return render_template("index.html", menu=menu)


# Маршрут для страницы "О сайте"
@app.route("/about")
def about() -> str:
    """
    Обработчик маршрута для страницы "О сайте".

    Returns:
        str: HTML-страница с использованием шаблона "about.html",
             в которую передаются переменные меню (menu) и заголовок (title).
    """
    # Выводим в консоль URL для страницы "about", сгенерированный с использованием функции url_for.
    # Это полезно для отладки и отслеживания, какие URL создаются в приложении.
    print(f"URL for page 'About': {url_for('about')}")

    # Возвращаем HTML-страницу, сгенерированную из шаблона "about.html".
    # Передаем в шаблон переменные menu (для построения меню) и title (заголовок страницы).
    return render_template("about.html", menu=menu, title="О сайте")


# Устанавливаем маршрут для страницы "Обратная связь" с поддержкой методов POST и GET.
@app.route("/contact", methods=["POST", "GET"])
def contact() -> str:
    """
    Обработчик маршрута для страницы "Обратная связь".

    Returns:
        str: HTML-страница "contact.html", в которую передаются переменные
        menu (для построения меню) и title (заголовок страницы).
    """
    # Если запрос осуществлен методом POST (отправка формы)
    if request.method == "POST":
        # Выводим данные из формы, полученные через request.form, в консоль для отладки.
        print(request.form)

        # Проверяем длину введенного имени пользователя из формы.
        if len(request.form['username']) > 2:
            # Если имя пользователя достаточно длинное, выводим сообщение об успешной отправке с использованием flash.
            flash("Сообщение отправлено!", category='success')
        else:
            # В противном случае выводим сообщение об ошибке с использованием flash.
            flash("Ошибка отправки сообщения!", category='error')

    # Возвращаем HTML-страницу "contact.html", передавая в шаблон переменные
    # menu (для построения меню) и title (заголовок страницы).
    return render_template('contact.html', menu=menu, title="Обратная связь")


# Устанавливаем маршрут для страницы "Авторизация" с поддержкой методов POST и GET.
@app.route("/login", methods=["POST", "GET"])
def login() -> Union[str, Response]:
    """
    Обработчик маршрута для страницы "Авторизация".

    Returns:
        str: HTML-страница "login.html", в которую передаются переменные menu (для построения меню) и title (заголовок страницы).
    """
    # Проверяем, авторизован ли пользователь (наличие ключа 'user_logged_in' в сессии).
    if 'user_logged_in' in session:
        # Если пользователь уже авторизован, перенаправляем его на страницу профиля.
        return redirect(url_for('profile', username=session['user_logged_in']))

    # Проверяем, был ли запрос методом POST и совпадают ли введенные данные с ожидаемыми.
    elif (request.method == 'POST' and
          request.form.get('username') == VALID_USERNAME and
          request.form.get('password') == VALID_PASSWORD):
        # Проверяем, был ли запрос методом POST и совпадают ли введенные данные с ожидаемыми.
        session['user_logged_in'] = request.form['username']
        # Если условия выполнены, сохраняем имя пользователя в сессии.
        return redirect(url_for('profile', username=session['user_logged_in']))
        # Перенаправляем пользователя на страницу профиля.

    # Если пользователь не авторизован и не был отправлен корректный запрос POST,
    # отображаем страницу авторизации.
    return render_template('login.html', menu=menu, title="Авторизация")


# Маршрут для отображения профиля пользователя
@app.route("/profile/<username>")  # или если нужно весь путь после - /profile/ тогда пишем "/profile/<patch:username>"
def profile(username: str) -> str:
    """
    Обработчик маршрута для страницы профиля пользователя.

    Parameters:
        username (str): Имя пользователя из URL.

    Returns:
        str: HTML-страница "profile.html" с информацией о пользователе, если он авторизован.
            В случае отсутствия авторизации, возвращает ошибку 401.
    """
    # В случае отсутствия авторизации, возвращает ошибку 401.
    if "user_logged_in" not in session or session["user_logged_in"] != username:
        abort(401)
    # Возвращает HTML-страницу с информацией о пользователе.
    return f"Профиль пользователя: {username}"


# Обработчик ошибки 404 (страница не найдена)
@app.errorhandler(404)
def page_not_found(error) -> Tuple[str, int]:
    """
       Обработчик ошибки 404 (страница не найдена).

       Parameters:
           error: Объект ошибки (может быть использован для получения дополнительной информации).

       Returns:
           Tuple[str, int]: HTML-страница "page404.html" с информацией об ошибке и код 404.
       """
    # Здесь можно использовать переменную error для получения дополнительной информации,
    # хотя в вашем случае это не обязательно.
    return render_template('page404.html', menu=menu, title="Страница не найдена"), 404


# Запуск приложения в режиме отладки на указанном хосте и порту
if __name__ == "__main__":
    try:
        app.run(debug=True, host='0.0.0.0', port=3333)
    except KeyboardInterrupt:
        logger.info("Приложение прервано пользователем")
    except Exception as error:
        # Обработка неожиданных ошибок с использованием логирования
        detailed_send_message_error = traceback.format_exc()
        logger.exception(f"Неожиданная ошибка в приложении: {error}\n{detailed_send_message_error}")
