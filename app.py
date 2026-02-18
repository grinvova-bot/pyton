from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import pandas as pd
import os
import tempfile
from datetime import datetime
import io
import traceback

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
app.secret_key = 'griin_pricelist_secret_key_2026'


def process_pricelist(template_path):
    """Обработка прайс-листа по логике:
    1. Если есть Спец.цены Акция в новом прайсе -> берём её
    2. Иначе если в названии К2 или К3 -> Розничная цена - 30%
    3. Иначе -> берём розничную цену
    """
    # Читаем листы
    xl = pd.ExcelFile(template_path)
    sheet_names = xl.sheet_names
    
    if len(sheet_names) < 3:
        raise ValueError(f"Ожидалось 3 листа, найдено: {len(sheet_names)}")
    
    # Лист 1 - шаблон для печати
    df_template = pd.read_excel(template_path, sheet_name=sheet_names[0], header=None)
    
    # Лист 3 - новые цены (сырые данные для поиска заголовка)
    df_new_raw = pd.read_excel(template_path, sheet_name=sheet_names[2], header=None)
    
    # Находим строку с заголовком "ФРС Спец.цены Акция"
    header_row_new = None
    for idx in range(len(df_new_raw)):
        cell_val = str(df_new_raw.iloc[idx, 3]) if pd.notna(df_new_raw.iloc[idx, 3]) else ''
        if 'ФРС' in cell_val and 'Спец' in cell_val:
            header_row_new = idx
            break
    
    if header_row_new is None:
        header_row_new = 5  # fallback
    
    # Читаем данные с найденным заголовком
    df_new_data = pd.read_excel(
        template_path, 
        sheet_name=sheet_names[2], 
        header=header_row_new
    )
    
    # Создаём словарь для быстрого поиска по коду товара
    prices_dict = {}
    for idx, row in df_new_data.iterrows():
        code_raw = row.iloc[0] if len(row) > 0 else None
        code_str = str(code_raw).strip() if pd.notna(code_raw) else ''
        
        # Пропускаем если не код товара (должен начинаться с цифры)
        if not code_str or not code_str[0].isdigit():
            continue
        
        code = code_str.split()[0]  # Берём только первую часть (код)
        
        # Столбцы: 0=Код товара, 1=Качество, 2=Номенклатура, 3=Цена (Спец), 4=Цена (Розничная)
        special_price = row.iloc[3] if len(row) > 3 and pd.notna(row.iloc[3]) else None
        retail_price = row.iloc[4] if len(row) > 4 and pd.notna(row.iloc[4]) else None
        name = str(row.iloc[2]) if len(row) > 2 and pd.notna(row.iloc[2]) else ''
        
        prices_dict[code] = {
            'special': special_price,
            'retail': retail_price,
            'name': name
        }
    
    # Находим заголовок в Листе 1
    header_row_template = None
    for idx in range(len(df_template)):
        if pd.notna(df_template.iloc[idx, 0]) and 'Код товара' in str(df_template.iloc[idx, 0]):
            header_row_template = idx
            break
    
    if header_row_template is None:
        header_row_template = 5  # fallback
    
    # Создаём результат - копию шаблона
    df_result = df_template.copy()
    
    # Статистика
    stats = {'updated': 0, 'special': 0, 'k2k3': 0, 'retail': 0}
    
    # Обрабатываем строки с товарами (после заголовка)
    for idx in range(header_row_template + 1, len(df_result)):
        code_raw = df_result.iloc[idx, 0]
        code = str(code_raw).strip().split()[0] if pd.notna(code_raw) else None
        
        # Пропускаем заголовки категорий и пустые строки
        if not code or len(code) < 4 or not code[0].isdigit():
            continue
        
        # Ищем в новых ценах
        if code in prices_dict:
            price_info = prices_dict[code]
            
            # Логика заполнения
            if price_info['special'] is not None and price_info['special'] > 0:
                # Есть спец.цена - берём её
                df_result.iloc[idx, 3] = price_info['special']
                df_result.iloc[idx, 4] = price_info['retail']
                stats['special'] += 1
                stats['updated'] += 1
            else:
                # Нет спец.цены - проверяем на К2/К3 в названии
                name = price_info['name']
                retail = price_info['retail']
                
                if retail is not None and retail > 0 and ('К2' in name or 'К3' in name):
                    # Скидка 30%
                    discounted = round(retail * 0.7, 2)
                    df_result.iloc[idx, 3] = discounted
                    df_result.iloc[idx, 4] = retail
                    stats['k2k3'] += 1
                    stats['updated'] += 1
                elif retail is not None and retail > 0:
                    # Просто розничная цена
                    df_result.iloc[idx, 4] = retail
                    stats['retail'] += 1
                    stats['updated'] += 1
    
    return df_result, sheet_names[0], stats


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Нет файла', 400
        
        file = request.files['file']
        if file.filename == '':
            return 'Файл не выбран', 400
        
        if not file.filename.endswith('.xlsx'):
            return 'Только Excel файлы (.xlsx)', 400
        
        # Сохраняем во временный файл
        temp_dir = tempfile.gettempdir()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{file.filename}"
        filepath = os.path.join(temp_dir, filename)
        file.save(filepath)
        
        try:
            # Обрабатываем
            df_result, sheet_name, stats = process_pricelist(filepath)
            
            # Создаём выходной файл
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_result.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
            
            output.seek(0)
            
            # Генерируем имя выходного файла
            date_str = datetime.now().strftime('%d_%m_%Y')
            out_filename = f'pricelist_{date_str}.xlsx'
            
            # Логируем статистику
            print(f"Обработка завершена: {stats}")
            
            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=out_filename
            )
            
        except Exception as e:
            error_msg = f'Ошибка обработки: {str(e)}\n{traceback.format_exc()}'
            print(error_msg)
            return error_msg, 500
        
        finally:
            # Удаляем загруженный файл
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except:
                pass
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
