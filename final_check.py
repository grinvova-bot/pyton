import pandas as pd

df = pd.read_excel('c:/Users/Grintsov/Pyton/price_standard/output/test_result.xlsx')

print("=== Уникальные статусы в результате ===")
status_col = df.iloc[:, 1]
print(status_col.value_counts().to_string())

print("\n=== Строки где статус не пуст и не РАСПРОДАЖА ===")
non_empty = df[(status_col.notna()) & (status_col != '') & (status_col != 'РАСПРОДАЖА')]
print(f"Количество: {len(non_empty)}")
if len(non_empty) > 0:
    print(non_empty.head(10).to_string())

print("\n=== Примеры строк с РАСПРОДАЖА ===")
sale_rows = df[status_col == 'РАСПРОДАЖА']
print(f"Всего: {len(sale_rows)}")
print(sale_rows.head(10).to_string())
