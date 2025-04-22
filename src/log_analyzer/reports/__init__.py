from typing import Optional, Type

from log_analyzer.reports.handlers import HandlersReport
from log_analyzer.reports.base import BaseReport


REPORTS: dict[str, Type[BaseReport]] = {
    'handlers': HandlersReport,
}


def get_reporter(name: str) -> Optional[BaseReport]:
    report_class = REPORTS.get(name.lower())
    if report_class:
        return report_class()
    return None
