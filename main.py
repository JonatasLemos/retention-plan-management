import argparse

from helpers import validate_date_format, validate_plan
from process import process_rules

parser = argparse.ArgumentParser(
    prog="Retention Plan Management",
    description="Check if a backup snapshot for a given date should be retained or deleted.",
)
parser.add_argument(
    "--plan",
    required=True,
    help="The retention plan: Standard, Gold or Platinum.",
    type=validate_plan,
)
parser.add_argument(
    "--date",
    required=True,
    help="The snapshot backup date. Date format must be ISO.",
    type=validate_date_format,
)
args = parser.parse_args()
final_rule = process_rules(
    date_arg=args.date, plan_arg=args.plan.strip().lower()
)
print(final_rule)
