import datetime
import pandas as pd
import os

# Создаем объект datetime
current_date_time = datetime.datetime.now()


def sorted_df_by_date(df):
    sorted_df = []
    try:
        if not os.path.exists(df):
            raise FileNotFoundError(f"Файл не найден: {df}")

        # Читаем файл Excel
        df = pd.read_excel(df, engine="openpyxl")

        if "Дата операции" in df.columns:
            # Проверяем формат даты в столбце
            try:
                df["Дата операции"] = pd.to_datetime(df["Дата операции"])
                df = df.sort_values(by="Дата операции")
            except ValueError:
                # Пытаемся определить формат даты автоматически
                df["Дата операции"] = pd.to_datetime(df["Дата операции"], infer_datetime_format=True)
            sorted_df = df.sort_values(by="Дата операции")

        return sorted_df
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        return None
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return None


def number_card(df):
    return df["Номер карты"].dropna().unique().tolist()


def sum_operations(df):
    return abs(df["Сумма операции"].sum())


def cashback(df):
    return abs(sum_operations(df) * 0.01)


def get_top_transactions(df):
    return df.nlargest(5, "Сумма операции").to_dict(orient="records")


if __name__ == "__main__":
    print(current_date_time.hour)
    excel_data = pd.read_excel("../data/operations.xlsx")
    print(excel_data.shape)
    print(number_card(excel_data))
    print(sum_operations(excel_data))
    print(cashback(excel_data))
