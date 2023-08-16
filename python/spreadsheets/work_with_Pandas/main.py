import pandas as pd


class TableManager:
    def __init__(self):
        self.current_table = None  # Атрибут для хранения текущей таблицы
        self.current_sheet = None  # Атрибут для хранения текущего листа таблицы

    def create_table(self):
        print("Let's create a table!!!\n")
        sheets_number = int(input("Enter the number of sheets: "))
        dict_sheets = {}

        for i in range(1, sheets_number + 1):
            sheets_title = input(f"Enter a title for sheet {i}: ")
            dict_table = {}
            columns_number = int(input("Enter the number of columns: "))

            for j in range(columns_number):
                columns_title = input(f"Enter a title for column {j + 1}: ")
                dict_table[j] = {"title": columns_title, "data": {}}

            rows_number = int(input("Enter the number of rows: "))

            for k in range(rows_number):
                rows_title = input(f"Enter a title for row {k + 1}: ")
                dict_table[k] = {"title": rows_title, "data": {}}

            while True:
                print("How would you like to complete the table?\n1. by line\n2. by columns\n")
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    for row_number in range(rows_number):
                        for col_number in range(columns_number):
                            value = input(
                                f"Enter data for row '{dict_table[row_number]['title']}' and column '{dict_table[col_number]['title']}': ")
                            dict_table[row_number]["data"][col_number] = value
                elif choice == 2:
                    for col_number in range(columns_number):
                        for row_number in range(rows_number):
                            value = input(
                                f"Enter data for column '{dict_table[col_number]['title']}' and row '{dict_table[row_number]['title']}': ")
                            dict_table[col_number]["data"][row_number] = value
                else:
                    print("Invalid choice. Please enter '1' for rows or '2' for columns.")
                    continue

                break

            dict_sheets[sheets_title] = dict_table

        print("Table created successfully!")
        self.current_table = pd.DataFrame(dict_sheets)

    def open_table(self):
        print("Let's open the table!")
        file_name = input("Enter the path and name for the file: ")

        try:
            self.current_table = pd.read_excel(file_name)  # Попробовать открыть как Excel
        except pd.errors.ExcelFileError:
            try:
                self.current_table = pd.read_csv(file_name)  # Попробовать открыть как CSV
            except pd.errors.ParserError:
                print("Unsupported file format. Please provide a valid XLS, XLSX, or CSV file.")
                return

        print("Table successfully opened.")

    def show_all_tables(self):
        if self.current_table is not None:
            for i, sheet_name in enumerate(self.current_table.keys(), start=1):
                print(f"\n{i}. Sheet Name: {sheet_name}\n")
                print(self.current_table[sheet_name])
        else:
            print("No table is currently open.")

    def show_single_table(self):
        if self.current_table is not None:
            sheet_names = self.current_table.keys()

            print("Available sheets:")
            for i, sheet_name in enumerate(sheet_names, start=1):
                print(f"{i}. {sheet_name}")

            while True:
                try:
                    choice = int(input("Enter the number of the sheet you want to view: "))
                    if 1 <= choice <= len(sheet_names):
                        selected_sheet = list(sheet_names)[choice - 1]
                        print(f"\nSheet Name: {selected_sheet}\n")

                        # Temporary increase the maximum number of displayed rows for easy viewing
                        pd.set_option('display.max_rows', None)
                        print(self.current_table[selected_sheet])
                        pd.reset_option('display.max_rows')

                        break
                    else:
                        print("Invalid choice. Please enter a valid number.")
                except ValueError:
                    print("Invalid choice. Please enter a valid number.")
        else:
            print("No table is currently open.")

    def show_table(self):
        while True:
            try:
                print("How will we view the sheets?\n1. for all sheets\n2. for a single sheet")
                choice = int(input("Enter a choice: "))
                if choice == 1:
                    self.show_all_tables()
                    break
                elif choice == 2:
                    self.show_single_table()
                    break
                else:
                    print("Invalid choice. Please enter '1' or '2'.")
            except ValueError:
                print("Invalid choice. Please enter a valid number.")

    def save_to_file(self):
        if self.current_table is not None:
            print("Now save the table!\nWhat format will we save in:")

            supported_formats_df = pd.DataFrame({
                "Format name": ["xlsx", "csv"],
                "Save function": [self.current_table.to_excel, self.current_table.to_csv]
            })

            format_names = supported_formats_df["Format name"].tolist()
            for i, format_name in enumerate(format_names, start=1):
                print(f"{i}. {format_name}")

            while True:
                try:
                    choice = int(input("Enter the number of the format you want to save: "))
                    if 1 <= choice <= len(format_names):
                        selected_format = format_names[choice - 1]
                        save_func = supported_formats_df.loc[
                            supported_formats_df["Format name"] == selected_format, "Save function"].values[0]

                        file_name = input(
                            "Enter the path and name for the file without extension: ") + f".{selected_format}"

                        print("How will we save:\n1. with indexes\n2. without indexes")
                        choice_index = int(input("Enter a choice: "))
                        index_flag = True if choice_index == 1 else False

                        print("Will we keep the headers?\n1. yes\n2. no")
                        choice_headers = int(input("Enter a choice: "))
                        header_flag = True if choice_headers == 1 else False

                        save_func(file_name, index=index_flag, header=header_flag)
                        print(f"Table successfully saved to {file_name}")
                        break
                    else:
                        print(f"Invalid choice. Please enter a valid number (1-{len(format_names)}).")
                except ValueError:
                    print("Invalid choice. Please enter a valid number.")
        else:
            print("No table is currently open.")


# Пример использования
table_manager = TableManager()

while True:
    print("Menu:")
    print("1. Create a table")
    print("2. Open a table")
    print("3. Show tables")
    print("4. Save table")
    print("5. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        table_manager.create_table()
    elif choice == 2:
        table_manager.open_table()
    elif choice == 3:
        table_manager.show_table()
    elif choice == 4:
        table_manager.save_to_file()
    elif choice == 5:
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a valid number.")
