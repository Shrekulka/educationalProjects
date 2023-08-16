import pandas as pd

# Загрузка данных из Excel файла "trekking1.xlsx" в DataFrame df
df = pd.read_excel("trekking1.xlsx")

# Выбор столбцов с названиями продуктов и калорийностью с помощью индексирования
# [:, [0, 1]] выбирает все строки (:), а второй индекс [0, 1] выбирает столбцы 0 (названия) и 1 (калории)
calories = df.iloc[:, [0, 1]]

# Сортировка DataFrame по убыванию калорийности (столбец 1) и названию продукта (столбец 0)
# ascending=[False, True] указывает, что калории сортируются по убыванию, а продукты в алфавитном порядке
sorted_calories = calories.sort_values(by=[calories.columns[1], calories.columns[0]], ascending=[False, True])

# Вывод названий продуктов из первого столбца отсортированного DataFrame
for product in sorted_calories.iloc[:, 0]:
    print(product)
