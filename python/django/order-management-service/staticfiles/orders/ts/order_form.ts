// order-management-service/modules/orders/static/orders/ts/order_form.ts

const API_BASE = '/api';

interface Client {
    id: number;
    name: string;
}

interface Product {
    id: number;
    name: string;
    price: string;
}

interface OrderItemPayload {
    product_id: number;
    quantity: number;
}

interface OrderResponse {
    id: number;
    total_amount: string;
}

let products: Product[] = [];

function getCookie(name: string): string | null {
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

async function loadInitialData(): Promise<void> {
    try {
        const [clientsRes, productsRes] = await Promise.all([
            fetch(`${API_BASE}/clients/`),
            fetch(`${API_BASE}/products/`)
        ]);
        const clientsData = await clientsRes.json();
        const productsData = await productsRes.json();
        products = productsData.results;

        const clientSelect = document.getElementById('client') as HTMLSelectElement;
        clientsData.results.forEach((c: Client) => {
            const option = document.createElement('option');
            option.value = c.id.toString();
            option.textContent = c.name;
            clientSelect.appendChild(option);
        });
        addItemRow();
    } catch (err) {
        showMessage('Помилка завантаження даних із сервера', 'error');
    }
}

function addItemRow(): void {
    const container = document.getElementById('items-container') as HTMLDivElement;
    const row = document.createElement('div');
    row.className = 'item-row';
    row.innerHTML = `
        <select class="product-select" required>
            <option value="">-- Оберіть товар --</option>
            ${products.map(p => `<option value="${p.id}">${p.name} (${p.price} грн)</option>`).join('')}
        </select>
        <input type="number" class="quantity" value="1" min="1" required style="width: 80px;">
        <button type="button" class="btn-remove">×</button>
    `;
    (row.querySelector('.btn-remove') as HTMLButtonElement).addEventListener('click', () => row.remove());
    container.appendChild(row);
}

document.getElementById('order-form')!.addEventListener('submit', async (e) => {
    e.preventDefault();
    const messageDiv = document.getElementById('message') as HTMLDivElement;
    messageDiv.style.display = 'none';

    const clientId = parseInt((document.getElementById('client') as HTMLSelectElement).value);
    if (!clientId) return showMessage('Оберіть клієнта', 'error');

    const itemRows = document.querySelectorAll('.item-row');
    const items: OrderItemPayload[] = [];
    itemRows.forEach(row => {
        const productId = parseInt((row.querySelector('.product-select') as HTMLSelectElement).value);
        const quantity = parseInt((row.querySelector('.quantity') as HTMLInputElement).value);
        if (productId && quantity > 0) items.push({ product_id: productId, quantity });
    });

    if (items.length === 0) return showMessage('Додайте хоча б один товар', 'error');

    try {
        const csrftoken = getCookie('csrftoken');
        const response = await fetch(`${API_BASE}/orders/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken || ''
            },
            body: JSON.stringify({ client_id: clientId, items })
        });
        const data: OrderResponse = await response.json();
        if (response.ok) {
            showMessage(`✅ Замовлення #${data.id} створено! Сума: ${data.total_amount} грн`, 'success');
            (document.getElementById('client') as HTMLSelectElement).value = '';
            document.getElementById('items-container')!.innerHTML = '';
            addItemRow();
        } else {
            showMessage(`Помилка: ${JSON.stringify(data)}`, 'error');
        }
    } catch (err: any) {
        showMessage(`Мережева помилка: ${err.message}`, 'error');
    }
});

function showMessage(text: string, type: string): void {
    const msg = document.getElementById('message') as HTMLDivElement;
    msg.textContent = text;
    msg.className = `message ${type}`;
    msg.style.display = 'block';
}

document.getElementById('add-item')!.addEventListener('click', addItemRow);

loadInitialData();