import pandas as pd

df = pd.read_excel('c:/Users/Grintsov/Pyton/Griin/Data.xlsx', header=None)

# Найдем уникальные значения в колонке статуса (индекс 1)
status_values = df.iloc[:, 1].dropna().unique()
print("=== Уникальные статусы ===")
for val in status_values[:30]:
    print(f"'{val}' -> lower: '{str(val).lower().strip()}'")
