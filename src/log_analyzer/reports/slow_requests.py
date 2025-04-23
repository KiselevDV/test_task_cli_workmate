from log_analyzer.reports.base import BaseReport


class SlowRequestsReport(BaseReport):
    def run(self, files: list[str]) -> None:
        print('Тестовая заглушка отчёта')
