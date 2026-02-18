import sys
sys.path.insert(0, 'C:/Users/Grintsov/Pyton/price_standard')

from app.core.config import STATUS_MAPPING

# Тест маппинга
test_statuses = ["Ограничено годен", "ограничено годен", "Новый", "новый", "РАСПРОДАЖА"]

print("=== Тест маппинга ===")
for status in test_statuses:
    status_lower = status.lower().strip()
    result = None
    for key, value in STATUS_MAPPING.items():
        if key in status_lower:
            result = value
            break
    if result is None:
        result = status
    print(f"'{status}' -> '{status_lower}' -> '{result}'")
