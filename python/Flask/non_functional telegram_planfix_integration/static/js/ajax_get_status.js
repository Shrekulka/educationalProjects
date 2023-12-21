// static/ajax_get_status.js

// Функция для получения статуса клиента
function getClientStatus(clientId) {
    $.ajax({
        type: "GET",
        url: `/get_status/${clientId}`,
    })
        .done(function (response) {
            console.log(response);  // Обработка успешного ответа от сервера
            // Здесь вы можете добавить дополнительную логику или обновление интерфейса с полученным статусом
        })
        .fail(function (error) {
            console.error(error);  // Обработка ошибки
        });
}
