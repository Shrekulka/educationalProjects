This code generates a plot of the sine function (sin(x)) over the interval from 0 to 10. It uses the matplotlib library 
to create the plot. Firstly, the plot settings are defined, such as axis ranges, labels, and more. Then, points for 
plotting are generated: sin(x) values are computed for different x values with a step of 0.01, and the corresponding 
coordinates (x, y) are added to the xs and sin_vals lists. Finally, the plt.plot() function is used to create the plot 
based on the xs and sin_vals lists. The plot is saved to the "sin.png" file, and then it's displayed using the plt.show()
function.




Этот код создает график функции синуса (sin(x)) на интервале от 0 до 10. Он использует библиотеку matplotlib для
создания графиков. Сначала определяются настройки графика, такие как диапазоны осей, подписи и т.д. Затем осуществляется
генерация точек для построения графика: значения функции sin(x) вычисляются для различных значений x на интервале с
шагом 0.01, и соответствующие координаты (x, y) добавляются в списки xs и sin_vals. Наконец, функция plt.plot()
используется для построения графика на основе списков xs и sin_vals. График сохраняется в файл "sin.png", и после этого
он отображается с помощью функции plt.show().