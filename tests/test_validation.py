import argparse
import datetime

import pytest

from helpers import validate_date_format, validate_plan
from validate import Date


def test_invalid_date_format():
    """Test non ISO date format"""
    with pytest.raises(argparse.ArgumentTypeError):
        validate_date_format("18-09")


def test_inexistent_plan():
    """Test a plan which does not exist"""
    with pytest.raises(argparse.ArgumentTypeError):
        validate_plan("Silver")


def test_date_conversion():
    """Test if string is converted to datetime.date"""
    input_date = Date("2004-12-12")
    assert type(input_date.date) == datetime.date


def test_older_date():
    """Test that an old date raises an exception"""
    with pytest.raises(ValueError):
        Date(date="1899-01-01")


def test_future_date():
    """Test that a future date raises an exception"""
    with pytest.raises(ValueError):
        Date(date="2899-01-01")
