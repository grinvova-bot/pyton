"""
Тестирование ядра обработки с отладкой
"""
import sys
sys.path.insert(0, 'C:/Users/Grintsov/Pyton/price_standard')

import pandas as pd
from app.services.cleaner import DataCleaner
from app.services.transformer import DataTransformer
from app.core.config import STATUS_MAPPING

# Чтение тестового файла
print("Чтение файла...")
df_raw = pd.read_excel("C:/Users/Grintsov/Pyton/Griin/Data.xlsx", header=None)

# Очистка
print("Очистка данных...")
cleaner = DataCleaner(df_raw)
df_cleaned = cleaner.clean()
print(f"Размер после очистки: {df_cleaned.shape}")

# Найдем строку 173 (индекс 173) в очищенных данных
print("\n=== Строка 173 в очищенных данных ===")
if 173 < len(df_cleaned):
    row = df_cleaned.iloc[173]
    print(f"Статус: '{row.iloc[1]}'")
    print(f"Статус lower: '{str(row.iloc[1]).lower()}'")
    
    # Проверка маппинга
    status_lower = str(row.iloc[1]).lower().strip()
    for key, value in STATUS_MAPPING.items():
        if key in status_lower:
            print(f"Найдено совпадение: '{key}' -> '{value}'")
            break
    else:
        print("Нет совпадений в маппинге!")

# Трансформация
print("\nТрансформация...")
column_mapping = {
    'code': 0,
    'status': 1,
    'name': 2,
    'special_price': 3,
    'retail_price': 4,
}

discount_settings = {"К2": 30, "К3": 40, "Л3": 50}

transformer = DataTransformer(df_cleaned, discount_settings)
df_transformed = transformer.transform(
    status_col=column_mapping['status'],
    name_col=column_mapping['name'],
    special_price_col=column_mapping['special_price'],
    retail_price_col=column_mapping['retail_price'],
    recalculate_existing=False
)

print(f"Размер после трансформации: {df_transformed.shape}")

# Проверка строки 173 после трансформации
print("\n=== Строка 173 после трансформации ===")
if 173 < len(df_transformed):
    row = df_transformed.iloc[173]
    print(f"Статус: '{row.iloc[1]}'")
    print(f"Спец.цена: {row.iloc[3]}")
    print(f"Розничная цена: {row.iloc[4]}")
    print(f"Номенклатура: {row.iloc[2]}")
