import csv
import json
from pathlib import Path

import pytest

from src.utils.csv_parser import MyCSVParser


class TestMyCSVParser:
    test_data_dir = (Path(__file__).parent.parent / 'test_data')

    @classmethod
    @pytest.fixture(scope='class')
    def get_csv_file(cls):
        file = open((cls.test_data_dir / 'data1.csv').absolute(), 'r')
        yield file
        file.close()

    @classmethod
    @pytest.fixture(scope='class')
    def get_empty_csv_file(cls):
        file = open((cls.test_data_dir / 'empty_data.csv').absolute(), 'r')
        yield file
        file.close()

    def test_to_json(self, get_csv_file):
        result = json.dumps(MyCSVParser.to_json(get_csv_file), sort_keys=True)
        get_csv_file.seek(0)
        correct_json = [obj for obj in csv.DictReader(get_csv_file)]
        assert result == json.dumps(correct_json, sort_keys=True)

    def test_to_json_empty(self, get_empty_csv_file):
        assert MyCSVParser.to_json(get_empty_csv_file) == []
