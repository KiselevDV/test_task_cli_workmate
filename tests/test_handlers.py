import pytest

from unittest.mock import patch
from io import StringIO

from log_analyzer.main import main
from log_analyzer.reports.handlers import HandlersReport
from log_analyzer.services.file_parser import collect_handler_stats


@pytest.fixture
def mock_log_file():
    return 'logs/app1.log'


@pytest.fixture
def sample_data():
    return {
        '/api/v1/reviews/': {
            'INFO': 10,
            'ERROR': 2,
        },
        '/api/v1/orders/': {
            'DEBUG': 5,
            'WARNING': 1,
        },
    }


def test_cli_correct_report(mock_log_file):
    with patch('sys.argv', ['log-analyzer', mock_log_file, '--report', 'handlers']):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            assert 'HANDLER' in output
            assert 'INFO' in output
            assert 'ERROR' in output


def test_handlers_report(sample_data):
    report = HandlersReport(level='INFO')
    with patch('log_analyzer.reports.handlers.collect_handler_stats', return_value=sample_data):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            report.run(['logs/app1.log'])
            output = mock_stdout.getvalue()
            assert 'INFO' in output
            assert '10' in output


def test_collect_handler_stats(sample_data):
    files = ['logs/app1.log']
    result = collect_handler_stats(files)
    assert isinstance(result, dict)
    assert '/api/v1/reviews/' in result
    assert 'INFO' in result['/api/v1/reviews/']
    assert result['/api/v1/reviews/']['INFO'] == 10


def test_filter_logs_by_level():
    logs = [
        {'level': 'INFO', 'message': 'Info log'},
        {'level': 'ERROR', 'message': 'Error log'},
        {'level': 'INFO', 'message': 'Another info log'},
    ]
    filtered_logs = filter_logs_by_level(logs, 'INFO')
    assert len(filtered_logs) == 2
    assert filtered_logs[0]['level'] == 'INFO'
