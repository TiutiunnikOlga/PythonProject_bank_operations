import unittest
import json
from src.services import filter_person_transfers

class TestFilterPersonTransfers(unittest.TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.test_data = [
            {
                "Категория": "Переводы",
                "Описание": "Иванов И."
            },
            {
                "Категория": "Переводы",
                "Описание": "Петрова А."
            },
            {
                "Категория": "Платежи",
                "Описание": "Оплата ЖКХ"
            },
            {
                "Категория": "Переводы",
                "Описание": "Сидоров П."
            },
            {
                "Категория": "Переводы",
                "Описание": "12345"
            }
        ]

    def test_filter_person_transfers(self):
        # Проверяем корректность фильтрации
        result = json.loads(filter_person_transfers(self.test_data))
        expected = {
            "Переводы физическим лицам": [
                {
                    "Категория": "Переводы",
                    "Описание": "Иванов И."
                },
                {
                    "Категория": "Переводы",
                    "Описание": "Петрова А."
                },
                {
                    "Категория": "Переводы",
                    "Описание": "Сидоров П."
                }
            ]
        }
        self.assertEqual(result, expected)

    def test_empty_data(self):
        # Проверяем обработку пустого списка
        result = json.loads(filter_person_transfers([]))
        expected = {"Переводы физическим лицам": []}
        self.assertEqual(result, expected)

    def test_incorrect_format(self):
        # Проверяем обработку некорректных данных
        incorrect_data = [
            "строка",
            123,
            {"некорректный": "словарь"}
        ]
        result = json.loads(filter_person_transfers(incorrect_data))
        expected = {"Переводы физическим лицам": []}
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
