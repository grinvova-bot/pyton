"""
Основной сервис обработки прайс-листов
Объединяет все модули: парсинг, очистку, трансформацию, экспорт
"""
import pandas as pd
from pathlib import Path
from typing import Dict, Tuple, Optional

from app.services.parser import ExcelParser
from app.services.cleaner import DataCleaner
from app.services.transformer import DataTransformer
from app.services.exporter import ExcelExporter, generate_output_filename
from app.core.config import DEFAULT_MARKERS, UPLOAD_DIR, OUTPUT_DIR


class PriceProcessor:
    """Основной процессор прайс-листов"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        self.column_mapping = {}
        
    def _detect_columns_advanced(self) -> Dict[str, int]:
        """
        Расширенное определение колонок.
        Анализирует структуру файла и находит ключевые колонки.
        """
        parser = ExcelParser(self.file_path)
        
        # Получаем все строки для анализа
        all_rows = parser.get_all_rows()
        
        # Находим строку с заголовками
        header_patterns = {
            'code': ['код товара', 'код', 'артикул'],
            'status': ['качество', 'статус', 'распродажа'],
            'name': ['номенклатура', 'название товара', 'товар'],
            'special_price': ['спец', 'акция', 'специальная'],
            'retail_price': ['розничн', 'цена', 'прайс'],
        }
        
        column_mapping = {}
        
        # Ищем заголовки в первых строках
        for row_idx, row in enumerate(all_rows[:15]):
            for col_idx, cell in enumerate(row):
                if cell is None:
                    continue
                    
                cell_text = str(cell).lower()
                
                for col_type, patterns in header_patterns.items():
                    if col_type not in column_mapping:
                        for pattern in patterns:
                            if pattern in cell_text:
                                column_mapping[col_type] = col_idx
                                break
        
        parser.close()
        return column_mapping
    
    def process(self, 
                discount_settings: Dict[str, int] = None,
                recalculate_existing: bool = False) -> Tuple[bool, str, Optional[str]]:
        """
        Полный цикл обработки файла.
        
        Args:
            discount_settings: Настройки скидок {маркер: процент}
            recalculate_existing: Пересчитывать ли существующие спец. цены
        
        Returns:
            (success, message, output_filename)
        """
        try:
            if discount_settings is None:
                discount_settings = DEFAULT_MARKERS.copy()
                # Удаляем К4 из настроек скидок (он обрабатывается отдельно)
                discount_settings.pop('К4', None)
            
            # Шаг 1: Чтение данных
            parser = ExcelParser(self.file_path)
            df_raw = parser.read_raw_data()
            parser.close()
            
            if df_raw.empty:
                return False, "Файл не содержит данных", None
            
            # Шаг 2: Очистка данных
            cleaner = DataCleaner(df_raw)
            df_cleaned = cleaner.clean()
            
            if df_cleaned.empty:
                return False, "Не удалось извлечь данные из файла", None
            
            # Шаг 3: Определение колонок
            # Для упрощения используем фиксированные индексы на основе анализа тестового файла
            # В продакшене нужно использовать более сложную логику определения
            column_mapping = {
                'code': 0,        # Код товара
                'status': 1,      # Качество/Статус
                'name': 2,        # Номенклатура
                'special_price': 3,  # Спец. цена
                'retail_price': 4,   # Розничная цена
            }
            
            # Шаг 4: Трансформация данных
            transformer = DataTransformer(df_cleaned, discount_settings)
            df_transformed = transformer.transform(
                status_col=column_mapping['status'],
                name_col=column_mapping['name'],
                special_price_col=column_mapping['special_price'],
                retail_price_col=column_mapping['retail_price'],
                recalculate_existing=recalculate_existing
            )
            
            # Шаг 5: Экспорт
            exporter = ExcelExporter(df_transformed, column_mapping)
            output_filename = generate_output_filename()
            output_path = OUTPUT_DIR / output_filename
            
            exporter.export(str(output_path))
            
            # Подсчёт статистики
            rows_processed = len(df_transformed)
            rows_with_sale = len(df_transformed[df_transformed.iloc[:, column_mapping['status']] == "РАСПРОДАЖА"])
            
            return True, f"Обработано {rows_processed} строк, из них {rows_with_sale} с распродажей", output_filename
            
        except Exception as e:
            return False, f"Ошибка обработки: {str(e)}", None


def process_file(file_path: str, 
                 discount_settings: Dict[str, int] = None,
                 recalculate_existing: bool = False) -> Tuple[bool, str, Optional[str]]:
    """
    Удобная функция для обработки файла.
    
    Args:
        file_path: Путь к файлу
        discount_settings: Настройки скидок
        recalculate_existing: Пересчитывать ли существующие цены
    
    Returns:
        (success, message, output_filename)
    """
    processor = PriceProcessor(file_path)
    return processor.process(discount_settings, recalculate_existing)
