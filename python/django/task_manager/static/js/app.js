/**
 * Task Manager - Клиентская валидация и drag-and-drop
 * Требование ТЗ: "It should have a client side and server side validation"
 */

function validateInput(input) {
    const errors = [];
    const value = input.value.trim();
    const type = input.type;
    const minLength = parseInt(input.minLength) || 0;
    const maxLength = input.maxLength > 0 ? parseInt(input.maxLength) : Infinity;
    const required = input.hasAttribute('required');

    if (required && !value) {
        errors.push(`${getFieldLabel(input)} is required`);
        return errors;
    }
    if (!required && !value) return errors;

    if (value.length < minLength && minLength > 0) {
        errors.push(`${getFieldLabel(input)} must be at least ${minLength} characters`);
    }
    if (value.length > maxLength) {
        errors.push(`${getFieldLabel(input)} must not exceed ${maxLength} characters`);
    }

    if (type === 'email' && !isValidEmail(value)) {
        errors.push(`${getFieldLabel(input)} must be a valid email`);
    }

    return errors;
}

function getFieldLabel(input) {
    const label = document.querySelector(`label[for="${input.id}"]`);
    if (label) return label.textContent.replace('*', '').trim();
    return input.name || 'Field';
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function addErrorClass(input) {
    input.classList.add('is-invalid');
    input.classList.remove('is-valid');
}

function removeErrorClass(input) {
    input.classList.remove('is-invalid');
}

function showError(input, message) {
    let errorEl = input.parentElement.querySelector('.invalid-feedback');
    if (!errorEl) {
        errorEl = document.createElement('div');
        errorEl.className = 'invalid-feedback d-block';
        input.parentElement.appendChild(errorEl);
    }
    errorEl.textContent = message;
    errorEl.style.display = 'block';
}

function hideError(input) {
    const errorEl = input.parentElement.querySelector('.invalid-feedback');
    if (errorEl) errorEl.style.display = 'none';
}

// Очистка ошибок при фокусе
document.addEventListener('focusin', function (evt) {
    const input = evt.target;
    if (input.classList && input.classList.contains('is-invalid')) {
        removeErrorClass(input);
    }
});

// Очистка формы после успешной отправки (HTMX)
document.addEventListener('htmx:afterRequest', function (evt) {
    const form = evt.detail.elt.closest('form');
    if (form && evt.detail.xhr.status === 200) {
        form.reset();
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => removeErrorClass(input));
        const errors = form.querySelectorAll('.invalid-feedback');
        errors.forEach(err => err.style.display = 'none');
    }
});

// ============================================================================
// 3. DRAG-AND-DROP (Alpine.js + параметризация)
// ============================================================================

function taskManager(containerId) {
    return {
        draggedTask: null,
        handleDrop(event) {
            event.preventDefault();
            const container = document.querySelector(`#${containerId}`);
            if (!container) return;
            const taskIds = Array.from(container.querySelectorAll('.task-item'))
                .map(el => el.dataset.taskId);

            // ✅ Исправление: получаем токен напрямую из DOM
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
            if (!csrfToken) {
                console.warn('CSRF token not found!');
                return;
            }

            // Отправить новый порядок на сервер
            fetch('/tasks/bulk-update-order/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken, // ← используем найденный токен
                },
                body: JSON.stringify({task_ids: taskIds}),
            });
            this.draggedTask = null;
        }
    };
}