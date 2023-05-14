from datetime import datetime

import constants


class Date:
    def __init__(self, date: str) -> None:
        """Convert and validate the input date

        Args:
            date (str): The input date in the ISO format
        """
        self._date = date
        self._initial_date = datetime.strptime(
            constants.INITIAL_DATE, constants.DATE_FORMAT
        ).date()
        self.convert_to_datetime()

    def convert_to_datetime(self):
        """Convert the date string to datetime.date"""
        self._date = datetime.strptime(
            self._date, constants.DATE_FORMAT
        ).date()
        self.validate_initial_date()

    def validate_initial_date(self):
        """Validate if provided date is greater than the initial date

        Raises:
            ValueError: If the provided date is smaller that the initial date
        """
        if self._date < self._initial_date:
            raise ValueError(
                f"The date provided: {self._date} is older than the initial date: {self._initial_date}"
            )
        self.validate_current_date()

    def validate_current_date(self):
        """Validate if the provided date is not in the future

        Raises:
            ValueError: If the provided date is in the future
        """
        if self._date >= datetime.now().date():
            raise ValueError(
                f"The date provided {self._date} is in the future"
            )

    @property
    def date(self) -> datetime.date:
        """Return the converted and validated date

        Returns:
            datetime.date: The input date as datetime.date
        """
        return self._date
