# ---- Stage 1: Compile TypeScript ----
FROM node:20 AS ts-builder
WORKDIR /ts
COPY modules/orders/static/orders/ts/package.json \
     modules/orders/static/orders/ts/tsconfig.json \
     modules/orders/static/orders/ts/*.ts \
     ./
RUN npm install && npx tsc

# ---- Stage 2: Final Python image ----
FROM python:3.13-slim

# Встановлюємо необхідні системні пакети (без Node.js)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту
COPY . .

# Копіюємо скомпільований JavaScript зі stage-1
COPY --from=ts-builder /ts/*.js /app/modules/orders/static/orders/js/

# Точка входу (Gunicorn для production)
CMD ["sh", "entrypoint.prod.sh"]
EXPOSE 8000