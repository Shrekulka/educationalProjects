# flask_database/f_data_base.py

import traceback


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        # language=SQL
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)  # Заменено с executer на execute
            res = self.__cur.fetchall()
            if res:
                return res

        except Exception as error:
            # Обработка неожиданных ошибок с использованием логирования
            detailed_send_message_error = traceback.format_exc()
            print(f"Ошибка чтения из BD: {error}\n{detailed_send_message_error}")

        return []
