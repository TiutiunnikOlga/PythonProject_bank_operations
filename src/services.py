import re
import json


def filter_person_transfers(data):
    result = {"Переводы физическим лицам": []}

    for item in data:
        try:
            if item["Категория"] == "Переводы" and \
                    any(char.isalpha() for char in item["Описание"]) and \
                    not item["Описание"].isdigit():
                # Обрабатываем инициалы
                name = item["Описание"].split()
                if len(name) > 1 and all(len(part) <= 2 for part in name[1:]):
                    item["Описание"] = ' '.join([name[0]] + [part[0] + '.' for part in name[1:]])
                result["Переводы физическим лицам"].append(item)
        except (KeyError, TypeError):
            continue

    return json.dumps(result)

if __name__ == "__main__":
    print(filter_person_transfers())
