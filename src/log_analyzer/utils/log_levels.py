LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


def filter_logs_by_level(log_data: list[dict], level: str) -> list[dict]:
    """Фильтрует логи по уровню"""
    return [entry for entry in log_data if entry['level'] == level]
