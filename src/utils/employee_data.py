import itertools
import json
import os
from io import TextIOWrapper
from pathlib import Path

from .arg_parser import ReportType, ReportOutputFormat
from .csv_parser import MyCSVParser


class EmployeeData:
    _rate_names = [
        'hourly_rate',
        'rate',
        'salary',
    ]
    _default_reports_dir = 'outputs'
    _unique_employees = True

    def __init__(self, files: list[TextIOWrapper], output_dir: str | None = None):
        self.data: list[dict] = self._parse_csv_files(files)
        self.output_dir: str | None = output_dir

    def report(
            self,
            report_type: str | ReportType,
            output_format: str | ReportOutputFormat = ReportOutputFormat.json,
    ) -> dict:
        method = f"report_{report_type if type(report_type) == str else report_type.value}"
        if not hasattr(self, method):
            raise AttributeError(f"EmployeeData class has no method {method}")

        report = getattr(self, method)()
        self._write_report(report, report_type, output_format)
        return report

    def report_payout(self) -> dict:
        result: dict[str, dict] = dict()

        for employee in self.data:
            department: str = employee['department']
            hours: int = int(employee["hours_worked"])
            rate: int = self._get_employee_rate(employee)

            if department in result:
                result[department]["hours"] += hours
                result[department]["payout"] += hours * rate
                result[department]["employees"].append({
                    "name": employee["name"],
                    "hours": hours,
                    "rate": rate,
                    "payout": hours * rate,
                })
            else:
                result[department] = {
                    "hours": hours,
                    "payout": hours * rate,
                    "employees": [{
                        "name": employee["name"],
                        "hours": hours,
                        "rate": rate,
                        "payout": hours * rate,
                    }]
                }

        return result

    @classmethod
    def _parse_csv_files(cls, files: list[TextIOWrapper]) -> list[dict]:
        data = list()
        for file in files:
            data.append(MyCSVParser.to_json(file))
            file.close()
        return cls._get_unique_employees(data)

    @classmethod
    def _get_unique_employees(cls, data: list[dict]) -> list[dict]:
        if not cls._unique_employees:
            return list(itertools.chain(*data))

        ids = set()
        result: list[dict] = list()
        for employee in itertools.chain(*data):
            employee_id = int(employee["id"])
            if employee_id not in ids:
                result.append(employee)
            ids.add(employee_id)
        return result

    @classmethod
    def _get_employee_rate(cls, employee: dict[str, str]) -> int:
        for rate_name in cls._rate_names:
            if rate_name in employee:
                return int(employee[rate_name])
        raise KeyError(f"Not found rate key for employee {employee['id']}")

    def _write_report(
            self,
            report: dict,
            report_type: str | ReportType,
            output_format: str | ReportOutputFormat = ReportOutputFormat.json,
    ) -> None:
        if self.output_dir is None:
            reports_dir = (Path(__file__).parent.parent.parent / self._default_reports_dir).absolute()
        else:
            reports_dir = Path(self.output_dir).absolute()
        report_type_str = report_type if type(report_type) == str else report_type.value
        output_type_str = output_format if type(output_format) == str else output_format.value
        filename = f"{reports_dir}/{report_type_str}.{output_type_str}"

        method = f"_write_report_{output_type_str}"
        if not hasattr(self, method):
            raise AttributeError(f"EmployeeData class has no method {method}")

        os.makedirs(reports_dir, exist_ok=True)
        return getattr(self, method)(
            report=report,
            filename=filename,
        )

    @classmethod
    def _write_report_json(cls, report: dict, filename: str) -> None:
        with open(filename, 'w') as file:
            json.dump(report, file, indent=5)
