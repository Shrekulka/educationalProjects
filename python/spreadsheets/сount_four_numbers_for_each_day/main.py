import pandas as pd
import math

# Настройка опций отображения для более подробного вывода данных
pd.set_option('display.max_columns', None)  # Показать все колонки без ограничений
pd.set_option('display.width', None)  # Установить ширину вывода без ограничений
pd.set_option('display.max_rows', None)  # Показать все строки без ограничений

# URL файла Excel для загрузки данных
xlsx_file = 'https://stepik.org/media/attachments/lesson/245290/trekking3.xlsx'

# Создание объекта ExcelFile для работы с файлом Excel
xls = pd.ExcelFile(xlsx_file)

# Загрузка данных из первого листа и заполнение пустых значений нулями
table_first = xls.parse(0).fillna(0)  # Загрузка данных первого листа
# Переименование столбцов: столбец 0 -> 'Name'
table_first = table_first.rename(columns={table_first.columns[0]: 'Name'})

# Загрузка данных из второго листа
table_second = xls.parse(1)  # Загрузка данных второго листа
# Переименование столбцов: столбец 1 -> 'Name'
table_second = table_second.rename(columns={table_second.columns[1]: 'Name'})

# Объединение таблиц на основе столбца 'Name'
table_merged = pd.merge(table_first, table_second, how='inner', on='Name')
# Объединение данных по столбцу 'Name' с использованием внутреннего объединения

# Вывод объединенной таблицы
print(table_merged)
print()
# Выполняем расчет общих значений питательных веществ для каждого продукта путем умножения содержания на 100 грамм
# продукта на вес в граммах продукта, деленный на 100. Рассчитанные значения сохраняются в новых столбцах
# 'Total Calories', 'Total Carbohydrates', 'Total Fat' и 'Total Protein' в объединенной таблице table_merged.
table_merged['Total Calories'] = table_merged['ККал на 100'] * table_merged['Вес в граммах'] / 100
table_merged['Total Carbohydrates'] = table_merged['Б на 100'] * table_merged['Вес в граммах'] / 100
table_merged['Total Fat'] = table_merged['Ж на 100'] * table_merged['Вес в граммах'] / 100
table_merged['Total Protein'] = table_merged['У на 100'] * table_merged['Вес в граммах'] / 100

# Данные группируются по столбцу 'День' (день недели) с помощью метода groupby, и производится агрегация общих значений
# питательных веществ для каждого дня с использованием функции sum.
aggregated_nutrient_totals = table_merged.groupby('День').agg({
    'Total Calories': sum,
    'Total Carbohydrates': sum,
    'Total Fat': sum,
    'Total Protein': sum
})

# Сброс индексов для превращения индекса 'День' в обычный столбец
# Если вы планируете сохранить агрегированные данные в файл или в базу данных, индекс 'День' становится частью данных,
# и вам может потребоваться его сохранить в виде столбца.
aggregated_nutrient_totals.reset_index(inplace=True)

# Применение функции floor к агрегированным значениям питательных веществ
aggregated_nutrient_totals = aggregated_nutrient_totals.applymap(math.floor)

# Добавление агрегированных данных обратно в исходную таблицу по столбцу 'День'
table_merged = table_merged.merge(aggregated_nutrient_totals, on='День')

print(table_merged.sort_values(by='День'))
print()

# Вывод агрегированных значений питательных веществ для каждого дня
for _, row in aggregated_nutrient_totals.iterrows():
    print(row['Total Calories'], row['Total Carbohydrates'], row['Total Fat'], row['Total Protein'])
