from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, \
    ElementNotInteractableException
import json
from selenium.webdriver.common.by import By

class ContactInformation:
    def __init__(self):
        self.data = {
            'first name': None,
            'last name': None,
            'email address': None
        }

    def set_field_value(self, field, value):
        if field in self.data:
            self.data[field] = value
        else:
            raise ValueError(f"Недопустимое поле: {field}")

    def get_data(self):
        return self.data


class Data:
    """
    Класс для работы с данными.
    """

    def __init__(self, filename):
        """
        Инициализация экземпляра класса Data.

        Аргументы:
        - filename: путь к файлу с данными.
        """
        self.filename = filename
        self.contact_info = None

    def write_data(self, data):
        """
        Запись данных в файл.

        Аргументы:
        - data: словарь данных для записи.
        """
        try:
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)
            print("Данные успешно записаны в файл.")
        except IOError as e:
            print(f"Ошибка при записи данных в файл: {str(e)}")

    def read_data(self):
        """
        Чтение данных из JSON файла.

        Возвращает данные из файла.
        """
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
            return data
        except IOError as e:
            print(f"Ошибка при чтении данных из файла: {str(e)}")
            return None

    def fill_contact_information(self):
        self.contact_info = ContactInformation()

        for field in self.contact_info.data.keys():
            value = input(f"Введите ваше {field}: ")
            self.contact_info.set_field_value(field, value)

    def get_contact_info(self):
        return self.contact_info.data


class Registration:
    """
    Класс для заполнения формы регистрации пользователя.
    """

    def __init__(self, driver):
        """
        Инициализация экземпляра класса RegistrationForm.

        Аргументы:
        - driver: экземпляр веб-браузера Selenium.
        """
        self.driver = driver

    def find_element(self, by, value):
        """
        Находит элемент на странице.

        Аргументы:
        - by: метод поиска элемента (например, By.ID, By.XPATH и т.д.).
        - value: значение для поиска элемента.

        Возвращает найденный элемент или None, если элемент не найден.
        """
        try:
            element = self.driver.find_element(by, value)
            return element
        except NoSuchElementException:
            print(f"Элемент не найден: {by}, {value}")
            return None

    def fill_text_field(self, field_id, value):
        """
        Заполняет текстовое поле значением.

        Аргументы:
        - field_id: идентификатор поля ввода.
        - value: значение для ввода в поле.
        """
        try:
            field = self.find_element(By.ID, field_id)
            if field:
                field.clear()
                field.send_keys(value)
        except (ElementNotVisibleException, ElementNotInteractableException) as e:
            print(f"Ошибка при заполнении текстового поля {field_id}: {str(e)}")

    def select_option(self, dropdown_id, option_text):
        """
        Выбирает значение из выпадающего списка.

        Аргументы:
        - dropdown_id: идентификатор выпадающего списка.
        - option_text: текст значения, которое нужно выбрать.
        """
        try:
            dropdown = self.find_element(By.ID, dropdown_id)
            if dropdown:
                dropdown.click()
                option = self.find_element(By.XPATH, f'//option[text()="{option_text}"]')
                if option:
                    option.click()
        except (ElementNotVisibleException, ElementNotInteractableException) as e:
            print(f"Ошибка при выборе опции {option_text} из выпадающего списка {dropdown_id}: {str(e)}")

    def check_checkbox(self, checkbox_id):
        """
        Выбирает чекбокс.

        Аргументы:
        - checkbox_id: идентификатор чекбокса.
        """
        try:
            checkbox = self.find_element(By.ID, checkbox_id)
            if checkbox:
                checkbox.click()
        except (ElementNotVisibleException, ElementNotInteractableException) as e:
            print(f"Ошибка при выборе чекбокса {checkbox_id}: {str(e)}")

    def submit_form(self, submit_id):
        """
        Отправляет форму.

        Аргументы:
        - submit_id: идентификатор кнопки отправки формы.
        """
        try:
            submit_button = self.find_element(By.ID, submit_id)
            if submit_button:
                submit_button.click()
        except (ElementNotVisibleException, ElementNotInteractableException) as e:
            print(f"Ошибка при отправке формы с помощью кнопки {submit_id}: {str(e)}")


class Menu:
    def __init__(self):
        """
        Инициализирует объект класса Menu.

        Аргументы:

        """
        self.filename = None
        self.data = None

    @staticmethod
    def print_menu_options(options):
        """
        Выводит на экран список опций меню.

        Аргументы:
        - options (dict): Словарь с опциями меню, где ключ - код опции, значение - кортеж с описанием опции.
        """
        try:
            for key, value in options.items():
                print(f"{key}. {value[0]}")
        except AttributeError:
            print("Неверный формат опций. Невозможно отобразить список опций меню.")

    def run(self):
        print("""                       ********** Привет, пользователь! **********
                      Эта программа предназначена для ???
                      """)
        while True:

            action_options = {
                "1": ("Создать новый файл - заполнить необходимые поля", self.create_file),
                "2": ("Показать данные из файла", self.show_data),
                "3": ("Изменить данные в файле", self.change_data),
                "4": ("Заполнить и отправить форму регистрации", self.fill_registration_form),
                "0": ("Выход", self.exit_program)
            }
            while True:
                self.print_menu_options(action_options)
                action_choice = input("Введите ваш выбор: ")

                if action_choice in action_options:
                    action_options[action_choice][1]()
                    input("Для продолжения нажмите Enter: ")
                    print()
                    break
                else:
                    print("Неверный выбор. Пожалуйста, попробуйте снова.")

    def create_file(self):
        while True:
            filename = input("Введите путь и имя файла: ")
            if filename.strip() == "":
                print("Пустое имя файла. Пожалуйста, введите действительное имя.")
            else:
                break

        if not filename.endswith(".json"):
            filename += ".json"

        self.data = Data(filename)
        self.data.fill_contact_information()
        data = self.data.get_contact_info()

        if data:
            self.data.write_data(data)
            print("Файл успешно создан и данные сохранены.")
        else:
            print("Нет данных для записи.")

    def load_existing_file(self):
        try:
            self.filename = input("Введите путь и имя файла без расширения: ")
            self.data = Data(self.filename)
            data = self.data.read_data()
            if data:
                print("Данные успешно загружены из файла.")
                self.data.contact_info.data = data
                return data
            else:
                print("Файл не содержит данных.")
                return None
        except IOError as e:
            print(f"Ошибка при чтении данных из файла: {str(e)}")
            return None

    def show_data(self):
        try:
            if self.filename is None:
                filename_without_extension = input("Введите путь и имя файла без расширения: ")
                self.filename = f"{filename_without_extension}.json"
            data = Data(self.filename).read_data()
            if data:
                print("Данные из файла:")
                for key, value in data.items():
                    print(f"{key}: {value}")
                print()
            else:
                print("В файле нет данных.")
        except IOError as e:
            print(f"Ошибка при чтении данных из файла: {str(e)}")

    def change_data(self):
        if self.filename is None:
            filename_without_extension = input("Введите путь и имя файла без расширения: ")
            self.filename = f"{filename_without_extension}.json"

        self.data = Data(self.filename)
        data = self.data.read_data()

        if data:
            print("Данные из файла:")
            for i, (key, value) in enumerate(data.items(), 1):
                print(f"{i}. {key}: {value}")
            key_number = int(input("Введите номер ключа, который нужно изменить: "))
            key_to_change = list(data.keys())[key_number - 1]

            if key_to_change in data:
                new_value = input("Введите новое значение: ")
                data[key_to_change] = new_value
                self.data.write_data(data)
            else:
                print("Неверный ключ.")
        else:
            print("В файле нет данных.")

    @staticmethod
    def get_website_address():
        website_address = input("Введите адрес веб-сайта: ")
        return website_address

    def fill_registration_form(self):
        website_address = self.get_website_address()

        driver = webdriver.Safari()

        if self.filename is None:
            self.filename = self.load_existing_file()

        if self.data is None or self.data.contact_info is None:
            print("Данные не найдены. Пожалуйста, создайте новый файл или загрузите существующие данные.")
            driver.quit()
            return

        form_data = self.data.get_contact_info()

        registration = Registration(driver)
        for field, value in form_data.items():
            registration.fill_text_field(field, value)

        driver.get(website_address)

        driver.quit()

    @staticmethod
    def exit_program():
        """
        Выходит из программы.
        """
        print("До свидания!")
        return


def main():
    menu = Menu()
    menu.run()


if __name__ == "__main__":
    main()
