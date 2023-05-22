// Данный код решает задачу ввода данных о студенте и их проверки. Он запрашивает у пользователя полное имя студента и
// оценки по предметам (математика, физика, химия). После ввода данных, производится проверка на их корректность, а
// затем выводится информация о студенте, включая имя, оценки по каждому предмету и среднюю оценку.
// Структура student определяет поля для хранения ФИО и оценок по предметам, а также метод aver, который вычисляет
// среднюю оценку студента.
// Функции isValidGrade и isValidFIO проверяют корректность оценки и ФИО соответственно. Они используются для валидации
// введенных данных.
// Операторы >> и << перегружены для структуры student и обеспечивают ввод и вывод данных студента соответственно.

#include <iostream>
#include <fstream>
#include <string>
#include <regex>

using namespace std;

struct student
{
	string fio {};  // Инициализируем поле ФИО пустой строкой
	int math{}, phys{}, chem{};  // Инициализируем оценки по предметам нулевыми значениями
	double aver() const;  // Метод aver объявлен как const
};

istream& operator>>(istream& obj, student& st);  // Оператор ввода
ostream& operator<<(ostream& obj, const student& st);  // Оператор вывода

bool isValidGrade(int grade);  // Функция для проверки корректности оценки
bool isValidFIO(const string& name);  // Функция для проверки корректности ФИО

int main()
{
	student st;  // Создаем объект типа student

	cout << "Enter the student's full name separated by a space (First Name Last Name):\n";
	do
	{
		cin >> st;  // Вводим имя студента
	} while (!isValidFIO(st.fio));  // Проверяем корректность ФИО

	string subjects[] = {"math", "physics", "chemistry"};  // Массив с названиями предметов
	int grades[] = {st.math, st.phys, st.chem};  // Массив с оценками предметов

	for (size_t i = 0; i < 3; i++)
	{
		cout << "Enter the " << subjects[i] << " grade: ";  // Выводим запрос на ввод оценки для текущего предмета
		do
		{
			cin >> grades[i];  // Вводим оценку
		} while (!isValidGrade(grades[i]));  // Проверяем корректность оценки
	}

	st.math = grades[0];  // Присваиваем оценки студенту из массива grades
	st.phys = grades[1];
	st.chem = grades[2];

	cout << "\nStudent information:\n";
	cout << st;  // Выводим информацию о студенте

	return 0;
}

istream& operator>>(istream& obj, student& st)
{
	cin.ignore();  // Игнорируем символ новой строки во входном потоке
	getline(obj, st.fio);  // Вводим имя студента

	return obj;
}

ostream& operator<<(ostream& obj, const student& st)
{
	obj << "Student's name: " << st.fio << "\n";  // Выводим имя студента
	obj << "Math grade: " << st.math << "\n";  // Выводим оценку по математике
	obj << "Physics grade: " << st.phys << "\n";  // Выводим оценку по физике
	obj << "Chemistry grade: " << st.chem << "\n";  // Выводим оценку по химии
	obj << "Average grade: " << st.aver() << "\n";  // Выводим среднюю оценку

	return obj;
}

double student::aver() const
{
	return (math + phys + chem) / 3.0;  // Вычисляем среднюю оценку
}

bool isValidGrade(int grade)
{
	return (grade >= 0 && grade <= 12);  // Проверяем, что оценка находится в диапазоне от 0 до 12
}

bool isValidFIO(const string& name)
{
	regex pattern(R"([a-zA-Z]+\s[a-zA-Z]+)");  // Паттерн для ФИО: имя и фамилия, разделенные пробелом
	if (regex_match(name, pattern))
	{
		return true;  // ФИО соответствует требованиям
	}
	else
	{
		cout << "Invalid name. Please enter a valid name.\n";  // Выводим сообщение об ошибке
		return false;  // ФИО не соответствует требованиям
	}
}
