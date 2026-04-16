import requests
import json
import sys
import os

def parse_steam(start, count):
    app_id = 252490  # Rust
    url = f"https://steamcommunity.com/market/search/render/?query=&start={start}&count={count}&search_descriptions=0&sort_column=popular&sort_dir=desc&appid={app_id}&norender=1"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        with open(f"data_{start}.json", "w", encoding="utf-8") as f:
            json.dump(data['results'], f, ensure_ascii=False)
        print(f"Successfully parsed {start} to {start+count}")
    else:
        print(f"Error: {response.status_code}")
        sys.exit(1) # Сообщаем GitHub, что задача упала

if __name__ == "__main__":
    start_index = int(sys.argv[1])
    parse_steam(start_index, 100)
