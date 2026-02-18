"""
Модуль очистки данных (Data Cleaning)
"""
import pandas as pd
import re
from typing import List, Optional


class DataCleaner:
    """Очистка данных от служебной информации"""
    
    # Паттерны для определения строк-шапок и подвалов
    HEADER_FOOTER_PATTERNS = [
        r'^прайс[-\s]?лист',
        r'^параметры\s*:',
        r'^дата\s*отчета',
        r'^ответственный',
        r'^контакт',
        r'^ООО\s*',
        r'^ИП\s*',
        r'^\d{1,2}\.\d{1,2}\.\d{4}',  # Даты
        r'^телефон',
        r'^email',
        r'^e-mail',
        r'^сайт',
    ]
    
    # Паттерны для заголовков разделов (категорий товаров)
    CATEGORY_PATTERNS = [
        r'^\d+[А-Я]+\s*$',  # типа "1ОСНОВНОЙ ТОВАР"
        r'^[A-Z]+\s*$',  # типа "BOSTIK"
        r'^[А-Я]+\s*$',  # типа "КРАСКИ"
        r'^в/д\s*краски',
        r'^\d-акзо\s*нобель',
    ]
    
    # Паттерны дубликатов заголовков таблицы
    DUPLICATE_HEADER_PATTERNS = [
        r'код\s*товара',
        r'номенклатура',
        r'цена',
        r'качество',
        r'распродажа',
    ]
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        
    def remove_empty_rows(self) -> 'DataCleaner':
        """Удаление полностью пустых строк"""
        initial_count = len(self.df)
        self.df = self.df.dropna(how='all')
        removed = initial_count - len(self.df)
        return self
    
    def remove_header_footer(self) -> 'DataCleaner':
        """Удаление шапок и подвалов документа"""
        indices_to_drop = []
        
        for idx, row in self.df.iterrows():
            row_text = ' '.join(str(c) for c in row if c and pd.notna(c)).lower()
            
            for pattern in self.HEADER_FOOTER_PATTERNS:
                if re.search(pattern, row_text):
                    indices_to_drop.append(idx)
                    break
        
        self.df = self.df.drop(indices_to_drop).reset_index(drop=True)
        return self
    
    def remove_category_headers(self) -> 'DataCleaner':
        """
        Удаление заголовков разделов (категорий).
        Строки, содержащие только названия категорий без цены или кода товара.
        """
        indices_to_drop = []
        
        for idx, row in self.df.iterrows():
            # Проверяем, есть ли в строке код товара или цена
            has_code = False
            has_price = False
            
            for cell in row:
                if pd.notna(cell):
                    cell_str = str(cell).strip()
                    # Код товара - обычно цифры
                    if re.match(r'^\d{5,}', cell_str):
                        has_code = True
                    # Цена - число
                    try:
                        float(cell_str.replace(' ', '').replace(',', '.'))
                        has_price = True
                    except ValueError:
                        pass
            
            # Если нет кода и цены, проверяем на категорию
            if not has_code and not has_price:
                row_text = ' '.join(str(c) for c in row if c and pd.notna(c)).upper()
                for pattern in self.CATEGORY_PATTERNS:
                    if re.search(pattern, row_text, re.IGNORECASE):
                        indices_to_drop.append(idx)
                        break
        
        self.df = self.df.drop(indices_to_drop).reset_index(drop=True)
        return self
    
    def remove_duplicate_headers(self) -> 'DataCleaner':
        """Удаление дублирующихся строк заголовков таблицы"""
        indices_to_drop = []
        
        # Первая строка - это заголовок, его не трогаем
        if len(self.df) > 0:
            first_row = self.df.iloc[0]
            first_row_text = ' '.join(str(c) for c in first_row if c and pd.notna(c)).lower()
            
            # Проверяем остальные строки
            for idx in range(1, len(self.df)):
                row = self.df.iloc[idx]
                row_text = ' '.join(str(c) for c in row if c and pd.notna(c)).lower()
                
                # Если строка содержит ключевые слова заголовков
                has_header_words = sum(
                    1 for pattern in self.DUPLICATE_HEADER_PATTERNS 
                    if pattern in row_text
                )
                
                if has_header_words >= 2:  # Если есть хотя бы 2 слова из заголовка
                    indices_to_drop.append(idx)
        
        self.df = self.df.drop(indices_to_drop).reset_index(drop=True)
        return self
    
    def clean(self) -> pd.DataFrame:
        """
        Полный цикл очистки данных.
        Возвращает очищенный DataFrame.
        """
        return (self
                .remove_empty_rows()
                .remove_header_footer()
                .remove_category_headers()
                .remove_duplicate_headers()
                .remove_empty_rows()  # Повторно удаляем пустые строки
                .df)
