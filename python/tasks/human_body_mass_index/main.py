def calculate_bmi(height, weight):
    """
    Функция для вычисления индекса массы тела (ИМТ)
    weight: вес в килограммах
    height: рост в метрах
    Возвращает вычисленный ИМТ
    """
    bmi = weight / (height ** 2)
    return bmi


def interpret_bmi(bmi):
    """
    Функция для интерпретации индекса массы тела (ИМТ)
    bmi: индекс массы тела
    Выводит интерпретацию результата согласно рекомендациям Всемирной Организации Здравоохранения
    """
    if bmi < 18.5:
        return "Недостаточная масса тела"
    elif 18.5 <= bmi <= 24.99:
        return "Нормальная масса тела"
    elif 25 <= bmi <= 29.99:
        return "Избыточная масса тела"
    else:
        return "Ожирение"


def main():
    """
    Основная функция программы для расчета массы человека.
    Приветствует пользователя, запрашивает имя, возраст, вес и рост, вычисляет ИМТ и выводит его интерпретацию.
    """

    name = input("Введите ваше имя: ")
    age = int(input("Сколько полных лет вам исполнилось? "))

    print(f"\nЗдравствуйте, {name}! Добро пожаловать в программу расчета массы тела.\n")

    weight = None
    height = None

    while True:
        weight_str = input("Введите ваш вес в килограммах: ")
        if not weight_str:
            print("Вес не может быть пустым. Попробуйте снова.")
            continue

        if not all(char.isdigit() or char in ['.', ','] for char in weight_str):
            print("Вес может содержать только цифры, точку (.) или запятую (,). Попробуйте снова.")
            continue

        weight_str = weight_str.replace(',', '.')
        try:
            weight = float(weight_str)
            if weight <= 0:
                print("Вес должен быть положительным числом. Попробуйте снова.")
                continue
        except ValueError:
            print("Некорректный ввод веса. Попробуйте снова.")
            continue

        break

    while True:
        height_str = input("Введите ваш рост в метрах: ")
        if not height_str:
            print("Рост не может быть пустым. Попробуйте снова.")
            continue

        if not all(char.isdigit() or char in ['.', ','] for char in height_str):
            print("Рост может содержать только цифры, точку (.) или запятую (,). Попробуйте снова.")
            continue

        height_str = height_str.replace(',', '.')
        try:
            height = float(height_str)
            if height <= 0:
                print("Рост должен быть положительным числом. Попробуйте снова.")
                continue
        except ValueError:
            print("Некорректный ввод роста. Попробуйте снова.")
            continue

        break

    bmi = calculate_bmi(height, weight)
    interpretation = interpret_bmi(bmi)

    print(f"\nРезультаты расчета для пользователя {name} (возраст: {age}):\n")
    print(f"Индекс массы тела (ИМТ): {bmi:.2f}")
    print(f"Заключение: {interpretation}")


if __name__ == "__main__":
    main()
