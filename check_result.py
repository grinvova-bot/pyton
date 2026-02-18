import pandas as pd

# Чтение результата
df_result = pd.read_excel('c:/Users/Grintsov/Pyton/price_standard/output/test_result.xlsx')
print("=== Результат (строки с К4) ===")
for i, row in df_result.iterrows():
    row_str = ' '.join(str(c) for c in row if pd.notna(c))
    if 'К4' in row_str:
        print(f'{i}: {row.tolist()}')

print("\n=== Статусы ===")
print(df_result.iloc[:, 1].value_counts().to_string())

print("\n=== Первые 30 строк ===")
print(df_result.head(30).to_string())
