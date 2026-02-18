"""
FastAPI приложение для обработки прайс-листов
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import os

from app.core.config import UPLOAD_DIR, OUTPUT_DIR, DEFAULT_MARKERS
from app.services.processor import process_file

app = FastAPI(
    title="Прайс-Стандарт",
    description="SaaS-сервис автоматической обработки и стандартизации прайс-листов",
    version="1.0.0"
)

# CORS для локальной разработки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Директории
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Создаем директории
STATIC_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

# Монтируем статику
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Шаблоны
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Главная страница"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "default_markers": DEFAULT_MARKERS,
        }
    )


@app.post("/process")
async def process_price_list(
    file: UploadFile = File(...),
    k2_discount: int = Form(default=30),
    k3_discount: int = Form(default=40),
    recalculate_existing: bool = Form(default=False),
):
    """
    Обработка прайс-листа
    
    Args:
        file: Загружаемый Excel-файл
        k2_discount: Скидка для маркера К2 (%)
        k3_discount: Скидка для маркера К3 (%)
        recalculate_existing: Пересчитывать существующие спец. цены
    """
    # Проверка типа файла
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Разрешены только файлы .xlsx или .xls")
    
    # Сохранение загруженного файла
    file_path = UPLOAD_DIR / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Настройки скидок
        discount_settings = {
            "К2": k2_discount,
            "К3": k3_discount,
        }
        
        # Обработка
        success, message, output_filename = process_file(
            str(file_path),
            discount_settings,
            recalculate_existing
        )
        
        if not success:
            raise HTTPException(status_code=400, detail=message)
        
        return {
            "success": True,
            "message": message,
            "output_filename": output_filename,
            "download_url": f"/download/{output_filename}",
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки: {str(e)}")
    finally:
        # Удаляем загруженный файл
        if file_path.exists():
            file_path.unlink()


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Скачивание обработанного файла"""
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.get("/health")
async def health_check():
    """Проверка работоспособности"""
    return {"status": "ok", "service": "Прайс-Стандарт"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
