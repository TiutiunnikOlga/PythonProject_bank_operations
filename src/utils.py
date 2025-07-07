import os
from typing import Optional
import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_exchange_rate(from_currency: str, to_currency: str, amount: float) -> Optional[float]:
    # Формируем правильную валютную пару
    pair = f"{from_currency}{to_currency}"

    url = f"https://currate.ru/api/?get=rates&pairs={pair}&key={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        if data.get("status") == 200:
            rates = data.get("data", {})
            rate = rates.get(pair)
            if rate:
                return float(rate) * amount
            else:
                raise ValueError(f"Валютная пара {pair} не найдена в ответе")
        else:
            raise ValueError(f"Ошибка API: {data.get('message', 'Неизвестная ошибка')}")

    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Ошибка обработки данных: {e}")
        return None
    except Exception as e:
        print(f"Произошла неизвестная ошибка: {e}")
        return None


if __name__ == "__main__":
    try:
        # Получаем курсы для разных сумм
        usd_rate = get_exchange_rate("USD", "RUB", 1)
        print(f"Курс USD/RUB: {usd_rate}")

        eur_rate = get_exchange_rate("EUR", "RUB", 1)
        print(f"Курс EUR/RUB: {eur_rate}")

        # Пример с другой суммой
        eur_100 = get_exchange_rate("EUR", "RUB", 100)
        print(f"Курс EUR/RUB для 100 евро: {eur_100}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
