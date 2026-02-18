"""
Модуль трансформации данных
Нормализация статусов и расчёт специальных цен
"""
import pandas as pd
import re
from typing import Dict, Optional, Tuple
from app.core.utils import round_half_up, clean_text, parse_price
from app.core.config import STATUS_MAPPING


class DataTransformer:
    """Трансформация данных: нормализация статусов и расчёт цен"""
    
    # Паттерны маркеров
    MARKER_PATTERNS = {
        'К2': r'[Кк][2]',
        'К3': r'[Кк][3]',
        'К4': r'[Кк][4]',
    }
    
    def __init__(self, df: pd.DataFrame, discount_settings: Dict[str, int]):
        """
        Инициализация трансформера.
        
        Args:
            df: DataFrame с данными
            discount_settings: Словарь {маркер: процент_скидки}
        """
        self.df = df.copy()
        self.discount_settings = discount_settings
        
    def _find_marker(self, text: str) -> Optional[str]:
        """
        Поиск маркера в тексте.
        Возвращает название маркера или None.
        """
        if not text:
            return None
        
        text = str(text)
        for marker, pattern in self.MARKER_PATTERNS.items():
            if re.search(pattern, text):
                return marker
        return None
    
    def _normalize_status(self, status: str) -> str:
        """
        Нормализация статуса товара.
        """
        if not status:
            return ""
        
        status_lower = str(status).lower().strip()
        
        # Проверяем маппинг
        for key, value in STATUS_MAPPING.items():
            if key in status_lower:
                return value
        
        # Если не найдено совпадений - возвращаем как есть
        return status
    
    def normalize_statuses(self, status_col: int) -> 'DataTransformer':
        """
        Нормализация всех статусов в колонке.
        
        "Новый", "new", "новинка" -> "" (пусто)
        "Ограничено годен", "брак", "уценка" -> "РАСПРОДАЖА"
        "Распродажа", "sale", "акция" -> "РАСПРОДАЖА"
        """
        if status_col >= len(self.df.columns):
            return self
        
        def transform_status(val):
            if pd.isna(val) or val is None:
                return ""
            return self._normalize_status(str(val))
        
        self.df.iloc[:, status_col] = self.df.iloc[:, status_col].apply(transform_status)
        return self
    
    def calculate_special_prices(
        self,
        name_col: int,
        status_col: int,
        special_price_col: int,
        retail_price_col: int,
        recalculate_existing: bool = False
    ) -> 'DataTransformer':
        """
        Расчёт специальных цен с учётом маркеров.
        
        Алгоритм:
        1. Если маркер К4 и спец. цена есть -> не пересчитываем
        2. Если маркер К2/К3/Л3 -> считаем по формуле
        """
        if any(col >= len(self.df.columns) for col in [name_col, status_col, special_price_col, retail_price_col]):
            return self
        
        for idx in range(len(self.df)):
            row = self.df.iloc[idx]
            
            # Получаем значения
            name = clean_text(row.iloc[name_col] if name_col < len(row) else None)
            status = clean_text(row.iloc[status_col] if status_col < len(row) else None)
            special_price = parse_price(row.iloc[special_price_col] if special_price_col < len(row) else None)
            retail_price = parse_price(row.iloc[retail_price_col] if retail_price_col < len(row) else None)
            
            # Ищем маркер в названии и статусе
            combined_text = f"{name} {status}"
            marker = self._find_marker(combined_text)
            
            if not marker:
                continue
            
            # Проверяем, есть ли уже спец. цена
            has_special_price = special_price > 0
            
            # Логика для К4 (исключение)
            if marker == 'К4':
                if has_special_price:
                    # Не пересчитываем, оставляем как есть
                    # Только устанавливаем статус РАСПРОДАЖА
                    self.df.iloc[idx, status_col] = "РАСПРОДАЖА"
                else:
                    # Если цены нет, все равно ставим РАСПРОДАЖА
                    # (товар с К4 но без цены - тоже распродажа)
                    self.df.iloc[idx, status_col] = "РАСПРОДАЖА"
                continue
            
            # Логика для остальных маркеров (К2, К3, Л3)
            if marker in self.discount_settings:
                discount = self.discount_settings[marker]
                
                # Если цены нет или настроен пересчёт
                if not has_special_price or recalculate_existing:
                    if retail_price > 0:
                        # Формула: Спец.цена = ОКРУГЛ(Розничная × (1 - P/100); 0)
                        new_price = round_half_up(retail_price * (1 - discount / 100))
                        self.df.iloc[idx, special_price_col] = new_price
                        self.df.iloc[idx, status_col] = "РАСПРОДАЖА"
        
        return self
    
    def transform(self, 
                  status_col: int,
                  name_col: int, 
                  special_price_col: int, 
                  retail_price_col: int,
                  recalculate_existing: bool = False) -> pd.DataFrame:
        """
        Полный цикл трансформации.
        
        Args:
            status_col: индекс колонки статуса
            name_col: индекс колонки номенклатуры
            special_price_col: индекс колонки спец. цены
            retail_price_col: индекс колонки розничной цены
            recalculate_existing: пересчитывать ли существующие спец. цены
        """
        return (self
                .normalize_statuses(status_col)
                .calculate_special_prices(
                    name_col=name_col,
                    status_col=status_col,
                    special_price_col=special_price_col,
                    retail_price_col=retail_price_col,
                    recalculate_existing=recalculate_existing
                )
                .df)
