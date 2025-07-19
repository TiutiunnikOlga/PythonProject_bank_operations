import pandas as pd
import logging
from datetime import datetime, timedelta
from typing import Optional, Callable
import json
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Путь к файлу с операциями
OPERATIONS_FILE = r"C:\Users\Olga\PycharmProjects\PythonProject\data\operations.xlsx"

# Директория для сохранения отчетов
REPORT_FOLDER = r"C:\Users\Olga\PycharmProjects\PythonProject\folder"  # Можно указать абсолютный путь

# Создаем директорию, если её не существует
if not os.path.exists(REPORT_FOLDER):
    os.makedirs(REPORT_FOLDER)


# Декоратор для записи отчетов
def report_saver(filename: str = None):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            # Получаем результат функции
            result = func(*args, **kwargs)

            # Проверяем, что результат не пустой
            if result.empty:
                logging.warning("Результат отчета пуст, сохранение пропущено")
                return result

            # Формируем имя файла
            if filename is None:
                report_name = f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            else:
                report_name = filename

            # Формируем полный путь к файлу
            full_path = os.path.join(REPORT_FOLDER, report_name)

            # Преобразуем Timestamp в строки
            try:
                # Конвертируем столбец с датами в строки
                result["Дата операции"] = result["Дата операции"].dt.strftime("%Y-%m-%d %H:%M:%S")

                # Записываем результат в файл
                with open(full_path, "w", encoding="utf-8") as f:
                    json.dump(result.to_dict(orient="records"), f, ensure_ascii=False, indent=4)
                logging.info(f"Отчет успешно сохранен в файл: {full_path}")
            except Exception as e:
                logging.error(f"Ошибка при сохранении отчета: {str(e)}")

            return result

        return wrapper

    return decorator


@report_saver()  # Декоратор без параметра
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    # Загружаем данные, если DataFrame не передан
    if transactions.empty:
        try:
            transactions = pd.read_excel(OPERATIONS_FILE)
        except Exception as e:
            logging.error(f"Ошибка при загрузке данных: {str(e)}")
            return pd.DataFrame()

    # Проверяем наличие необходимых столбцов
    required_columns = ["Дата операции", "Категория", "Сумма операции"]
    if not all(col in transactions.columns for col in required_columns):
        logging.error("Отсутствуют необходимые столбцы в DataFrame")
        return pd.DataFrame()

    # Преобразуем даты
    try:
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    except Exception as e:
        logging.error(f"Ошибка при преобразовании дат: {str(e)}")
        return pd.DataFrame()

    # Устанавливаем дату для расчета
    if date:
        try:
            end_date = pd.to_datetime(date)
        except ValueError:
            logging.error("Неверный формат даты")
            return pd.DataFrame()
    else:
        end_date = datetime.now()

    # Рассчитываем период
    start_date = end_date - timedelta(days=90)

    # Фильтруем данные
    filtered_df = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
    ]

    # Проверяем, есть ли данные после фильтрации
    if filtered_df.empty:
        logging.warning(f"Нет данных по категории {category} за указанный период")
        return pd.DataFrame()

    # Формируем итоговый отчет
    result = (
        filtered_df.groupby(["Категория", "Дата операции"]).agg(total_amount=("Сумма операции", "sum")).reset_index()
    )

    return result


# Пример использования
if __name__ == "__main__":
    # Загружаем данные один раз
    try:
        df = pd.read_excel(OPERATIONS_FILE)
    except Exception as e:
        logging.error(f"Ошибка при загрузке данных: {str(e)}")
        df = pd.DataFrame()

    # Получаем отчет
    report = spending_by_category(df, "Супермаркеты")
    print(report)
