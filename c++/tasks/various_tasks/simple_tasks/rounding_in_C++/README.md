Данный код позволяет пользователю конвертировать сумму в гривнах в другие валюты (доллары, фунты стерлингов, марки и 
рубли) с использованием заданных курсов обмена. Он также демонстрирует использование функций округления `round()`, 
`floor()`, `ceil()` и `trunc()`.

1. Запрашивает у пользователя сумму в гривнах, которую необходимо конвертировать.
2. Инициализирует переменные `uah`, `a`, `b`, `c` и `d` со значениями 0.
3. Устанавливает курсы обмена валют: `usd` - курс доллара к гривне, `gbp` - курс фунта стерлингов к гривне, `bam` - 
   курс марки к гривне, `rub` - курс рубля к гривне.
4. Вычисляет суммы валют, разделив введенную сумму в гривнах на соответствующие курсы обмена, и сохраняет результаты в 
   переменные `a`, `b`, `c` и `d`.
5. Выводит на экран суммы валют, округленные с помощью функции `round()`, и соответствующие им валюты.
6. Выводит значения, округленные с помощью других функций (`floor()`, `ceil()`, `trunc()`), для демонстрации их 
   использования.
7. Ожидает ввода пользователя, чтобы программа не закрывалась сразу после вывода результатов.