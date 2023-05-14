import calendar
from abc import ABC, abstractmethod
from datetime import datetime

from dateutil.relativedelta import relativedelta

from validate import Date

current_date = datetime.now().date()


class DailyRule(ABC):
    """Base abstract class for plans with daily rules"""

    @abstractmethod
    def day_rule():
        """Day rule abstract method"""
        pass


class MonthlyRule(ABC):
    """Base abstract class for plans with monthly rules"""

    @abstractmethod
    def month_rule():
        """Month rule abstract method"""
        pass


class YearlyRule(ABC):
    """Base abstract class for plans with yearly rules"""

    @abstractmethod
    def year_rule():
        """Year rule abstract method"""
        pass


class Standard(DailyRule):
    def __init__(self, input_date: str, retention_days: int) -> None:
        """Standard Plan - contains only a day rule. Derived from
        DailyRule class.

        Args:
            date (str): The snapshot date string
            retention_days (int): The number of retention days
        """
        self._date = Date(date=input_date).date
        self._retention_days = retention_days
        self.standard_match = False
        self.day_rule()

    def day_rule(self) -> bool:
        """The plan's day rule
        Returns:
            bool: Wether the rule is matched
        """
        time_delta = current_date - self._date
        self.standard_match = time_delta.days <= self._retention_days


class Gold(Standard, MonthlyRule):
    def __init__(self, input_date: str, retention_days: int) -> None:
        """Gold Plan rules - It first applies the Standard plan day rule
        to finally apply the month rule. Derived from Standard and MonthlyRule
        classes.

        Args:
            date (str): The snapshot date string
            retention_days (int): The number of retention days
        """
        super().__init__(input_date, retention_days)
        self.gold_match = False
        self.day_rule()
        self.month_rule()

    def day_rule(self) -> bool:
        """The plan's day rule
        Returns:
            bool: Wether the rule is matched
        """
        return super().day_rule()

    def month_rule(self) -> bool:
        """The plan's month rule
        Returns:
            bool: Wether the rule is matched
        """
        if self.standard_match:
            self.gold_match = True
        elif self._date > current_date - relativedelta(years=1):
            month_range = calendar.monthrange(
                self._date.year, self._date.month
            )
            self.gold_match = self._date.day == month_range[1]


class Platinum(Gold, YearlyRule):
    def __init__(
        self, input_date: str, retention_days: int, retention_years: int
    ) -> None:
        """Platinum Plan rules - It first applies the day rule from the Standard plan,
        than it applies the month rule from the Gold Plan to finally apply the year rule.
        Derived from Gold and YearlyRule classes.

        Args:
            date (str): The snapshot date string
            retention_days (int): The number of retention days
        """
        super().__init__(input_date, retention_days)
        self._retention_years = retention_years
        self.platinum_match = False
        self.day_rule()
        self.month_rule()
        self.year_rule()

    def day_rule(self):
        """The plan's day rule
        Returns:
            bool: Wether the rule is matched
        """
        return super().day_rule()

    def month_rule(self) -> bool:
        """The plan's month rule
        Returns:
            bool: Wether the rule is matched
        """
        return super().month_rule()

    def year_rule(self) -> bool:
        """The plan's year rule
        Returns:
            bool: Wether the rule is matched
        """
        if self.standard_match or self.gold_match:
            self.platinum_match = True
        elif self._date > current_date - relativedelta(
            years=self._retention_years
        ):
            self.platinum_match = (
                self._date.day == 31 and self._date.month == 12
            )
