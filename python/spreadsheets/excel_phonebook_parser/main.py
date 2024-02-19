import pandas as pd
import phonenumbers
import warnings

from logger import logger


def open_table():
    print("Let's open the table!")
    file_name = '03-12.xlsx'  # Можно запросить у пользователя путь к файлу

    try:
        current_table = pd.read_excel(file_name)  # Попробуем открыть как Excel
    except pd.errors.ExcelFileError:
        try:
            current_table = pd.read_csv(file_name)  # Попробуем открыть как CSV
        except pd.errors.ParserError:
            print("Unsupported file format. Please provide a valid XLS, XLSX, or CSV file.")
            return None

    print("Table successfully opened.")
    return current_table


def extract_contacts(table):
    if table is not None:
        # Создаем список словарей для хранения данных
        contacts = []

        # Получаем датафреймы для каждого листа
        keys_df = table["ADRESS"]
        values_df = table["Unnamed: 1"]

        for index, value in values_df.items():
            contact = {"Name": "", "Country": "", "Phone": ""}

            if "NAME:" in keys_df.iloc[index]:
                contact["Name"] = value
                logger.info(f"Name: {contact['Name']}")
            if "COUNTRY:" in keys_df.iloc[index]:
                contact["Country"] = value
                logger.info(f"Country: {contact['Country']}")
            if "TELEPHONE:" in keys_df.iloc[index]:
                contact["Phone"] = value
                logger.info(f"Phone: {contact['Phone']}")

            contacts.append(contact)
        logger.info("After extracting")
        # Выводим список контактов
        # Удаляем пустые поля в контактах
        # for contact in contacts:
        #     contact = {key: value for key, value in contact.items() if value}  # Оставляем только непустые значения
        #     logger.info(f"Contact: {contact}")
        #     formatted_phone = "+" + str(phonenumbers.country_code_for_region(contact["Country"])) + str(
        #         contact["Phone"])
            # print(f"{contact['Name']}: {formatted_phone}")
    else:
        print("No table is currently open.")


def main():
    # Подавляем предупреждения о нежелательности использования Pyarrow
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    table = open_table()
    extract_contacts(table)


if __name__ == "__main__":
    main()
