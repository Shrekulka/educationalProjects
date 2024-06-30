// Выбираем все кнопки рейтинга на странице
const ratingButtons = document.querySelectorAll('.rating-buttons');

// Для каждой кнопки добавляем слушатель события 'click'
ratingButtons.forEach(button => {
    button.addEventListener('click', event => {
        // Получаем значение рейтинга из data-атрибута кнопки
        const value = parseInt(event.target.dataset.value);
        // Получаем id статьи из data-атрибута кнопки
        const articleId = parseInt(event.target.dataset.article);
        // Находим элемент, который будет отображать сумму рейтинга
        const ratingSum = button.querySelector('.rating-sum');

        // Создаем объект FormData для отправки данных на сервер
        const formData = new FormData();
        // Добавляем id статьи и значение рейтинга в FormData
        formData.append('article_id', articleId);
        formData.append('value', value);

        // Отправляем POST-запрос на сервер с использованием fetch
        fetch("/rating/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,  // CSRF-токен для защиты от CSRF-атак
                "X-Requested-With": "XMLHttpRequest",  // Заголовок, указывающий на AJAX-запрос
            },
            body: formData  // Передаем FormData в теле запроса
        }).then(response => response.json())  // Обрабатываем полученный ответ как JSON
            .then(data => {
                // После успешного получения ответа обновляем значение на кнопке
                ratingSum.textContent = data.rating_sum;
            })
            .catch(error => console.error(error));  // Обрабатываем ошибки запроса
    });
});
