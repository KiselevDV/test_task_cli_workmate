# Log Analyzer

CLI-приложение для анализа логов Django. Поддерживает отчёты по различным метрикам и фильтрацию по уровням логирования (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).


## Установка

```bash
git clone https://github.com/yourusername/log-analyzer.git
cd log-analyzer
poetry install
```


## Использование

```bash
poetry run log-analyzer logs/app1.log logs/app2.log --report handlers --level ERROR
```
- logs/app1.log logs/app2.log — один или несколько файлов логов
- --report — имя отчёта (например: handlers)
- --level — уровень логирования (необязательный параметр)


## Доступные отчёты

- handlers — выводит статистику по обработчикам (endpoint'ам) и уровням логирования
- slow_requests — пример заглушки под будущую реализацию анализа медленных запросов


## Добавление нового отчёта

Чтобы добавить новый отчёт:
1) Создайте файл в src/log_analyzer/reports, например: my_report.py. 
2) Реализуйте класс, унаследованный от BaseReport, и реализуйте метод run:
```python
# src/log_analyzer/reports/my_report.py
from log_analyzer.reports.base import BaseReport

class MyCustomReport(BaseReport):
    def __init__(self, level: str = None):
        self.level = level

    def run(self, files: list[str]) -> None:
        # Анализ логов
        print("Пример отчёта: MyCustomReport")
```
3) Зарегистрируйте новый отчёт в src/log_analyzer/reports/__init__.py:
```python
from log_analyzer.reports.my_report import MyCustomReport

REPORTS = {
    'handlers': HandlersReport,
    'slow_requests': SlowRequestsReport,
    'my_report': MyCustomReport,  # <--- добавьте сюда
}

```
Теперь можно запускать:
```bash
poetry run log-analyzer logs/app1.log logs/app2.log --report handlers --level ERROR
```


## Лог уровни

Фиксированный список:
- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL


## Тестирование

Приложение покрыто тестами. Запуск:
```bash
poetry install --with dev
poetry run pytest --cov=src
```
Цель — достичь 80% покрытия, особенно важно тестировать:
- CLI-интерфейс
- корректность сбора статистики
- корректность фильтрации по уровню логирования

UI-аспекты (например, выравнивание колонок) можно не покрывать


## Линтинг и стиль

Форматирование и проверка кода:
```bash
poetry add --group dev flake8
poetry run flake8 src tests
```


## Структура проекта

```
.
├── logs/                    # Примеры логов
├── src/log_analyzer/       # Исходный код приложения
│   ├── reports/            # Реализации отчётов
│   ├── services/           # Парсеры и обработчики логов
│   └── utils/              # Утилиты, уровни логирования
├── tests/                  # Тесты
├── pyproject.toml
└── README.md
```
