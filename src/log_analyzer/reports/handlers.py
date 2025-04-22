from typing import List

from log_analyzer.reports.base import BaseReport


class HandlersReport(BaseReport):
    def run(self, files: List[str]) -> None:
        print(f'[handlers] Запуск анализа логов по файлам: {", ".join(files)}')
        print('[handlers] Анализ завершён')
