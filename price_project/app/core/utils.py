"""
Утилиты
"""
from decimal import Decimal, ROUND_HALF_UP


def round_half_up(value: float) -> int:
    """
    Математическое округление (как Excel ОКРУГЛ).
    Эмулирует поведение Excel ROUND_HALF_UP вместо banker's rounding в Python.
    """
    if value is None or value == 0:
        return 0
    d = Decimal(str(value))
    return int(d.quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def clean_text(text) -> str:
    """
    Очистка текста: удаление лишних пробелов, приведение к строке.
    """
    if text is None:
        return ""
    return str(text).strip()


def parse_price(value) -> float:
    """
    Парсинг цены из различных форматов.
    """
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    try:
        # Удаляем пробелы и символы валют
        cleaned = str(value).replace(' ', '').replace('₽', '').replace('руб', '').replace(',', '.')
        return float(cleaned)
    except (ValueError, TypeError):
        return 0.0
