from typing import Optional, Type

from log_analyzer.reports.base import BaseReport
from log_analyzer.reports.handlers import HandlersReport
from log_analyzer.reports.slow_requests import SlowRequestsReport


REPORTS: dict[str, Type[BaseReport]] = {
    'handlers': HandlersReport,
    'slow_requests': SlowRequestsReport,
}


def get_reporter(name: str, level: str = None) -> Optional[BaseReport]:
    report_class = REPORTS.get(name.lower())
    if report_class:
        return report_class(level)
    return None
