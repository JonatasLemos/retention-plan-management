import calendar
from datetime import datetime

from dateutil.relativedelta import relativedelta

import constants
from rules import Gold, Platinum, Standard

current_date = datetime.now().date()


def test_standard_match():
    """Test that all plans match if there is a standard match (snapshot in the last 42 days)"""
    test_date = current_date - relativedelta(days=constants.RETENTION_DAYS - 1)
    test_date = test_date.strftime(constants.DATE_FORMAT)
    std = Standard(
        input_date=test_date, retention_days=constants.RETENTION_DAYS
    )
    gold = Gold(input_date=test_date, retention_days=constants.RETENTION_DAYS)
    plat = Platinum(
        input_date=test_date,
        retention_days=constants.RETENTION_DAYS,
        retention_years=constants.RETENTION_YEARS,
    )
    assert std.standard_match
    assert gold.gold_match
    assert plat.platinum_match


def test_standard_no_match():
    """Test that there is not a standard match if the snapshot is older than 42 days"""
    test_date = current_date - relativedelta(days=constants.RETENTION_DAYS + 1)
    test_date = test_date.strftime(constants.DATE_FORMAT)
    std = Standard(
        input_date=test_date, retention_days=constants.RETENTION_DAYS
    )
    assert not std.standard_match


def test_gold_match():
    """Test that the gold and platinum plans match if there is
    a gold match (last snapshot of the month for 12 months)"""
    test_date = current_date - relativedelta(months=6)
    month_range = calendar.monthrange(test_date.year, test_date.month)
    test_date = datetime(test_date.year, test_date.month, month_range[1])
    test_date = test_date.strftime(constants.DATE_FORMAT)
    gold = Gold(input_date=test_date, retention_days=constants.RETENTION_DAYS)
    plat = Platinum(
        input_date=test_date,
        retention_days=constants.RETENTION_DAYS,
        retention_years=constants.RETENTION_YEARS,
    )
    assert gold.gold_match
    assert plat.platinum_match


def test_gold_no_match():
    """Test that there is not a gold match if the snapshot happend within 12 months but not
    in the last day of the month"""
    test_date = current_date - relativedelta(months=6)
    month_range = calendar.monthrange(test_date.year, test_date.month)
    test_date = datetime(test_date.year, test_date.month, month_range[0])
    test_date = test_date.strftime(constants.DATE_FORMAT)
    gold = Gold(input_date=test_date, retention_days=constants.RETENTION_DAYS)
    assert not gold.gold_match


def test_platinum_match():
    """Test that there is a platinum match(last snapshot of the year for 7 years)
    if the snapshot happened in the last day of the year"""
    test_date = current_date - relativedelta(
        years=constants.RETENTION_YEARS - 4
    )
    test_date = datetime(test_date.year, 12, 31)
    test_date = test_date.strftime(constants.DATE_FORMAT)
    plat = Platinum(
        input_date=test_date,
        retention_days=constants.RETENTION_DAYS,
        retention_years=constants.RETENTION_YEARS,
    )
    assert plat.platinum_match


def test_platinum_no_match():
    """Test that there is not a platinum match(last snapshot of the year for 7 years)
    if the snapshot happened in a date different from the last day of the year
    """
    test_date = current_date - relativedelta(
        years=constants.RETENTION_YEARS - 4
    )
    test_date = datetime(test_date.year, 12, 30).date()
    test_date = test_date.strftime(constants.DATE_FORMAT)
    plat = Platinum(
        input_date=test_date,
        retention_days=constants.RETENTION_DAYS,
        retention_years=constants.RETENTION_YEARS,
    )
    assert not plat.platinum_match
