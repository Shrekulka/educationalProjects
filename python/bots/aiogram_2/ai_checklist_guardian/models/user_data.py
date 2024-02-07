# ai_checklist_guardian/models/user_data.py

import sqlite3 as sq
import traceback


class UserData:
    """
       Class UserData provides a representation of user data for generating reports and interacting with a SQLite database.

       Methods:

       __init__(self, location=None, option=None, comment=None, photo_link=None, report=None):
           Initializes the UserData object with the specified attributes.

           Parameters:
           - location (str): The selected location of the user.
           - option (str): The selected checklist option.
           - comment (str): The user's comment.
           - photo_link (str): The link to the user's photo.
           - report (str): The user's report.

           generate_report(self) -> str:
           Forms the text of the report based on location, checklist option, comment, and photo link.
           Returns the generated report text.

           Attributes:
           - location (str): The selected location of the user.
           - option (str): The selected checklist option.
           - comment (str): The user's comment.
           - photo_link (str): The link to the user's photo.
           - report (str): The user's report.

           Attributes for database interaction:
           - db_base: SQLite database connection.
           - db_cursor: Cursor for interacting with the SQLite database.
       """
    # Инициализация объекта UserData с четырьмя атрибутами:
    def __init__(self, location=None, option=None, comment=None, photo_link=None, report=None):
        """
            Initialization of the UserData object.

            Parameters:
            - location (str): The selected location of the user.
            - option (str): The selected checklist option.
            - comment (str): User's comment.
            - photo_link (str): Link to the user's photograph.
            - report (str): User's report.

            The object also initializes a connection to the SQLite database for storing information.
        """

        self.location = location               # Выбранное местоположение пользователя
        self.option = option                   # Выбранный вариант чек-листа
        self.comment = comment                 # Комментарий пользователя
        self.photo_link = photo_link           # Ссылка на фотографию пользователя
        self.report = report                   # Отчет пользователя
        with sq.connect('ai_bd.db') as base:   # Установка соединения с базой данных SQLite
            self.db_base = base                # База данных для хранения информации
            self.db_cursor = base.cursor()     # Курсор для взаимодействия с базой данных

    def generate_report(self) -> str:
        """
            Generates a report text based on location data, checklist, comment, and a photograph.

            Returns:
            - str: Formatted text of the report.
        """

        try:
            report = f"Location: {self.location}\n"
            report += f"Checklist option: {self.option}\n"

            if self.comment:
                report += f"Comment: {self.comment}\n"

            if self.photo_link:
                report += f"Photo Link: {self.photo_link}\n"

            return report
        except Exception as e:
            detailed_send_message_error = traceback.format_exc()
            return f"Error generating report: {str(e)}\n{detailed_send_message_error}"
