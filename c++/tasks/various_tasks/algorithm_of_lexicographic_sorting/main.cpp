// Нехай S = 's1s2...sa' і T = 't1t2...tb' будуть рядками довжини a і b відповідно (mi називається i-м літерою S). Ми
// кажемо, що S лексикографічно менше за T, позначаючи S <lex T, якщо:
// a < b і si = ti для всіх i = 1, 2, ..., a, або
// Існує індекс i ≤ min {a, b}, такий, що sj = tj для всіх j = 1, 2, ..., i − 1 і si < ti.
// Алгоритм лексикографічного сортування спрямований на сортування заданого набору n рядків у лексикографічному порядку
// за зростанням (у разі збігів через однакові рядки, то в неспадному порядку).
//
// Довжина кожного рядка у вхідному масиві обмежена 100 000 символами.
//
// Кожен рядок містить лише малі латинські літери.
//
// Сигнатура функції:
//
// void contains(std::vector<std::string>& strings);
//
// Напишіть рішення. Виведіть результат у консоль.
//
// Перевірте правильність вашого алгоритму.
//
// У коментарях поясніть час виконання і складність за простором для вашого алгоритму.
//
// Примітка: не використовуйте функції сортування std.
//
//
//
// Приклади тестових випадків:
//
// Вхідні дані: ["hello", "world", "apple", "banana", "cat", "dog"]
// Вихід: apple banana cat dog hello world
//
// Вхідні дані: ["zebra", "apple", "banana", "cat", "dog"]
// Вихід: apple banana cat dog zebra
//
// Вхідні дані: ["cat", "dog", "mouse", "elephant", "tiger"]
// Вихід: cat dog elephant mouse tiger
//
// Вхідні дані: ["abcd", "abc", "abcde", "ab", "abcdef"]
// Вихід: ab abc abcd abcde abcdef
//
// Вхідні дані: []
// Вихід: a aa aaa aaaa aaaaa



#include <iostream>
#include <vector>

// Функція порівняння рядків
bool compareStrings(const std::string& s1, const std::string& s2) {
	const int len1 = s1.length();
	const int len2 = s2.length();
	int i = 0;

	// Порівнюємо символи рядків по одному
	while (i < len1 && i < len2) {
		if (s1[i] < s2[i]) {
			return true;
		} else if (s1[i] > s2[i]) {
			return false;
		}
		i++;
	}

	// Якщо один рядок є підстрокою іншого, повертаємо коротший рядок
	return len1 < len2;
}

// Функція сортування методом бульбашки
void bubbleSort(std::vector<std::string>& strings) {
	const int n = strings.size();
	bool swapped;

	// Застосовуємо сортування методом бульбашки
	for (int i = 0; i < n - 1; i++) {
		swapped = false;
		for (int j = 0; j < n - i - 1; j++) {
			// Порівнюємо два сусідніх рядки та, якщо потрібно, обмінюємо їх
			if (!compareStrings(strings[j], strings[j + 1])) {
				std::swap(strings[j], strings[j + 1]);
				swapped = true;
			}
		}
		// Якщо під час ітерації не було обмінів, вихід з циклу
		if (!swapped) {
			break;
		}
	}
}

int main() {
	std::vector<std::string> strings;
	std::string input;

	std::cout << "Введіть рядки (розділені комами та в лапках):" << std::endl;
	std::getline(std::cin, input);

	std::size_t start = 0;
	std::size_t end = input.find(',');

	// Розбиваємо введений рядок на окремі рядки
	while (end != std::string::npos) {
		std::string token = input.substr(start, end - start);
		// Видаляємо пробіли навколо рядка
		token.erase(0, token.find_first_not_of(' '));
		token.erase(token.find_last_not_of(' ') + 1);
		// Видаляємо лапки з рядка
		if (!token.empty() && token.front() == '\"' && token.back() == '\"') {
			token = token.substr(1, token.length() - 2);
		}
		strings.push_back(token);

		start = end + 1;
		end = input.find(',', start);
	}

	// Останній рядок після останньої коми
	std::string lastToken = input.substr(start);
	// Видаляємо пробіли навколо рядка
	lastToken.erase(0, lastToken.find_first_not_of(' '));
	lastToken.erase(lastToken.find_last_not_of(' ') + 1);
	// Видаляємо лапки з рядка
	if (!lastToken.empty() && lastToken.front() == '\"' && lastToken.back() == '\"') {
		lastToken = lastToken.substr(1, lastToken.length() - 2);
	}
	strings.push_back(lastToken);

	bubbleSort(strings);

	std::cout << "Вихід: ";
	for (int i = 0; i < strings.size(); i++) {
		std::cout << strings[i];
		if (i < strings.size() - 1) {
			std::cout << " ";
		}
	}
	std::cout << std::endl;

	return 0;
}
