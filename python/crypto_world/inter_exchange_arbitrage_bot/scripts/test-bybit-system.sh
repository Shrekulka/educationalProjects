#!/usr/bin/env bash

# Определяем пути
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_ROOT/.env"

echo "Загружаем переменные из .env файла: $ENV_FILE"

# Проверяем существование файла
if [ ! -f "$ENV_FILE" ]; then
    echo "Ошибка: файл .env не найден по пути: $ENV_FILE"
    exit 1
fi

# Загружаем переменные напрямую
export $(grep -v '^#' "$ENV_FILE" | grep -v '^$' | xargs)

echo "Переменные загружены успешно"

# Отладочная информация
echo "DEBUG: Проверяем загруженные переменные..."
echo "BYBIT_API_KEY: ${BYBIT_API_KEY:-NOT_SET}"
echo "BYBIT_API_SECRET: ${BYBIT_API_SECRET:-NOT_SET}"
echo "BYBIT_TESTNET: ${BYBIT_TESTNET:-NOT_SET}"
echo ""

# Проверяем, что необходимые переменные установлены
if [ -z "$BYBIT_API_KEY" ] || [ -z "$BYBIT_API_SECRET" ]; then
    echo "Ошибка: BYBIT_API_KEY и BYBIT_API_SECRET должны быть установлены в .env файле"
    echo "Добавьте в .env файл:"
    echo "BYBIT_API_KEY=ваш_api_key"
    echo "BYBIT_API_SECRET=ваш_secret_key"
    echo ""
    echo "Текущее содержимое .env файла:"
    cat "$ENV_FILE"
    exit 1
fi

# Используем переменные из .env
API_KEY="$BYBIT_API_KEY"
SECRET="$BYBIT_API_SECRET"

echo "Тестируем подключение к Bybit API..."
echo "API Key: ${API_KEY:0:8}..." # Показываем только первые 8 символов для безопасности

# Определяем URL в зависимости от настройки
if [ "$BYBIT_TESTNET" = "True" ]; then
    BASE_URL="https://api-testnet.bybit.com"
    echo "Используется TESTNET"
else
    BASE_URL="https://api.bybit.com"
    echo "Используется MAINNET"
fi

# Настройка запроса (используем более простой эндпоинт)
API_METHOD="GET"
API_CALL="v5/account/info"

# Подписываем запрос
recv_window=5000
timestamp=$(date +%s000)
api_params=""  # Пустые параметры для простого теста

# Создаем подпись
signature=$(echo -n "${timestamp}${API_KEY}${recv_window}${api_params}" \
    | openssl dgst -sha256 -hmac "${SECRET}" \
    | awk '{print $2}')

echo "Отправляем запрос: [$API_METHOD] $API_CALL?$api_params"
echo "Timestamp: $timestamp"
echo "Signature: ${signature:0:16}..." # Показываем только часть подписи
echo ""

# Отправляем запрос
response=$(curl -s -X "$API_METHOD" \
    -H "X-BAPI-API-KEY: $API_KEY" \
    -H "X-BAPI-TIMESTAMP: $timestamp" \
    -H "X-BAPI-SIGN: $signature" \
    -H "X-BAPI-RECV-WINDOW: $recv_window" \
    "$BASE_URL/$API_CALL?$api_params")

echo "Ответ от сервера:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

# Проверяем успешность запроса
if echo "$response" | grep -q '"retCode":0'; then
    echo ""
    echo "✅ Подключение к Bybit API успешно!"
else
    echo ""
    echo "❌ Ошибка подключения к Bybit API"
    echo "Проверьте правильность API ключей и их права доступа"
fi