from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from generate_sample_data import COLUMNS, DEFAULT_OUTPUT as DEFAULT_RAW_PATH, PROJECT_ROOT


DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "processed" / "clean_data.csv"

CATEGORY_COLUMNS = ["site_section", "device", "country", "ad_unit"]
INTEGER_COLUMNS = ["ad_requests", "matched_requests", "impressions", "clicks"]
FLOAT_COLUMNS = ["estimated_revenue"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean AdOps performance data.")
    parser.add_argument("--input", type=Path, default=DEFAULT_RAW_PATH, help="Raw CSV input path.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Clean CSV output path.")
    return parser.parse_args()


def load_csv(input_path: Path) -> pd.DataFrame:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    return pd.read_csv(input_path)


def validate_required_columns(df: pd.DataFrame) -> None:
    missing_columns = [column for column in COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")


def normalize_categories(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()

    for column in CATEGORY_COLUMNS:
        output[column] = output[column].astype("string").fillna("unknown").str.strip()
        output[column] = output[column].replace("", "unknown")

    output["country"] = output["country"].str.upper()
    return output


def normalize_dates(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()
    output["date"] = pd.to_datetime(output["date"], errors="coerce")
    output = output.dropna(subset=["date"])
    output["date"] = output["date"].dt.strftime("%Y-%m-%d")
    return output


def normalize_numeric_values(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()

    for column in INTEGER_COLUMNS:
        output[column] = pd.to_numeric(output[column], errors="coerce")
        output[column] = output[column].fillna(0).clip(lower=0).round().astype("int64")

    for column in FLOAT_COLUMNS:
        output[column] = pd.to_numeric(output[column], errors="coerce")
        output[column] = output[column].fillna(0).clip(lower=0).round(2)

    return output


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    validate_required_columns(df)
    output = df[COLUMNS].copy()
    output = normalize_dates(output)
    output = normalize_categories(output)
    output = normalize_numeric_values(output)
    output = output.drop_duplicates()
    output = output.sort_values(["date", "site_section", "device", "country", "ad_unit"])
    return output.reset_index(drop=True)


def save_csv(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def main() -> None:
    args = parse_args()

    try:
        raw_df = load_csv(args.input)
        clean_df = clean_data(raw_df)
        save_csv(clean_df, args.output)
    except Exception as exc:
        raise SystemExit(f"Failed to clean data: {exc}") from exc

    print(f"Cleaned {len(clean_df):,} rows at {args.output}")


if __name__ == "__main__":
    main()
