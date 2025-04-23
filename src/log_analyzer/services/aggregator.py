from collections import defaultdict
from multiprocessing import Pool
from typing import List, Dict

from log_analyzer.services.file_parser import parse_log_file


def nested_defaultdict() -> defaultdict[str, int]:
    return defaultdict(int)


def merge_stats(stats_list: List[Dict[str, Dict[str, int]]]) -> Dict[str, Dict[str, int]]:
    merged: Dict[str, Dict[str, int]] = defaultdict(nested_defaultdict)
    for stats in stats_list:
        for path, levels in stats.items():
            for level, count in levels.items():
                merged[path][level] += count
    return merged


def process_files_parallel(file_paths: List[str]) -> Dict[str, Dict[str, int]]:
    with Pool() as pool:
        results = pool.map(parse_log_file, file_paths)
    return merge_stats(results)
