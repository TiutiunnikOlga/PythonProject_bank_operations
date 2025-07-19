import pandas as pd
import json
import unittest
from unittest.mock import patch
from src.services import filter_person_transfers


class TestFilterPersonTransfers(unittest.TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.data = pd.DataFrame(
            {
                "Категория": ["Переводы", "Переводы", "Переводы", "Оплата"],
                "Описание": ["Иванов И.", "Петрова А.", "Сидоров", "Оплата услуг"],
            }
        )

    def test_correct_names(self):
        # Создаем временный Excel файл для теста
        with patch("pandas.read_excel") as mock_read:
            mock_read.return_value = self.data
            result = filter_person_transfers("test_file.xlsx")
            expected = {"Переводы физическим лицам": ["Иванов И.", "Петрова А."]}
            self.assertEqual(json.loads(result), expected)

    def test_incorrect_names(self):
        # Тестируем некорректные имена
        with patch("pandas.read_excel") as mock_read:
            mock_read.return_value = pd.DataFrame({"Категория": ["Переводы"], "Описание": ["Иванов Иван Иванович"]})
            result = filter_person_transfers("test_file.xlsx")
            expected = {"Переводы физическим лицам": []}
            self.assertEqual(json.loads(result), expected)

    def test_missing_columns(self):
        # Тестируем отсутствие необходимых столбцов
        with patch("pandas.read_excel") as mock_read:
            mock_read.return_value = pd.DataFrame({"Категория": ["Переводы"], "Неправильное_описание": ["Иванов И."]})
            result = filter_person_transfers("test_file.xlsx")
            expected = {"Переводы физическим лицам": []}
            self.assertEqual(json.loads(result), expected)

    def test_empty_file(self):
        # Тестируем пустой файл
        with patch("pandas.read_excel") as mock_read:
            mock_read.return_value = pd.DataFrame()
            result = filter_person_transfers("test_file.xlsx")
            expected = {"Переводы физическим лицам": []}
            self.assertEqual(json.loads(result), expected)

    def test_non_existent_file(self):
        # Тестируем несуществующий файл
        with self.assertRaises(FileNotFoundError):
            filter_person_transfers("non_existent_file.xlsx")


if __name__ == "__main__":
    unittest.main()
