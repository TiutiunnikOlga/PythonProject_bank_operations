import pandas as pd
import pytest
import json
from datetime import datetime
from src.reports import spending_by_category, report_saver  # Предполагаем, что код находится в файле main.py


# Создаем тестовые данные
@pytest.fixture
def test_transactions():
    data = {
        "Дата операции": [datetime(2025, 7, 1), datetime(2025, 7, 15), datetime(2025, 7, 20), datetime(2025, 7, 25)],
        "Категория": ["Супермаркеты", "Супермаркеты", "Рестораны", "Супермаркеты"],
        "Сумма операции": [1000, 2000, 1500, 3000],
    }
    return pd.DataFrame(data)


# Тест на корректную работу с данными
def test_spending_by_category_valid(test_transactions):
    result = spending_by_category(test_transactions, "Супермаркеты")
    assert not result.empty
    assert len(result) == 2
    assert result["total_amount"].sum() == 3000


# Тест на отсутствие данных по категории
def test_spending_by_category_no_data(test_transactions):
    result = spending_by_category(test_transactions, "Аптеки")
    assert result.empty


# Тест на корректную работу с датой
def test_spending_by_category_with_date(test_transactions):
    result = spending_by_category(test_transactions, "Супермаркеты", date="2025-07-20")
    assert len(result) == 2
    assert result["total_amount"].sum() == 3000


# Тест на отсутствие необходимых столбцов
def test_spending_by_category_missing_columns():
    bad_df = pd.DataFrame({"Дата": [datetime(2025, 7, 1)], "Категория": ["Супермаркеты"], "Сумма": [1000]})
    result = spending_by_category(bad_df, "Супермаркеты")
    assert result.empty


# Тест декоратора с указанием имени файла
def test_report_saver_with_filename(test_transactions, tmpdir):
    filename = tmpdir.join("test_report.json")

    @report_saver(filename=str(filename))
    def test_func():
        return test_transactions

    result = test_func()
    assert result is not None
    assert filename.check()

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) == 4
