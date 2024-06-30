// Выбираем кнопку подписки или отписки пользователя
const followBtn = document.querySelector('.btn-follow');

// Выбираем блок с подписчиками
const followerBox = document.querySelector('.followers-box');

// Добавляем обработчик события при клике на кнопку подписки или отписки
followBtn.addEventListener('click', event => {
    // Получаем уникальный идентификатор пользователя (slug) из атрибута data-slug кнопки
    const userSlug = event.target.dataset.slug;

    // Отправляем POST-запрос на сервер для создания или удаления подписки
    fetch(`/user/follow/${userSlug}/`, {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,  // Передаем CSRF-токен для безопасности
            "X-Requested-With": "XMLHttpRequest",  // Указываем тип запроса
        }
    })
        .then(response => response.json())  // Обрабатываем полученный JSON-ответ
        .then(data => {
            // Проверяем, является ли кнопка текущей подпиской или отпиской
            const isBtnPrimary = followBtn.classList.contains('btn-primary');

            // Получаем сообщение из ответа сервера или пустую строку, если сообщение не передано
            const message = data.message || '';

            // Изменяем стиль кнопки в зависимости от её текущего состояния (подписка или отписка)
            if (isBtnPrimary) {
                followBtn.classList.remove('btn-primary');
                followBtn.classList.add('btn-danger');
            } else {
                followBtn.classList.remove('btn-danger');
                followBtn.classList.add('btn-primary');
            }

            // Если подписка создана (status=true), добавляем нового подписчика в блок с подписчиками
            if (data.status) {
                followerBox.innerHTML += `
                <div class="col-md-2" id="user-slug-${data.slug}">
                    <a href="${data.get_absolute_url}">
                        <img src="${data.avatar}" class="img-fluid rounded-1" alt="${data.slug}"/>
                    </a>
                </div>
            `;
            } else {
                // Если подписка удалена (status=false), удаляем пользователя из блока с подписчиками
                const currentUserSlug = document.querySelector(`#user-slug-${data.slug}`);
                currentUserSlug && currentUserSlug.remove();
            }

            // Выводим сообщение о действии (подписка или отписка) на кнопке
            followBtn.innerHTML = message;
        });
});
