import pandas as pd
import json


def filter_person_transfers(df):
    # Читаем Excel файл
    df = pd.read_excel(df)

    result = {"Переводы физическим лицам": []}

    for _, row in df.iterrows():
        try:
            if row["Категория"] == "Переводы" and \
                    any(char.isalpha() for char in row["Описание"]) and \
                    not row["Описание"].isdigit():
                # Обрабатываем инициалы
                name = row["Описание"].split()
                if len(name) > 1 and all(len(part) <= 2 for part in name[1:]):
                    formatted_name = ' '.join([name[0]] + [part[0] + '.' for part in name[1:]])
                    result["Переводы физическим лицам"].append(formatted_name)
        except (KeyError, TypeError):
            continue

    return json.dumps(result, ensure_ascii=False)


if __name__ == "__main__":
    print(filter_person_transfers(r"C:\Users\Olga\PycharmProjects\PythonProject\data\operations.xlsx"))
