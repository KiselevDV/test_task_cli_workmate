from typing import List

from log_analyzer.reports.base import BaseReport
from log_analyzer.services.file_parser import collect_handler_stats  # Импортируем функцию
from log_analyzer.utils.log_levels import LOG_LEVELS


class HandlersReport(BaseReport):
    def __init__(self, level: str = None):
        self.level = level

    def run(self, files: List[str]) -> None:
        data = collect_handler_stats(files)  # Используем функцию для сбора данных
        if self.level:
            data = {handler: {lvl: count for lvl, count in levels.items() if lvl == self.level}
                    for handler, levels in data.items()}
        self.print_report(data)

    def print_report(self, data: dict[str, dict[str, int]]) -> None:
        handlers = sorted(data.keys())
        level_totals = {lvl: 0 for lvl in LOG_LEVELS}
        total_requests = 0
        header = "HANDLER".ljust(30) + "".join(level.ljust(10) for level in LOG_LEVELS)
        print(header)
        print("-" * len(header))
        for handler in handlers:
            line = handler.ljust(30)
            for level in LOG_LEVELS:
                count = data[handler].get(level, 0)
                line += str(count).ljust(10)
                level_totals[level] += count
                total_requests += count
            print(line)
        total_line = ' ' * 30 + ''.join(str(level_totals[level]).ljust(10) for level in LOG_LEVELS)
        print('-' * len(header))
        print(total_line)
        print(f'\nTotal requests: {total_requests}')
