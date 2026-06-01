// order-management-service/modules/orders/static/orders/js/order_form.js

const API_BASE = '/api';

let products = [];

// Функция получения CSRF-токена из cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function loadInitialData() {
    try {
        const [clientsRes, productsRes] = await Promise.all([
            fetch(`${API_BASE}/clients/`),
            fetch(`${API_BASE}/products/`)
        ]);
        const clientsData = await clientsRes.json();
        const productsData = await productsRes.json();
        products = productsData.results;

        const clientSelect = document.getElementById('client');
        clientsData.results.forEach(c => {
            const option = document.createElement('option');
            option.value = c.id;
            option.textContent = c.name;
            clientSelect.appendChild(option);
        });
        addItemRow();
    } catch (err) {
        showMessage('Помилка завантаження даних із сервера', 'error');
    }
}

function addItemRow() {
    const container = document.getElementById('items-container');
    const row = document.createElement('div');
    row.className = 'item-row';
    row.innerHTML = `
        <select class="product-select" required>
            <option value="">-- Оберіть товар --</option>
            ${products.map(p => `<option value="${p.id}">${p.name} (${p.price} грн)</option>`).join('')}
        </select>
        <input type="number" class="quantity" value="1" min="1" required>
        <button type="button" class="btn-remove">×</button>
    `;
    row.querySelector('.btn-remove').addEventListener('click', () => row.remove());
    container.appendChild(row);
}

document.getElementById('order-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const messageDiv = document.getElementById('message');
    messageDiv.style.display = 'none';

    const clientId = parseInt(document.getElementById('client').value);
    if (!clientId) return showMessage('Оберіть клієнта', 'error');

    const itemRows = document.querySelectorAll('.item-row');
    const items = [];
    itemRows.forEach(row => {
        const productId = parseInt(row.querySelector('.product-select').value);
        const quantity = parseInt(row.querySelector('.quantity').value);
        if (productId && quantity > 0) {
            items.push({ product_id: productId, quantity });
        }
    });

    if (items.length === 0) return showMessage('Додайте хоча б один товар', 'error');

    try {
        // Добавляем CSRF-токен в заголовок
        const csrftoken = getCookie('csrftoken');
        const response = await fetch(`${API_BASE}/orders/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ client_id: clientId, items })
        });
        const data = await response.json();
        if (response.ok) {
            showMessage(`✅ Замовлення #${data.id} створено! Сума: ${data.total_amount} грн`, 'success');
            document.getElementById('client').value = '';
            document.getElementById('items-container').innerHTML = '';
            addItemRow();
        } else {
            const detail = typeof data === 'string' ? data : JSON.stringify(data);
            showMessage(`Помилка: ${detail}`, 'error');
        }
    } catch (err) {
        showMessage(`Мережева помилка: ${err.message}`, 'error');
    }
});

function showMessage(text, type) {
    const msg = document.getElementById('message');
    msg.textContent = text;
    msg.className = `message ${type}`;
    msg.style.display = 'block';
}

document.getElementById('add-item').addEventListener('click', addItemRow);

loadInitialData();