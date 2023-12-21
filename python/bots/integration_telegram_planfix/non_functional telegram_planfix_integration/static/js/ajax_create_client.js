// static/ajax_create_client.js

// Функция для создания клиента
function createClient() {
    const clientName = $("#clientName").val();
    const clientChannel = $("#clientChannel").val();

    const data = {
        "name": clientName,
        "channel": clientChannel
    };

    let createdClientId, createdToken;

    $.ajax({
        type: "POST",
        url: "/telegram/create_client",
        contentType: "application/json;charset=UTF-8",
        data: JSON.stringify(data)
    })
        .done(function (response) {
            if (response.client_id && response.token) {
                createdClientId = response.client_id;
                createdToken = response.token;

                // Уведомление об успешном создании клиента
                Swal.fire({
                    icon: 'success',
                    title: 'Client created successfully!',
                    text: `Client ID: ${createdClientId}, Token: ${createdToken}`
                });

                // Вызываем функцию для получения статуса клиента
                getClientStatus(createdClientId);

                // Дополнительные действия при успешном создании клиента
            } else {
                // Уведомление об ошибке (неожиданный ответ от сервера)
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Unexpected response from the server!'
                });
            }
        })
        .fail(function (error) {
            // Уведомление об ошибке (AJAX-запрос завершился ошибкой)
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: error.responseText || 'Unknown error'
            });
        })
        .always(function () {
            console.log('createdClientId:', createdClientId);
            console.log('createdToken:', createdToken);
        });
}

