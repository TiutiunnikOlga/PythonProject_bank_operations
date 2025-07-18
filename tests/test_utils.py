import pytest
import requests
from unittest.mock import patch, MagicMock
from src.utils import get_exchange_rate


# Тест успешного конвертирования
@patch('requests.get')
def test_successful_conversion(mock_get):
    # Мокаем успешный ответ API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 200,
        "data": {"USDRUB": 90.0}
    }
    mock_get.return_value = mock_response

    # Проверяем конвертацию для разных сумм
    assert get_exchange_rate("USD", "RUB", 1) == 90.0
    assert get_exchange_rate("USD", "RUB", 2) == 180.0
    assert get_exchange_rate("USD", "RUB", 0.5) == 45.0


# Тест обработки ошибки API
@patch('requests.get')
def test_api_error(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 400,
        "message": "Invalid API key"
    }
    mock_get.return_value = mock_response

    result = get_exchange_rate("USD", "RUB", 1)
    assert result is None


# Тест отсутствия валютной пары
@patch('requests.get')
def test_missing_pair(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 200,
        "data": {"EURRUB": 100.0}
    }
    mock_get.return_value = mock_response

    result = get_exchange_rate("USD", "RUB", 1)
    assert result is None


# Тест сетевой ошибки
@patch('requests.get')
def test_network_error(mock_get):
    mock_get.side_effect = requests.ConnectionError("Connection failed")

    result = get_exchange_rate("USD", "RUB", 1)
    assert result is None


# Тест с нулевой суммой
def test_zero_amount():
    # Проверяем, что при нулевой сумме результат тоже 0
    assert get_exchange_rate("USD", "RUB", 0) == 0.0


# Тест с некорректными валютными кодами
def test_invalid_currency():
    # Проверяем обработку некорректных кодов валют
    assert get_exchange_rate("XXX", "RUB", 1) is None
    assert get_exchange_rate("USD", "YYY", 1) is None


if __name__ == '__main__':
    # Для запуска тестов выполните: pytest test_exchange_rate.py
    pass
