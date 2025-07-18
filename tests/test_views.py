import unittest
import pandas as pd
import io
from datetime import datetime
from src.views import number_card, sorted_df_by_date,sum_operations,cashback, get_top_transactions


# Создаем тестовые данные в формате Excel
def create_test_excel():
    # Создаем тестовый DataFrame
    data = {
        'Дата операции': [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3)],
        'Номер карты': ['1234', '5678', '1234'],
        'Сумма операции': [1000, -500, 2000]
    }
    df = pd.DataFrame(data)

    # Создаем Excel файл в памяти
    excel_data = io.BytesIO()
    df.to_excel(excel_data, index=False)
    excel_data.seek(0)
    return excel_data


class TestOperations(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые данные перед каждым тестом
        self.test_excel = create_test_excel()
        self.df = pd.read_excel(self.test_excel)

    def sorted_df_by_date(df):
        try:
            # Убедимся, что столбец с датой имеет правильный формат
            df['Дата операции'] = pd.to_datetime(df['Дата операции'])

            # Сортируем DataFrame по дате
            sorted_df = df.sort_values(by='Дата операции', ascending=True)
            return sorted_df
        except Exception as e:
            print(f"Ошибка при сортировке: {e}")
            return None

    def test_number_card(self):
        # Проверяем получение уникальных номеров карт
        result = number_card(self.df)
        self.assertEqual(result, [1234, 5678])

    def test_sum_operations(self):
        # Проверяем расчет суммы операций
        result = sum_operations(self.df)
        self.assertEqual(result, 2500)  # 1000 + (-500) + 2000 = 2500

    def test_cashback(self):
        # Проверяем расчет кэшбэка
        result = cashback(self.df)
        self.assertEqual(result, 25)  # 2500 * 0.01 = 25

    def test_get_top_transactions(self):
        # Проверяем получение топ транзакций
        self.df.loc[0, 'Сумма операции'] = 5000  # Добавляем большую сумму
        top_transactions = get_top_transactions(self.df)
        self.assertEqual(len(top_transactions), 3)  # У нас всего 3 транзакции
        self.assertEqual(top_transactions[0]['Сумма операции'], 5000)

    def test_file_not_found(self):
        # Проверяем обработку ошибки отсутствия файла
        result = sorted_df_by_date('non_existent_file.xlsx')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

