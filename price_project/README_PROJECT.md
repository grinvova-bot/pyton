# Прайс-лист ООО "АЛЬТ-ИКС" - Рабочий проект

## Структура проекта

```
price_project/
├── app/                        # Ядро приложения
│   ├── core/                   # Конфигурация и утилиты
│   │   ├── config.py           # Настройки (маркеры, маппинг статусов)
│   │   └── utils.py            # Утилиты (округление, парсинг цен)
│   ├── services/               # Бизнес-логика
│   │   ├── parser.py           # Парсинг Excel
│   │   ├── cleaner.py          # Очистка данных
│   │   ├── transformer.py      # Трансформация статусов, расчёт цен
│   │   ├── exporter.py         # Экспорт с оформлением
│   │   └── processor.py        # Основной процессор
│   └── main.py                 # FastAPI приложение
├── templates/                  # HTML шаблоны
│   └── index.html
├── templates_excel/            # Excel шаблоны
│   ├── Temlate.xlsx
│   └── Temlate2-color.xlsx
├── data/                       # Тестовые данные
│   └── Data.xlsx
├── cli.py                      # Консольный интерфейс
├── main_exe.py                 # Точка входа для EXE
├── requirements.txt            # Зависимости
└── README.md                   # Документация
```

## Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Запуск веб-версии
```bash
python app/main.py
# или
uvicorn app.main:app --reload
```

### 3. Запуск консольной версии
```bash
python cli.py --input data/Data.xlsx --output result.xlsx
```

### 4. Сборка EXE
```bash
pyinstaller main_exe.spec
```

## Тестирование
```bash
python cli.py --input data/Data.xlsx --output test_result.xlsx
```

## Требования
- Python 3.8+
- pandas
- openpyxl
- fastapi
- uvicorn
