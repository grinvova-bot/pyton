"""
Консольный скрипт для обработки прайс-листов
Использование: python cli.py <путь_к_файлу> [--k2 30] [--k3 40] [--l3 50]
"""
import sys
import argparse
from pathlib import Path

# Добавляем корень проекта в путь
sys.path.insert(0, str(Path(__file__).parent))

from app.services.processor import process_file


def main():
    parser = argparse.ArgumentParser(
        description="Обработка прайс-листов",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python cli.py price.xlsx
  python cli.py price.xlsx --k2 25 --k3 35 --l3 45
  python cli.py price.xlsx --recalculate
        """
    )
    
    parser.add_argument("file", help="Путь к Excel-файлу")
    parser.add_argument("--k2", type=int, default=30, help="Скидка для маркера К2 (по умолчанию 30)")
    parser.add_argument("--k3", type=int, default=40, help="Скидка для маркера К3 (по умолчанию 40)")
    parser.add_argument(
        "--recalculate",
        action="store_true",
        help="Пересчитывать существующие спец. цены для К2/К3/Л3"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Путь для сохранения результата (по умолчанию в output/)"
    )
    
    args = parser.parse_args()
    
    # Проверка существования файла
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Ошибка: файл '{args.file}' не найден")
        sys.exit(1)
    
    print("=" * 60)
    print("Прайс-Стандарт - Обработка прайс-листа")
    print("=" * 60)
    print(f"Файл: {file_path.absolute()}")
    print(f"Настройки скидок: К2={args.k2}%, К3={args.k3}%, Л3={args.l3}%")
    print(f"Пересчёт существующих цен: {'да' if args.recalculate else 'нет'}")
    print("-" * 60)
    
    # Обработка
    discount_settings = {
        "К2": args.k2,
        "К3": args.k3,
    }
    
    success, message, output_filename = process_file(
        str(file_path.absolute()),
        discount_settings,
        args.recalculate
    )
    
    if success:
        print(f"[OK] {message}")
        print(f"[FILE] Файл сохранен: {output_filename}")
        print("=" * 60)
        sys.exit(0)
    else:
        print(f"[ERROR] {message}")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
