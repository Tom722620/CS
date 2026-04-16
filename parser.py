import requests
import json
import sys
import os
import time

def main():
    if len(sys.argv) < 3:
        print("Ошибка: Нужно передать start и count. Пример: python parser.py 0 500")
        return

    start_index = int(sys.argv[1])
    count = int(sys.argv[2])
    output_filename = f"result_{start_index}.json"

    # 1. Сразу создаем файл, чтобы шаг Upload Artifact не ругался
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump([], f)

    # 2. Проверяем наличие входного файла
    if not os.path.exists("item_ids.json"):
        print("ОШИБКА: Файл item_ids.json не найден в корне репозитория!")
        return

    try:
        with open("item_ids.json", "r", encoding="utf-8") as f:
            all_ids = json.load(f)
    except Exception as e:
        print(f"ОШИБКА при чтении JSON: {e}")
        return

    chunk = all_ids[start_index : start_index + count]
    if not chunk:
        print(f"Предупреждение: Кусок списка [{start_index}:{start_index+count}] пуст.")
        return

    print(f"Начинаем парсинг куска: {start_index} - {start_index + len(chunk)}")
    results = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for i, item_id in enumerate(chunk):
        url = f"https://steamcommunity.com/market/itemordershistogram?country=LV&language=russian&currency=1&item_nameid={item_id}&two_factor=0"
        
        try:
            print(f"[{i+1}/{len(chunk)}] Запрос ID: {item_id}")
            resp = requests.get(url, headers=headers, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                results.append({
                    "id": item_id,
                    "sell": data.get("lowest_sell_order"),
                    "buy": data.get("highest_buy_order")
                })
            elif resp.status_code == 429:
                print("БАН ПО IP (429). Останавливаемся.")
                break
            else:
                print(f"Ошибка {resp.status_code} для ID {item_id}")
        except Exception as e:
            print(f"Ошибка на ID {item_id}: {e}")

        # Пауза, чтобы не забанили
        time.sleep(1.5)

    # 3. Перезаписываем файл уже с данными
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Готово! Данные сохранены в {output_filename}")

if __name__ == "__main__":
    main()
