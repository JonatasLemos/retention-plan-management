import constants
from rules import Gold, Platinum, Standard

rules = {True: "retained", False: "deleted"}


def process_rules(date_arg: str, plan_arg: str) -> str:
    """Return the rule (deletion or retention) for a given
    plan and snapshot date.

    Args:
        date_arg (str): The snapshot date argument
        plan_arg (str): The retention plan argument

    Returns:
        str: The final rule
    """
    initial_msg = f"The snapshot from {date_arg} should be"
    if plan_arg == "standard":
        standard = Standard(
            input_date=date_arg, retention_days=constants.RETENTION_DAYS
        )
        return f"{initial_msg} {rules[standard.day_rule()]}"
    elif plan_arg == "gold":
        gold = Gold(
            input_date=date_arg, retention_days=constants.RETENTION_DAYS
        )
        return f"{initial_msg} {rules[gold.month_rule()]}"
    # elif plan_arg == "bronze":
    #     bronze = Bronze(
    #         input_date=date_arg,
    #         retention_days=15,
    #         retention_years=3,
    #     )
    #     return f"{initial_msg} {rules[bronze.year_rule()]}"
    platinum = Platinum(
        input_date=date_arg,
        retention_days=constants.RETENTION_DAYS,
        retention_years=constants.RETENTION_YEARS,
    )
    return f"{initial_msg} {rules[platinum.year_rule()]}"
