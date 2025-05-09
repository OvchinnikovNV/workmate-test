import json
from io import TextIOWrapper
from pathlib import Path

import pytest

from src.utils.arg_parser import ReportType, ReportOutputFormat
from src.utils.employee_data import EmployeeData


class TestEmployeeData:
    test_data_dir = (Path(__file__).parent.parent / 'test_data')

    @pytest.fixture(scope='class')
    def files(self) -> tuple:
        return (
            (self.test_data_dir / 'data1.csv').absolute(),
            (self.test_data_dir / 'data2.csv').absolute(),
            (self.test_data_dir / 'empty_data.csv').absolute(),
            (self.test_data_dir / 'incorrect_rate.csv').absolute(),
        )

    def test_parse_csv_files(self, files: tuple):
        files_io: list[TextIOWrapper] = self._get_list_open_files(files, 0, 3)
        try:
            employee_data = EmployeeData(files_io)
            assert len(employee_data.data) == 6
        finally:
            self._close_files(files_io)

    def test_correct_payout_file(self, files: tuple):
        files_io: list[TextIOWrapper] = self._get_list_open_files(files, 0, 1)
        result_filename: Path = (self.test_data_dir / 'payout.json')
        try:
            employee_data = EmployeeData(files_io, output_dir=str(self.test_data_dir))
            employee_data.report(ReportType.payout, ReportOutputFormat.json)

            with open(result_filename) as result_file:
                result = json.dumps(json.load(result_file), sort_keys=True)
            with open((self.test_data_dir / 'data1_payout.json')) as correct_file:
                correct = json.dumps(json.load(correct_file), sort_keys=True)
            assert result == correct
        finally:
            self._close_files(files_io)
            if result_filename.exists():
                result_filename.unlink()

    def test_incorrect_rate_column(self, files: tuple):
        files_io: list[TextIOWrapper] = self._get_list_open_files(files, 3, 4)
        try:
            employee_data = EmployeeData(files_io)
            with pytest.raises(KeyError):
                employee_data.report_payout()
        finally:
            self._close_files(files_io)

    @classmethod
    def _get_list_open_files(cls, files: tuple, start: int, end: int) -> list[TextIOWrapper]:
        return [open(file) for file in files[start:end]]

    @classmethod
    def _close_files(cls, files: list[TextIOWrapper]):
        for file in files:
            file.close()
