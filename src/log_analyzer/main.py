import argparse
import os
import sys

from log_analyzer.reports import get_reporter


def parse_args():
    parser = argparse.ArgumentParser(
        description='Анализ логов Django и генерация отчётов'
    )
    parser.add_argument(
        'files',
        nargs='+',
        help='Пути к логам (можно передать несколько файлов)',
    )
    parser.add_argument(
        '--report',
        required=True,
        help='Название отчета (например, handlers)',
    )
    return parser.parse_args()


def validate_files(file_paths: list[str]) -> None:
    for path in file_paths:
        if not os.path.isfile(path):
            print(f'Файл не найден: {path}', file=sys.stderr)
            sys.exit(1)


def validate_report(report_name: str):
    reporter = get_reporter(report_name)
    if not reporter:
        print(f'Отчёт с названием "{report_name}" не существует', file=sys.stderr)
        sys.exit(1)
    return reporter


def main():
    args = parse_args()
    validate_files(args.files)
    reporter = validate_report(args.report)
    reporter.run(args.files)


if __name__ == "__main__":
    main()
