import argparse
import datetime

import constants


def validate_date_format(input_date: str) -> str:
    """Function to perform date validation for the parser

    Args:
        input_date (str): Input date from parser as string

    Raises:
        argparse.ArgumentTypeError: If the input date is not ISO.

    Returns:
        str: Validated input date
    """
    try:
        datetime.date.fromisoformat(input_date)
        return input_date
    except ValueError:
        msg = f"The date: {input_date} is not a valid date, it must follow the ISO format: {constants.DATE_FORMAT}"
        raise argparse.ArgumentTypeError(msg)


def validate_plan(input_plan: str) -> str:
    """Function to perform plan validation for the parser

    Args:
        input_plan (str): Input plan from parser as string

    Raises:
        argparse.ArgumentTypeError: If the input plan is not an available plan.

    Returns:
        str: Validated input plan
    """
    if input_plan.lower() not in map(str.lower, constants.AVAILABLE_PLANS):
        msg = "not a valid plan"
        raise argparse.ArgumentTypeError(msg)
    return input_plan
