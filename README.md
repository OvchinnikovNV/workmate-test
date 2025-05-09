- [Usage](#usage)
- [Добавление нового отчета](#new-report)
- [Добавление нового выходного формата](#new-formet)
- [Результат для data1.csv](#result1)
- [Результат для трех файлов](#result-all)

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

<h2 id="result1">Результат для data1.csv</h2>

```json
{
     "Marketing": {
          "hours": 160,
          "payout": 8000,
          "employees": [
               {
                    "name": "Alice Johnson",
                    "hours": 160,
                    "rate": 50,
                    "payout": 8000
               }
          ]
     },
     "Design": {
          "hours": 320,
          "payout": 16200,
          "employees": [
               {
                    "name": "Bob Smith",
                    "hours": 150,
                    "rate": 40,
                    "payout": 6000
               },
               {
                    "name": "Carol Williams",
                    "hours": 170,
                    "rate": 60,
                    "payout": 10200
               }
          ]
     }
}
```

<h2 id="result-all">Результат для трех файлов</h2>

```json
{
     "Marketing": {
          "hours": 310,
          "payout": 13250,
          "employees": [
               {
                    "name": "Alice Johnson",
                    "hours": 160,
                    "rate": 50,
                    "payout": 8000
               },
               {
                    "name": "Henry Martin",
                    "hours": 150,
                    "rate": 35,
                    "payout": 5250
               }
          ]
     },
     "Design": {
          "hours": 320,
          "payout": 16200,
          "employees": [
               {
                    "name": "Bob Smith",
                    "hours": 150,
                    "rate": 40,
                    "payout": 6000
               },
               {
                    "name": "Carol Williams",
                    "hours": 170,
                    "rate": 60,
                    "payout": 10200
               }
          ]
     },
     "HR": {
          "hours": 473,
          "payout": 19714,
          "employees": [
               {
                    "name": "Grace Lee",
                    "hours": 160,
                    "rate": 45,
                    "payout": 7200
               },
               {
                    "name": "Ivy Clark",
                    "hours": 158,
                    "rate": 38,
                    "payout": 6004
               },
               {
                    "name": "Liam Harris",
                    "hours": 155,
                    "rate": 42,
                    "payout": 6510
               }
          ]
     },
     "Sales": {
          "hours": 325,
          "payout": 14170,
          "employees": [
               {
                    "name": "Karen White",
                    "hours": 165,
                    "rate": 50,
                    "payout": 8250
               },
               {
                    "name": "Mia Young",
                    "hours": 160,
                    "rate": 37,
                    "payout": 5920
               }
          ]
     }
}
```
