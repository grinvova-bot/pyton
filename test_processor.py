"""
Тестирование ядра обработки на тестовых данных
"""
import sys
sys.path.insert(0, 'C:/Users/Grintsov/Pyton/price_standard')

from app.services.processor import process_file
from app.core.config import DEFAULT_MARKERS

# Тестовый файл
test_file = "C:/Users/Grintsov/Pyton/Griin/Data.xlsx"

print("=== Тестирование обработки прайс-листа ===\n")
print(f"Исходный файл: {test_file}")
print(f"Настройки скидок: {DEFAULT_MARKERS}")
print()

# Обработка
success, message, output_filename = process_file(
    test_file,
    discount_settings={"К2": 30, "К3": 40, "Л3": 50},
    recalculate_existing=False
)

result_status = "OK" if success else "ERROR"
print(f"Результат: [{result_status}]")
print(f"Сообщение: {message}")
print(f"Выходной файл: {output_filename}")

if success and output_filename:
    print(f"\nФайл сохранен: {output_filename}")
    
    # Чтение результата для проверки
    import pandas as pd
    from pathlib import Path
    
    output_path = Path("C:/Users/Grintsov/Pyton/price_standard/output") / output_filename
    if output_path.exists():
        df_result = pd.read_excel(output_path)
        print(f"\n=== Результат (первые 20 строк) ===")
        print(df_result.head(20).to_string())
        
        # Проверка статусов
        if len(df_result.columns) > 1:
            status_col = df_result.columns[1]  # Статус
            sale_count = len(df_result[df_result[status_col] == "РАСПРОДАЖА"])
            print(f"\nСтатистика:")
            print(f"   Всего строк: {len(df_result)}")
            print(f"   Строк с РАСПРОДАЖА: {sale_count}")
