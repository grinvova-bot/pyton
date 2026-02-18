@echo off
REM Скрипт подготовки к деплою на хостинг

echo ============================================
echo Подготовка файлов для деплоя
echo ============================================

set DEPLOY_DIR=deploy
set PROJECT_DIR=%~dp0

echo Очистка папки deploy...
if exist %DEPLOY_DIR% rmdir /S /Q %DEPLOY_DIR%
mkdir %DEPLOY_DIR%

echo Копирование файлов...

xcopy /E /I /Y app %DEPLOY_DIR%\app
xcopy /E /I /Y templates %DEPLOY_DIR%\templates
xcopy /E /I /Y templates_excel %DEPLOY_DIR%\templates_excel
xcopy /E /I /Y data %DEPLOY_DIR%\data

copy requirements.txt %DEPLOY_DIR%\
copy run.py %DEPLOY_DIR%\
copy README.md %DEPLOY_DIR%\
copy DEPLOY.md %DEPLOY_DIR%\

echo Исключение временных файлов...
if exist %DEPLOY_DIR%\app\__pycache__ rmdir /S /Q %DEPLOY_DIR%\app\__pycache__
if exist %DEPLOY_DIR%\app\core\__pycache__ rmdir /S /Q %DEPLOY_DIR%\app\core\__pycache__
if exist %DEPLOY_DIR%\app\services\__pycache__ rmdir /S /Q %DEPLOY_DIR%\app\services\__pycache__
if exist %DEPLOY_DIR%\app\uploads rmdir /S /Q %DEPLOY_DIR%\app\uploads
if exist %DEPLOY_DIR%\app\output rmdir /S /Q %DEPLOY_DIR%\app\output

echo ============================================
echo Готово! Папка %DEPLOY_DIR% создана
echo ============================================
echo
echo Структура:
tree %DEPLOY_DIR% /F

echo
echo Далее:
echo 1. Заархивируйте папку %DEPLOY_DIR%
echo 2. Загрузите на хостинг
echo 3. Следуйте инструкции в DEPLOY.md
