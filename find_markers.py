import pandas as pd
df = pd.read_excel('c:/Users/Grintsov/Pyton/Griin/Data.xlsx', header=None)
# Найдем строки с маркерами
for i, row in df.iterrows():
    row_str = ' '.join(str(c) for c in row if pd.notna(c))
    if 'К4' in row_str or 'К2' in row_str or 'К3' in row_str or 'Л3' in row_str:
        print(f'{i}: {row.tolist()}')
