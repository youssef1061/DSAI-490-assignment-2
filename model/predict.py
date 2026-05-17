import argparse
import calendar
from pathlib import Path
from typing import List, Tuple


DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
MONTH_TO_IDX = {month: i + 1 for i, month in enumerate(MONTHS)}
MIN_YEAR = 1800
MAX_YEAR = 2200


def parse_condition_tokens(line: str) -> Tuple[str, str, str, str]:
    parts = line.strip().split()
    if len(parts) < 4:
        raise ValueError(f"Expected four condition tokens, got: {line!r}")
    return tuple(part.strip("[]") for part in parts[:4])


def format_condition(cond: Tuple[str, str, str, str]) -> str:
    day, month, leap, decade = cond
    return f"[{day}] [{month}] [{leap}] [{decade}]"


def is_leap_year(year: int) -> bool:
    return calendar.isleap(year)


def weekday_token(day: int, month: int, year: int) -> str:
    return DAYS[calendar.weekday(year, month, day)]


def valid_dates_for_condition(cond: Tuple[str, str, str, str]) -> List[str]:
    day_token, month_token, leap_token, decade_token = cond
    month = MONTH_TO_IDX[month_token]
    start_year = int(decade_token) * 10
    dates = []

    for year in range(start_year, start_year + 10):
        if year < MIN_YEAR or year > MAX_YEAR:
            continue
        if str(is_leap_year(year)) != leap_token:
            continue
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            if weekday_token(day, month, year) == day_token:
                dates.append(f"{day}-{month}-{year}")
    return dates


def predict_one(cond: Tuple[str, str, str, str]) -> str:
    valid = valid_dates_for_condition(cond)
    if not valid:
        raise ValueError(f"No valid date found for condition: {format_condition(cond)}")
    return valid[0]


def predict_file(input_path: Path, output_path: Path) -> None:
    input_lines = [line.strip() for line in input_path.read_text().splitlines() if line.strip()]
    output_lines = []
    for line in input_lines:
        cond = parse_condition_tokens(line)
        output_lines.append(f"{format_condition(cond)} {predict_one(cond)}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(output_lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate assignment-format date predictions.")
    parser.add_argument("-i", "--input", required=True, type=Path, help="Path to input conditions file.")
    parser.add_argument("-o", "--output", required=True, type=Path, help="Path to output predictions file.")
    args = parser.parse_args()
    predict_file(args.input, args.output)


if __name__ == "__main__":
    main()
