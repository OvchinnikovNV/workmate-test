- [Usage](#usage)
- [Добавление нового отчета](#new-report)
- [Добавление нового выходного формата](#new-formet)

<h2 id="usage">Usage</h2>

```
usage: main.py [-h] -r {payout} [-f {json}] [-o OUTPUT] files [files ...]

positional arguments:
  files                 one or more paths to csv files

options:
  -h, --help            show this help message and exit
  -r {payout}, --report {payout}
                        report name (required)
  -f {json}, --format {json}
                        output format (default: json)
  -o OUTPUT, --output OUTPUT
                        output directory (default: 'outputs' dir at the root of project)
```

<h2 id="new-report">Добавление нового отчета</h2>

1. Дополнить enum `ReportType` в файле `src/utils/arg_parser.py`. Например:
    ```python
    class ReportType(enum.Enum):
        payout = 'payout'
        avg_rate = 'avg_rate'
    ```
   
2. В файле `src/utils/employee_data.py` реализовать метод класса `EmployeeData.report_{новое значение ReportType}`.
    Для примера выше:
    ```python
    def report_avg_rate(self) -> dict:
    ```

<h2 id="new-format">Добавление нового выходного формата</h2>

1. Дополнить enum `ReportOutputFormat` в файле `src/utils/arg_parser.py`. Например:
    ```python
    class ReportOutputFormat(enum.Enum):
        json = 'json'
        txt = 'txt'
    ```
   
2. В файле `src/utils/employee_data.py` реализовать метод класса
`EmployeeData._write_report__{новое значение ReportOutputFormat}`. Для примера выше:
    ```python
    @classmethod
    def _write_report_txt(cls, report: dict, filename: str) -> None:
    ```
