import re

from collections import defaultdict
from datetime import datetime
from typing import Dict, Callable


LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+)\s+"
    r"(?P<level>\w+)\s+"
    r"(?P<logger>[\w\.]+):\s+"
    r"(?:(?P<method>GET|POST|PUT|DELETE|PATCH)\s+(?P<path>/[^\s']*)\s+(?P<status>\d{3})\s+OK\s+\[(?P<ip>[^\]]+)\])?"
    r"(?:.*?-\s+(?P<message>.*))?"
)


def nested_defaultdict() -> defaultdict[str, int]:
    return defaultdict(int)


def parse_log_line(line: str) -> dict | None:
    match = LOG_PATTERN.search(line)
    if not match:
        return None
    groups = match.groupdict()
    try:
        return {
            "timestamp": datetime.strptime(groups["timestamp"], "%Y-%m-%d %H:%M:%S,%f"),
            "level": groups["level"].upper(),
            "logger": groups.get("logger", ""),
            "method": groups.get("method"),
            "path": groups.get("path"),
            "status": int(groups["status"]) if groups["status"] else None,
            "ip": groups.get("ip"),
            "message": groups.get("message", "").strip(),
        }
    except Exception:
        return None


def parse_log_file(file_path: str, aggregator: Callable[[dict], None] = None):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data = parse_log_line(line)
            if data and aggregator:
                aggregator(data)


def collect_handler_stats(files: list[str]) -> dict[str, dict[str, int]]:
    stats = defaultdict(lambda: defaultdict(int))

    def aggregator(entry: dict):
        if entry["path"] and entry["level"]:
            stats[entry["path"]][entry["level"]] += 1
    for file_path in files:
        parse_log_file(file_path, aggregator)
    return stats
