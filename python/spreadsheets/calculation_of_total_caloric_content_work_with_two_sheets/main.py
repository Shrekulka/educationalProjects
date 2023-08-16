import pandas as pd

# Настройка опций отображения
pd.set_option('display.max_columns', None)  # Показать все колонки
pd.set_option('display.width', None)  # Установить ширину вывода без ограничений
pd.set_option('display.max_rows', None)  # Показать все строки

# URL файла Excel для загрузки данных
xlsx_file = 'https://stepik.org/media/attachments/lesson/245290/trekking2.xlsx'

# Загрузка данных из Excel
xls = pd.ExcelFile(xlsx_file)

# Загрузка данных из первого листа и переименование столбцов
table_first = xls.parse(0)  # Загрузка данных первого листа
table_first = table_first.rename(columns={table_first.columns[0]: 'Name'})  # Переименование столбцов
print(table_first)  # Вывод первой таблицы
print('\n')

# Загрузка данных из второго листа и переименование столбцов
table_second = xls.parse(1)  # Загрузка данных второго листа
table_second = table_second.rename(columns={table_second.columns[0]: 'Name'})  # Переименование столбцов
print(table_second)  # Вывод второй таблицы
print('\n')

# Этот код выполняет операцию объединения (слияния) двух DataFrame (таблиц) table_first и table_second на основе общего
# столбца 'Name'. Здесь объяснение параметров функции pd.merge():

# table_first: Первый DataFrame, который вы хотите объединить.
# table_second: Второй DataFrame, который вы хотите объединить.
# how='inner': Определяет тип объединения. В данном случае, 'inner' означает, что будут выбраны только строки, которые
# присутствуют в обоих таблицах.
# on='Name': Указывает столбец, по которому будет происходить объединение.
# В результате выполнения этой операции, table_merged будет содержать объединенную таблицу, в которой строки, имеющие
# общее значение в столбце 'Name' в обоих исходных таблицах, будут объединены в одну строку.
table_merged = pd.merge(table_first, table_second, how='inner', on='Name')
print(table_merged)  # Вывод объединенной таблицы
print('\n')

# Агрегация данных

# Расчет суммы калорий
calories = int((table_merged[table_merged.columns[1]] * table_merged[table_merged.columns[5]] / 100).sum())
# Расчет суммы белка
protein = int((table_merged[table_merged.columns[2]] * table_merged[table_merged.columns[5]] / 100).sum())
# Расчет суммы жиров
fat = int((table_merged[table_merged.columns[3]] * table_merged[table_merged.columns[5]] / 100).sum())
# Расчет суммы углеводов
carbohydrates = int((table_merged[table_merged.columns[4]] * table_merged[table_merged.columns[5]] / 100).sum())

# Вывод результатов
print(calories, protein, fat, carbohydrates)
