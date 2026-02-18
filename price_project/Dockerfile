FROM python:3.12-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY app ./app
COPY templates ./templates
COPY templates_excel ./templates_excel
COPY data ./data
COPY run.py .

# Создание директорий для файлов
RUN mkdir -p /app/app/uploads /app/app/output

# Порт приложения
EXPOSE 8000

# Запуск
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
