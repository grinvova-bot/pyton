import requests

# Тест загрузки файла
file_path = r'c:\Users\Grintsov\Pyton\Griin\прайс-лист от 06_02_2026.xlsx'

with open(file_path, 'rb') as f:
    files = {'file': ('test.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    response = requests.post('http://localhost:5000/', files=files)

print(f'Status: {response.status_code}')
print(f'Content-Type: {response.headers.get("Content-Type")}')
print(f'Content-Length: {len(response.content)} bytes')

if response.status_code == 200:
    # Сохраняем результат
    with open(r'c:\Users\Grintsov\Pyton\test_result.xlsx', 'wb') as out:
        out.write(response.content)
    print('OK! Файл сохранён: test_result.xlsx')
else:
    print(f'Error: {response.text[:500]}')
