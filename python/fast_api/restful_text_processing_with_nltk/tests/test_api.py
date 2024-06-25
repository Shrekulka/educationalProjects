# restful_text_processing_with_nltk/tests/test_api.py

from typing import Dict, List

from fastapi.testclient import TestClient

from src.main import create_app

# Создание клиента для тестирования API
client = TestClient(create_app())


def test_tokenize() -> Dict[str, List[str]]:
    """
        Тест для проверки API endpoint /api/v1/tokenize.

        Отправляет POST-запрос с текстом "Hello, world!" и проверяет:
        1. Код ответа сервера должен быть 200 (успешный запрос).
        2. Ответ сервера должен содержать JSON с ожидаемым списком токенов.

        Returns:
            Dict[str, List[str]]: JSON-объект с полем "tokens", содержащим список токенов.
                                  Тип возвращаемого значения: словарь, ключи - строки,
                                  значения - списки строк.
    """
    # Отправляем POST-запрос на API endpoint /api/v1/tokenize с JSON-телом {"text": "Hello, world!"}
    response = client.post("/api/v1/tokenize", json={"text": "Hello, world!"})

    # Проверяем, что код ответа сервера равен 200 (успешный запрос)
    assert response.status_code == 200

    # Проверяем, что ответ сервера содержит ожидаемый JSON с полем "tokens"
    expected_json = {"tokens": ["Hello", ",", "world", "!"]}

    # Проверяет, что JSON-ответ сервера точно соответствует ожидаемому объекту `expected_json`.
    assert response.json() == expected_json

    # Возвращаем JSON-объект с полем "tokens"
    return response.json()


def test_pos_tag() -> None:
    """
        Тест для проверки API endpoint /api/v1/pos_tag.

        Отправляет POST-запрос с текстом "Hello, world!" и проверяет:
        1. Код ответа сервера должен быть 200 (успешный запрос).
        2. Ответ сервера должен содержать JSON с ожидаемым списком пар (токен, тег).

        Returns:
            None
    """
    # Отправляем POST-запрос на API endpoint /api/v1/pos_tag с JSON-телом {"text": "Hello, world!"}
    response = client.post("/api/v1/pos_tag", json={"text": "Hello, world!"})

    # Проверяем, что код ответа сервера равен 200 (успешный запрос)
    assert response.status_code == 200

    # Ожидаемый JSON-ответ с полем "pos_tags"
    expected_pos_tags = [["Hello", "NNP"], [",", ","], ["world", "NN"], ["!", "."]]

    # Проверяем, что JSON-ответ сервера точно соответствует ожидаемому списку тегов `expected_pos_tags`
    assert response.json()["pos_tags"] == expected_pos_tags


def test_ner() -> None:
    """
        Тест для проверки API endpoint /api/v1/ner.

        Отправляет POST-запрос с текстом "Hello, John Doe!" и проверяет:
        1. Код ответа сервера должен быть 200 (успешный запрос).
        2. Ответ сервера должен содержать непустой список сущностей (entities).

        Returns:
            None
    """
    # Отправляем POST-запрос на API endpoint /api/v1/ner с JSON-телом {"text": "Hello, John Doe!"}
    response = client.post("/api/v1/ner", json={"text": "Hello, John Doe!"})

    # Проверяем, что код ответа сервера равен 200 (успешный запрос)
    assert response.status_code == 200

    # Проверяем, что в ответе есть хотя бы одна сущность в списке "entities"
    assert len(response.json()["entities"]) > 0


def test_invalid_input() -> None:
    """
        Тест для проверки некорректного ввода на API endpoint /api/v1/tokenize.

        Отправляет POST-запрос с пустым текстом и проверяет:
        1. Код ответа сервера должен быть 422 (некорректный запрос).

        Returns:
            None
    """
    # Отправляем POST-запрос на API endpoint /api/v1/tokenize с пустым JSON-телом
    response = client.post("/api/v1/tokenize", json={"text": ""})

    # Проверяем, что код ответа сервера равен 422 (некорректный запрос)
    assert response.status_code == 422  # Unprocessable Entity


def test_rate_limit() -> None:
    """
        Тест для проверки ограничения запросов на API endpoint /api/v1/tokenize.

        Отправляет POST-запросы с текстом "Test" более 10 раз и проверяет:
        1. Код ответа сервера должен быть 429 (слишком много запросов).

        Returns:
            None
    """
    # Отправляем более 10 POST-запросов на API endpoint /api/v1/tokenize с текстом "Test"
    for _ in range(11):
        response = client.post("/api/v1/tokenize", json={"text": "Test"})

    # Проверяем, что последний код ответа сервера равен 429 (слишком много запросов)
    assert response.status_code == 429  # Too Many Requests
