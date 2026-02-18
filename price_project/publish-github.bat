@echo off
REM Автоматическая публикация на GitHub

echo ============================================
echo Публикация проекта на GitHub
echo ============================================
echo

REM Проверка наличия Git
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ОШИБКА: Git не найден!
    echo Установите Git с https://git-scm.com/
    pause
    exit /b 1
)

echo Git найден: 
git --version
echo

REM Проверка наличия GitHub CLI
where gh >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo GitHub CLI найден - будет использован
    set USE_GH=1
) else (
    echo GitHub CLI не найден - будет использован обычный git
    set USE_GH=0
)
echo

REM Инициализация репозитория
if not exist .git (
    echo Инициализация Git-репозитория...
    git init
    echo.
)

REM Добавление всех файлов
echo Добавление файлов...
git add .
echo

REM Создание коммита
echo Введите сообщение для коммита (или нажмите Enter для стандартного):
set /p COMMIT_MSG=
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Initial commit: Price Standard project

git commit -m "%COMMIT_MSG%"
echo

REM Создание/проверка удалённого репозитория
echo
echo ============================================
echo Создание репозитория на GitHub
echo ============================================
echo

if %USE_GH% EQU 1 (
    echo Использование GitHub CLI...
    echo
    
    REM Проверка авторизации
    gh auth status >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo Требуется авторизация в GitHub...
        gh auth login
    )
    
    REM Создание репозитория
    echo Введите имя репозитория (или нажмите Enter для 'price-standard'):
    set /p REPO_NAME=
    if "%REPO_NAME%"=="" set REPO_NAME=price-standard
    
    echo Создание репозитория '%REPO_NAME%'...
    gh repo create %REPO_NAME% --public --source=. --remote=origin --push
    
    echo
    echo ============================================
    echo ГОТОВО! Репозиторий создан и загружен
    echo ============================================
    echo URL: https://github.com/%USERNAME%/%REPO_NAME%
    echo
) else (
    echo GitHub CLI не доступен - ручная настройка
    echo
    echo 1. Создайте репозиторий на https://github.com/new
    echo 2. Введите имя: price-standard
    echo 3. Скопируйте URL репозитория
    echo
    set /p REPO_URL=Вставьте URL репозитория:
    
    git remote add origin %REPO_URL%
    
    REM Отправка на GitHub
    git branch -M main
    git push -u origin main
    
    echo
    echo ============================================
    echo ГОТОВО! Проект загружен на GitHub
    echo ============================================
    echo URL: %REPO_URL%
    echo
)

pause
