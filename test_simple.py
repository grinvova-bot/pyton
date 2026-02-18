"""
Простой тест для отладки
"""
import sys
sys.path.insert(0, 'C:/Users/Grintsov/Pyton/price_standard')

import pandas as pd
from app.services.cleaner import DataCleaner
from app.services.transformer import DataTransformer

# Чтение тестового файла
print("Чтение файла...")
df_raw = pd.read_excel("C:/Users/Grintsov/Pyton/Griin/Data.xlsx", header=None)
print(f"Размер: {df_raw.shape}")
print(f"Первые 5 строк:")
print(df_raw.head().to_string())

# Очистка
print("\nОчистка данных...")
cleaner = DataCleaner(df_raw)
df_cleaned = cleaner.clean()
print(f"Размер после очистки: {df_cleaned.shape}")
print(f"Первые 10 строк:")
print(df_cleaned.head(10).to_string())

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
print(f"Первые 10 строк:")
print(df_transformed.head(10).to_string())

# Проверка статусов
status_counts = df_transformed.iloc[:, 1].value_counts()
print(f"\nСтатусы:")
print(status_counts.to_string())

# Экспорт
print("\nЭкспорт...")
from app.services.exporter import ExcelExporter

exporter = ExcelExporter(df_transformed, column_mapping)
output_path = "C:/Users/Grintsov/Pyton/price_standard/output/test_result.xlsx"
exporter.export(output_path)
print(f"Файл сохранен: {output_path}")
