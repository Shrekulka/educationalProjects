# app.py
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, url_for, request, abort
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urljoin
from models import User, Site, SiteStats, UserSite  # импорт моделей
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_hub.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


def replace_links(html_content, user_site_name):
    """
    Заменяет атрибуты href в HTML-коде на прокси-URL.

    Аргументы:
        html_content (str): HTML-код.
        user_site_name (str): Имя сайта пользователя.

    Возвращает:
        bs4.BeautifulSoup: Модифицированный объект BeautifulSoup.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    for a_tag in soup.find_all('a', href=True):
        original_url = a_tag.get('href')
        if original_url and not original_url.startswith(('http://', 'https://')):
            a_tag['href'] = f'/proxy/{user_site_name}/{original_url}'
    return soup

# Функция для проверки безопасности пользовательского ввода
def is_safe_user_input(user_input):
    # В данном примере просто проверяем, что ввод состоит только из букв и цифр
    return user_input.isalnum()
@app.route('/proxy/<user_site_name>/<path:routes_on_original_site>')
@login_required
def proxy_site(user_site_name, routes_on_original_site):
    # Проверка параметров на безопасность
    if not is_safe_user_input(user_site_name) or not is_safe_user_input(routes_on_original_site):
        abort(400)  # Возвращайте ошибку HTTP 400 в случае небезопасных параметров

    try:
        original_url = urljoin(f'http://{routes_on_original_site}', '')  # Передача URL через urljoin для безопасного объединения
        response = requests.get(original_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Помилка при отриманні вмісту оригінального сайту: {e}", 500

    modified_content = replace_links(response.text, user_site_name)
    return modified_content


# Основний роут для особистого кабінету
@app.route('/dashboard')
@login_required
def dashboard():
    try:
        user_sites = current_user.get_accessible_sites()

        if not user_sites:
            return render_template('no_sites.html')

        stats = {}
        for site in user_sites:
            site_stats = SiteStats.query_stats(site.id)
            stats[site.name] = {'views': site_stats.views, 'traffic': site_stats.traffic}

        return render_template('dashboard.html', stats=stats)

    except SQLAlchemyError as e:
        # Обработка ошибки базы данных, например, логирование или вывод сообщения пользователю
        app.logger.error(f"Database error: {e}")
        return render_template('error.html', error_message="Database error")


# Роут для додавання сайту в особистий кабінет
@app.route('/add_site', methods=['POST'])
@login_required
def add_site():
    site_name = request.form.get('site_name')
    site_url = request.form.get('site_url')

    # Тут ви можете зберегти інформацію про сайт в базі даних, пов'язану з користувачем
    # Наприклад, використовуючи модель Site і встановивши відповідний зв'язок між User та Site

    return redirect(url_for('dashboard'))


# Роут для редагування особистих даних користувача
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Оновіть дані користувача в базі даних
        current_user.username = request.form.get('new_username')
        # Опціонально, додайте інші поля користувача

        db.session.commit()

        return redirect(url_for('dashboard'))

    # Якщо метод GET, виведіть сторінку редагування профілю
    return render_template('edit_profile.html')


@app.route('/some_route')
def some_route():
    site = Site.query.filter_by(name='some_name').first()
    if site is None:
        abort(404)
    # продолжайте выполнение кода


# Новий роут для створення проксі-сайту
@app.route('/create_proxy', methods=['POST'])
@login_required
def create_proxy():
    user_site_name = request.form.get('user_site_name')
    original_url = request.form.get('original_url')

    # Зберігаємо проксі-сайт в базі даних
    proxy_site = ProxySite(user_site_name=user_site_name, original_url=original_url, user_id=current_user.id)
    db.session.add(proxy_site)
    db.session.commit()

    return jsonify({"success": True})


# Роут для створення сайту
@app.route('/create_site', methods=['POST'])
@login_required
def create_site():
    # Отримати дані форми для створення сайту
    site_name = request.form.get('site_name')
    site_url = request.form.get('site_url')

    # Створити сайт та призначити доступ користувачу
    new_site = Site(name=site_name, url=site_url, user_id=current_user.id)
    new_site.create()

    # Додати доступ до створеного сайту для користувача
    UserSite.add_access(current_user, new_site)

    return redirect(url_for('dashboard'))


# Роут для реєстрації
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # В методе register
        password_hash = generate_password_hash(password)
        new_user = User(username=username, password=password_hash)
        # сохранение new_user в базу данных

        # Тут ви можете зберегти інформацію про користувача в базі даних, наприклад, використовуючи модель User

        # Після реєстрації перенаправте користувача на вхід
        return redirect(url_for('login'))

    # Якщо метод GET, виведіть сторінку реєстрації
    return render_template('register.html')


# Роут для перегляду статистики сайту
@app.route('/site_stats/<site_name>')
@login_required
def site_stats(site_name):
    # Отримати інформацію про кількість переходів та об'єм даних для конкретного сайту
    site = Site.query.filter_by(name=site_name).first()
    if not site:
        return "Сайт не знайдено", 404

    site_stats = SiteStats.query_stats(site.id)

    return render_template('site_stats.html', site_name=site_name, views=site_stats.views, traffic=site_stats.traffic)


# Роут для входу
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Тут ви повинні перевірити, чи існує користувач з такими данними в базі даних
        # Якщо так, використовуйте flask-login для автентифікації користувача
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))

    # Якщо метод GET, виведіть сторінку входу
    return render_template('login.html')


# Ваш роут для вихіду
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.context_processor
def inject_user():
    return dict(current_user=current_user)


if __name__ == '__main__':
    app.run(debug=True)
