// Получаем элементы формы для добавления комментария
const commentForm = document.forms.commentForm;
const commentFormContent = commentForm.content;  // Поле ввода для содержимого комментария
const commentFormParentInput = commentForm.parent;  // Скрытое поле для идентификатора родительского комментария
const commentFormSubmit = commentForm.commentSubmit;  // Кнопка отправки формы
const commentArticleId = commentForm.getAttribute('data-article-id');  // Идентификатор статьи, к которой относится комментарий

// Добавляем обработчик события отправки формы, который вызывает функцию createComment
commentForm.addEventListener('submit', createComment);

// Инициализируем обработчики событий для кнопок "Ответить"
replyUser()

// Функция для добавления обработчиков событий для кнопок "Ответить"
function replyUser() {
    document.querySelectorAll('.btn-reply').forEach(e => {
        e.addEventListener('click', replyComment);  // Добавляем обработчик события клика для каждой кнопки
    });
}

// Функция, вызываемая при клике на кнопку "Ответить"
function replyComment() {
    const commentUsername = this.getAttribute('data-comment-username');  // Получаем имя автора комментария
    const commentMessageId = this.getAttribute('data-comment-id');  // Получаем идентификатор комментария
    commentFormContent.value = `${commentUsername}, `;  // Заполняем поле содержимого комментария, указывая имя автора
    commentFormParentInput.value = commentMessageId;  // Устанавливаем значение скрытого поля с идентификатором родительского комментария
}

// Асинхронная функция для создания комментария
async function createComment(event) {
    event.preventDefault();  // Предотвращаем стандартное поведение формы (перезагрузку страницы)
    commentFormSubmit.disabled = true;  // Отключаем кнопку отправки, чтобы предотвратить повторное нажатие
    commentFormSubmit.innerText = "Ожидаем ответа сервера";  // Изменяем текст кнопки, указывая на ожидание ответа сервера
    try {
        // Отправляем POST-запрос на сервер для создания нового комментария
        const response = await fetch(`/articles/${commentArticleId}/comments/create/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,  // Добавляем CSRF токен для защиты от CSRF атак
                'X-Requested-With': 'XMLHttpRequest',  // Указываем, что запрос является AJAX-запросом
            },
            body: new FormData(commentForm),  // Отправляем данные формы
        });

        const comment = await response.json();  // Получаем ответ сервера в формате JSON

        // Шаблон HTML для нового комментария
        let commentTemplate = `<ul id="comment-thread-${comment.id}">
                                <li class="card border-0">
                                    <div class="row">
                                        <!-- Отображение аватара автора комментария -->
                                        <div class="col-md-2">
                                            <img src="${comment.avatar}" style="width: 120px;height: 120px;object-fit: cover;" alt="${comment.author}"/>
                                        </div>
                                        <!-- Отображение содержимого комментария -->
                                        <div class="col-md-10">
                                            <div class="card-body">
                                                <h6 class="card-title">
                                                    <a href="${comment.get_absolute_url}">${comment.author}</a>
                                                </h6>
                                                <p class="card-text">
                                                    ${comment.content}
                                                </p>
                                                <!-- Кнопка для ответа на комментарий -->
                                                <a class="btn btn-sm btn-dark btn-reply" href="#commentForm" data-comment-id="${comment.id}" data-comment-username="${comment.author}">Ответить</a>
                                                <hr/>
                                                <!-- Время создания комментария -->
                                                <time>${comment.time_create}</time>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>`;
        // Вставляем новый комментарий в соответствующее место в дереве комментариев
        if (comment.is_child) {
            document.querySelector(`#comment-thread-${comment.parent_id}`).insertAdjacentHTML("beforeend", commentTemplate);
        } else {
            document.querySelector('.nested-comments').insertAdjacentHTML("beforeend", commentTemplate);
        }

        // Сбрасываем форму после успешного создания комментария
        commentForm.reset();
        commentFormSubmit.disabled = false;  // Включаем кнопку отправки
        commentFormSubmit.innerText = "Добавить комментарий";  // Возвращаем первоначальный текст кнопки
        commentFormParentInput.value = null;  // Очищаем скрытое поле с идентификатором родительского комментария
        replyUser();  // Повторно добавляем обработчики событий для кнопок "Ответить"
    } catch (error) {
        console.log(error);  // Выводим ошибку в консоль
    }
}
