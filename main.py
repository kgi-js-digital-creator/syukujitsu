import requests
import csv
import json
import datetime
from io import StringIO

def main():
    url = "https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv"
    response = requests.get(url)
    response.encoding = 'shift_jis'
    
    f = StringIO(response.text)
    reader = csv.reader(f)
    
    next(reader, None)
    
    body_data = {}
    for row in reader:
        if len(row) >= 2:
            try:
                dt = datetime.datetime.strptime(row[0], "%Y/%m/%d")
                day_formatted = dt.strftime("%Y-%m-%d")
                body_data[day_formatted] = row[1]
            except ValueError:
                pass
            
    update_date = datetime.datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%z")
    
    result = {
        "update-date": update_date,
        "body": body_data
    }
            
    with open("syukujitsu.json", "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
