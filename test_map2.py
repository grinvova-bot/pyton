import sys
sys.path.insert(0, 'C:/Users/Grintsov/Pyton/price_standard')

from app.core.config import STATUS_MAPPING
from app.core.utils import clean_text

# Тестовые значения из файла
test_values = [
    "Ограничено годен",
    "ограничено годен",
    "  Ограничено годен  ",
]

print("=== Тест маппинга ===")
print(f"STATUS_MAPPING ключи: {list(STATUS_MAPPING.keys())}")

for val in test_values:
    cleaned = clean_text(val)
    lowered = cleaned.lower()
    result = None
    for key, value in STATUS_MAPPING.items():
        if key in lowered:
            result = value
            break
    if result is None:
        result = cleaned
    print(f"'{val}' -> cleaned: '{cleaned}' -> lowered: '{lowered}' -> result: '{result}'")
