# SQL Задачи - Task Manager Database

## Таблицы

```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50),
    project_id INT REFERENCES projects(id)
);
```

## 1. Получить все уникальные статусы (без повторений), отсортированные алфавитно
SELECT DISTINCT status
FROM tasks
WHERE status IS NOT NULL
ORDER BY status ASC;

## 2. Получить количество всех задач в каждом проекте, отсортированное по убыванию количества задач
SELECT 
    p.id,
    p.name,
    COUNT(t.id) AS task_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
GROUP BY p.id, p.name
ORDER BY task_count DESC;

## 3. Количество задач в каждом проекте, отсортированное по названию проекта
SELECT 
    p.id,
    p.name,
    COUNT(t.id) AS task_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
GROUP BY p.id, p.name
ORDER BY p.name ASC;

## 4. Получить задачи для всех проектов, названия которых начинаются с буквы "N"
SELECT 
    t.id,
    t.name AS task_name,
    p.name AS project_name,
    t.status
FROM tasks t
INNER JOIN projects p ON t.project_id = p.id
WHERE p.name LIKE 'N%'
ORDER BY p.name, t.name;

## 5. Список проектов, содержащих букву 'a' в середине названия, с количеством задач
SELECT 
    p.id,
    p.name AS project_name,
    COUNT(t.id) AS task_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
WHERE p.name ILIKE '_%a%_'
GROUP BY p.id, p.name
ORDER BY p.name;

## 6. Список задач с дублирующимися названиями, отсортированный алфавитно
SELECT 
    id,
    name,
    status,
    project_id
FROM tasks
WHERE name IN (
    SELECT name
    FROM tasks
    GROUP BY name
    HAVING COUNT(*) > 1
)
ORDER BY name ASC, id;

## 7. Список задач с несколькими точными совпадениями имени и статуса из проекта 'Delivery', отсортированный по количеству совпадений
SELECT name, status, COUNT(*) AS match_count
FROM tasks
WHERE project_id IN (SELECT id FROM projects WHERE name = 'Delivery')
GROUP BY name, status
HAVING COUNT(*) > 1
ORDER BY match_count DESC, name;

## 8. Список названий проектов, имеющих более 10 задач со статусом 'completed', отсортированный по project_id
SELECT 
    p.id,
    p.name,
    COUNT(t.id) AS completed_task_count
FROM projects p
INNER JOIN tasks t ON p.id = t.project_id
WHERE t.status = 'completed'
GROUP BY p.id, p.name
HAVING COUNT(t.id) > 10
ORDER BY p.id ASC;