"""
Модели данных
"""
from pydantic import BaseModel
from typing import Dict, Optional, List


class DiscountSettings(BaseModel):
    """Настройки скидок для маркеров"""
    k2: int = 30
    k3: int = 40
    l3: int = 50
    # К4 - особый маркер, цена не пересчитывается


class ProcessingOptions(BaseModel):
    """Опции обработки файла"""
    recalculate_existing: bool = False  # Пересчитывать существующие спец. цены
    markers: DiscountSettings = DiscountSettings()


class ProcessingResult(BaseModel):
    """Результат обработки файла"""
    success: bool
    message: str
    output_filename: Optional[str] = None
    rows_processed: int = 0
    rows_with_sale: int = 0
