import matplotlib as mpl
import matplotlib.pyplot as plt
import math

# Задаём разрешение изображения и размер фигуры
dpi = 80
fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))

# Обновляем параметры шрифта для графика
mpl.rcParams.update({'font.size': 10})

# Задаём интервалы значений осей x и y
plt.axis([0, 10, -1.5, 1.5])

# Задаём заголовок графика и подписи осей
plt.title('Синус и Косинус')
plt.xlabel('x')
plt.ylabel('F(x)')

# Инициализируем списки для хранения значений x, sin(x) и cos(x)
xs = []
sin_vals = []
cos_vals = []

# Заполняем списки значениями синуса и косинуса для заданных значений x
x = 0.0
while x < 10.0:
    sin_vals += [math.sin(3 * x)]
    cos_vals += [math.cos(x)]
    xs += [x]
    x += 0.1

# Строим графики для sin(3x) и cos(x) с разными стилями линий и цветами.
plt.plot(xs, sin_vals, color='blue', linestyle='solid',
         label='sin(3x)')
plt.plot(xs, cos_vals, color='red', linestyle='dashed',
         label='cos(x)')

# Добавляем легенду в правом верхнем углу
plt.legend(loc='upper right')

# Сохраняем график в файл
fig.savefig('trigan.png')
