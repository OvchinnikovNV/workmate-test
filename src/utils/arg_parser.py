import argparse
import enum
import sys
from argparse import ArgumentParser


class ReportType(enum.Enum):
    payout = 'payout'


class ReportOutputFormat(enum.Enum):
    json = 'json'


class MyArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_argument(
            'files',
            nargs='+',
            type=argparse.FileType('r'),
            help='one or more paths to csv files',
        )
        self.add_argument(
            '-r', '--report',
            type=str,
            choices=[e.value for e in ReportType],
            required=True,
            help='report name (required)',
        )
        self.add_argument(
            '-f', '--format',
            type=str,
            choices=[f.value for f in ReportOutputFormat],
            default=ReportOutputFormat.json.value,
            help='output format (default: %(default)s)',
        )
        self.add_argument(
            '-o', '--output',
            type=str,
            help="output directory (default: 'outputs' dir at the root of project)",
        )

    def error(self, message):
        if 'are required: -r/--report' in message:
            _message = (f"Нужно явно указать название отчета с помощью параметра -r/--report. "
                        f"Доступные варианты: {[rt.value for rt in ReportType]}")
        elif '-r/--report: invalid choice' in message:
            _message = f"Указано неверное название отчета. Доступные варианты: {[t.value for t in ReportType]}"
        elif 'No such file or directory' in message:
            error_file = message.split("argument files: can't open ")[1].split("\'")[1]
            _message = f"Файл с данными не найден: '{error_file}'"
        elif 'arguments are required: files' in message:
            _message = f"Не передано ни одного файла с данными"
            self.print_usage(sys.stderr)
        elif '-f/--format: invalid choice' in message:
            _message = f"Указан неверный выходной формат. Доступные варианты: {[f.value for f in ReportOutputFormat]}"
        else:
            _message = message

        self.exit(2, f"{self.prog}: error: {_message}\n")
