# 📦 Инструкция по размещению на хостинге

## Вариант 1: Python-хостинг (FastAPI/uvicorn)

### Требования к хостингу
- Python 3.8+ (рекомендуется 3.12)
- Поддержка pip install
- Возможность запуска процессов (не только CGI)
- Доступ к терминалу/SSH (желательно)

---

## 📋 Шаг 1: Подготовка файлов для загрузки

### Создайте архив для хостинга

```bash
cd c:\Users\Grintsov\Pyton\price_project

# Создайте папку для деплоя
mkdir deploy

# Скопируйте только необходимые файлы
xcopy /E /I /Y app deploy\app
xcopy /E /I /Y templates deploy\templates
xcopy /E /I /Y templates_excel deploy\templates_excel
copy main.py deploy\
copy requirements.txt deploy\
copy .env.example deploy\.env  (если есть)
```

### Или используйте готовую структуру:
```
deploy/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── utils.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── services/
│       ├── __init__.py
│       ├── parser.py
│       ├── cleaner.py
│       ├── transformer.py
│       ├── exporter.py
│       └── processor.py
├── templates/
│   └── index.html
├── templates_excel/
│   ├── Temlate.xlsx
│   └── Temlate2-color.xlsx
├── requirements.txt
└── run.py  (точка входа)
```

---

## 📋 Шаг 2: Загрузка на хостинг

### Через FTP/SFTP:
1. Подключитесь к хостингу через FileZilla или WinSCP
2. Загрузите папку `deploy` в директорию сайта (обычно `www` или `public_html`)
3. Переименуйте `deploy` в нужное имя (например, `price`)

### Через панель хостинга:
1. Зайдите в файловый менеджер
2. Создайте папку для приложения
3. Загрузите архив и распакуйте

---

## 📋 Шаг 3: Установка зависимостей

### Через SSH (рекомендуется):
```bash
cd /path/to/your/app
pip install -r requirements.txt --user
```

### Через панель хостинга:
1. Найдите раздел "Python" или "Менеджер приложений"
2. Укажите путь к `requirements.txt`
3. Нажмите "Установить зависимости"

---

## 📋 Шаг 4: Настройка точки входа

### Создайте файл `run.py` в корне приложения:

```python
"""
Точка входа для хостинга
"""
import sys
import os

# Добавляем текущую директорию в путь
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)

from app.main import app

# Для разных хостингов
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 📋 Шаг 5: Настройка веб-сервера

### Для Apache (.htaccess):
Создайте файл `.htaccess` в корне приложения:

```apache
RewriteEngine On
RewriteRule ^$ http://localhost:8000/ [P,L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ http://localhost:8000/$1 [P,L]
```

### Для Nginx:
Добавьте в конфиг nginx:

```nginx
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

### Для PythonAnywhere:
1. Зайдите в раздел "Web"
2. Добавьте новое веб-приложение
3. Выберите "Manual configuration"
4. Укажите:
   - Python version: 3.12
   - Path to your app: `/home/username/price_project`
   - WSGI configuration file

### Для Beget/Timeweb/Reg.ru:
1. Раздел "Python" → "Добавить приложение"
2. Укажите путь: `/path/to/price_project`
3. Команда запуска: `python run.py`
4. Порт: 8000 (или другой свободный)

---

## 📋 Шаг 6: Настройка переменных окружения

### Создайте файл `.env`:
```env
# Порт приложения
PORT=8000

# Хост
HOST=0.0.0.0

# Максимальный размер файла (байты)
MAX_FILE_SIZE=10485760

# Путь к шаблонам
TEMPLATES_DIR=templates
TEMPLATES_EXCEL_DIR=templates_excel

# Режим отладки (False для продакшена)
DEBUG=False
```

---

## 📋 Шаг 7: Проверка работы

### Локальный тест перед загрузкой:
```bash
cd c:\Users\Grintsov\Pyton\price_project
python run.py
```
Откройте http://localhost:8000

### После загрузки:
1. Откройте ваш домен: `https://your-domain.com`
2. Проверьте загрузку страницы
3. Протестируйте загрузку файла

---

## 🔧 Решение проблем

### Ошибка "ModuleNotFoundError"
```bash
# Убедитесь, что все зависимости установлены
pip install -r requirements.txt --user

# Проверьте PYTHONPATH
export PYTHONPATH=/path/to/app:$PYTHONPATH
```

### Ошибка прав доступа
```bash
# Дайте права на папку
chmod -R 755 /path/to/app
chmod -R 777 /path/to/app/uploads
chmod -R 777 /path/to/app/output
```

### Приложение не запускается
Проверьте логи:
```bash
# Для systemd
journalctl -u your-app-name -f

# Для PythonAnywhere
/var/log/username/pythonanywhere.com.log
```

---

## 📊 Специфичные инструкции для хостингов

### PythonAnywhere (бесплатный тариф)
```python
# WSGI-файл: /var/www/username_pythonanywhere_com_wsgi.py
import sys
import os

path = '/home/username/price_project'
if path not in sys.path:
    sys.path.append(path)

from app.main import app as application
```

### Beget.com
1. Панель → Python → Добавить приложение
2. Путь: `/home/username/sites/price`
3. Команда: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
4. Включите приложение

### Timeweb
1. Панель → Python → Новое приложение
2. Выберите директорию
3. Укажите `requirements.txt`
4. Команда: `python run.py`

### Reg.ru (VPS)
```bash
# Установка
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Создание виртуального окружения
cd /var/www/price_project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Запуск через systemd
sudo nano /etc/systemd/system/price.service
```

```ini
[Unit]
Description=Price Standard API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/price_project
ExecStart=/var/www/price_project/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable price
sudo systemctl start price
sudo systemctl status price
```

### Docker (универсальный)
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t price-standard .
docker run -p 8000:8000 price-standard
```

---

## ✅ Чек-лист после установки

- [ ] Страница загружается по домену
- [ ] Форма загрузки файлов отображается
- [ ] Файл загружается без ошибок
- [ ] Обработка проходит успешно
- [ ] Скачивание результата работает
- [ ] Шаблоны Excel доступны
- [ ] Логи пишутся без ошибок

---

## 📞 Поддержка

При проблемах проверьте:
1. Версию Python (`python --version`)
2. Установленные пакеты (`pip list`)
3. Логи приложения
4. Права доступа к папкам
