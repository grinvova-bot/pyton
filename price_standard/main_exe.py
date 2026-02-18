"""
Точка входа для exe-версии приложения
"""
import sys
import os

# Добавляем текущую директорию в путь
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

os.chdir(application_path)

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("=" * 60)
    print("Прайс-Стандарт - SaaS-сервис обработки прайс-листов")
    print("=" * 60)
    print()
    print("Запуск веб-сервера...")
    print()
    print("Откройте в браузере: http://localhost:8000")
    print("Для остановки нажмите Ctrl+C")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
