#include <iostream>
#include <cmath>

// Округление в C++ довольно часто требуется для выполнения различных задач. Существует большое количество вариантов
// округления, в зависимости от необходимого значения.

int main()
{
	double uah {}, a {}, b {}, c {}, d {};
	double usd = 26.6422;
	double gbp = 36.4199;
	double bam = 15.93;
	double rub = 0.36494;

	std::cout << "Введите сумму в гривне, которую надо конвертировать : \n";
	std::cin >> uah;

	a = uah / usd;
	b = uah / gbp;
	c = uah / bam;
	d = uah / rub;

// Рекомендуется использовать оператор std::fixed перед выводом чисел с фиксированной точностью, чтобы избежать вывода
// в научной нотации. Например, можно добавить std::cout << std::fixed; перед выводом сумм валют.
	std::cout << std::fixed;
	std::cout << "Сумма в американских долларах по курсу НБУ равна : " << round(a) << '\n';
	std::cout << "Сумма в фунтах стерлингов по курсу НБУ равна : " << round(b) << '\n';
	std::cout << "Сумма в марках равна по курсу НБУ равна : " << round(c) << '\n';
	std::cout << "Сумма в рублях по курсу НБУ равна : " << round(d) << '\n';
	system("pause");

// Самые распространенные – это функции round(), ceil(), floor() и trunc(). Если первая выполняет математически правильное
// округление, то есть к ближайшему целому, а 0,5 к более дальнему от 0, то ceil() округляет в сторону большего, а floor()
// - в сторону меньшего. Последняя функция trunc() скорее не округление, а простое отбрасывание дробной части.
	std::cout << std::fixed;
	double y;
	y = floor(2.8);
	printf(" floor %f\n", y);
	y = ceil(2.1);
	printf(" ceil %f\n", y);
	y = round(2.6);
	printf(" round %f\n", y);
	y = trunc(2.9);
	printf(" trunc %f\n", y);
// Программа выведет значения 2, 3, 3 и 2.

	std::cin.ignore();

	return 0;
}
