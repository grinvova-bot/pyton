import requests

# Тест обработки файла
url = "http://localhost:8000/process"
file_path = "c:/Users/Grintsov/Pyton/Griin/Data.xlsx"

print("Отправка файла на обработку...")

with open(file_path, "rb") as f:
    files = {"file": ("Data.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    data = {
        "k2_discount": 30,
        "k3_discount": 40,
        "l3_discount": 50,
        "recalculate_existing": False
    }
    
    response = requests.post(url, files=files, data=data)
    
print(f"Статус: {response.status_code}")
print(f"Ответ: {response.text}")
