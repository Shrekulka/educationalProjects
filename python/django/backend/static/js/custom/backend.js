// Функция для получения значения cookie по имени
const getCookie = (name) => {
  let cookieValue = null; // Переменная для хранения значения cookie

  // Проверяем, есть ли cookies в документе и не пустые ли они
  if (document.cookie && document.cookie !== "") {
    // Разделяем строку cookies на массив отдельных cookies
    const cookies = document.cookie.split(";");

    // Перебираем массив cookies
    for (let i = 0; i < cookies.length; i++) {
      // Удаляем пробелы в начале и в конце текущего cookie
      const cookie = cookies[i].trim();

      // Проверяем, начинается ли текущая строка cookie с нужного имени
      if (cookie.substring(0, name.length + 1) === name + "=") {
        // Если да, декодируем и сохраняем значение cookie
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break; // Прекращаем поиск, так как нашли нужное cookie
      }
    }
  }

  // Возвращаем значение cookie или null, если cookie не найден
  return cookieValue;
};

// Получаем значение CSRF токена, используя функцию getCookie
const csrftoken = getCookie("csrftoken");
