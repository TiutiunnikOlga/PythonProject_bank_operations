from utils import get_exchange_rate
from views import cashback, current_date_time, get_sp500_prices, get_top_transactions, number_card, sorted_df_by_date,
                   sum_operations
  

def main():
    # Программа здоровается исходя из времени суток
    current_hour = current_date_time.hour
    if 6 < current_hour < 12:
        greeting = "Доброе утро!"
    elif 12 <= current_hour <= 17:
        greeting = "Добрый день!"
    elif 18 <= current_hour <= 22:
        greeting = "Добрый вечер!"
    else:
        greeting = "Доброй ночи!"

    print(greeting)

    try:
        # Читаем и обрабатываем данные
        df = sorted_df_by_date(r"C:\Users\Olga\PycharmProjects\PythonProject\data\operations.xlsx")

        if df is not None:
            print("Уникальные номера карт:", number_card(df))
            print("Общая сумма операций:", sum_operations(df))
            print("Кэшбэк:", cashback(df))
            print("Топ-5 транзакций:", get_top_transactions(df))
            print("Курс валют EUR/RUB", get_exchange_rate("EUR", "RUB", 1))
            print("Курс валют USD/RUB", get_exchange_rate("USD", "RUB", 1))
            print("Стоимость акций из S&P500", get_sp500_prices())

        else:
            print("Не удалось получить данные")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
