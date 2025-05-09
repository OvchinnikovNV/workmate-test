from io import TextIOWrapper
from pathlib import Path

import pytest

from src.utils.arg_parser import MyArgumentParser, ReportOutputFormat


@pytest.fixture(scope='module')
def data_filename() -> str:
    return str((Path(__file__).parent.parent / 'test_data' / 'data1.csv').absolute())


@pytest.fixture(scope='module')
def parser() -> MyArgumentParser:
    return MyArgumentParser()


def test_parsing(parser, data_filename):
    args = parser.parse_args([data_filename, "--report", "payout"])
    assert ('payout', 1, TextIOWrapper) == (args.report, len(args.files), type(args.files[0]))


def test_required_files(parser):
    with pytest.raises(SystemExit):
        parser.parse_args(["--report", "payout"])


def test_required_report(parser, data_filename):
    with pytest.raises(SystemExit):
        parser.parse_args([data_filename])


def test_incorrect_report(parser, data_filename):
    with pytest.raises(SystemExit):
        parser.parse_args([data_filename, "--report", "unknown"])


def test_incorrect_format(parser, data_filename):
    with pytest.raises(SystemExit):
        parser.parse_args([data_filename, "--report", "payout", "--format", "unknown"])


def test_default_format(parser, data_filename):
    args = parser.parse_args([data_filename, "--report", "payout"])
    assert args.format == ReportOutputFormat.json.value


def test_default_output(parser, data_filename):
    args = parser.parse_args([data_filename, "--report", "payout"])
    assert args.output is None
