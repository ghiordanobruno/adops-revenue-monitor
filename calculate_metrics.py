from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from clean_data import DEFAULT_OUTPUT as DEFAULT_CLEAN_PATH, load_csv
from generate_sample_data import PROJECT_ROOT


DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "processed" / "metrics.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate AdOps metrics.")
    parser.add_argument("--input", type=Path, default=DEFAULT_CLEAN_PATH, help="Clean CSV input path.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Metrics CSV output path.")
    return parser.parse_args()


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    denominator = denominator.astype(float).where(denominator.astype(float) != 0)
    return (numerator.astype(float) / denominator).fillna(0.0)


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()
    output["match_rate"] = safe_divide(output["matched_requests"], output["ad_requests"])
    output["fill_rate"] = safe_divide(output["impressions"], output["matched_requests"])
    output["ctr"] = safe_divide(output["clicks"], output["impressions"])
    output["rpm"] = safe_divide(output["estimated_revenue"] * 1000, output["ad_requests"])
    output["ecpm"] = safe_divide(output["estimated_revenue"] * 1000, output["impressions"])

    metric_columns = ["fill_rate", "ctr", "rpm", "ecpm", "match_rate"]
    output[metric_columns] = output[metric_columns].round(6)
    return output


def save_csv(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def main() -> None:
    args = parse_args()

    try:
        clean_df = load_csv(args.input)
        metrics_df = calculate_metrics(clean_df)
        save_csv(metrics_df, args.output)
    except Exception as exc:
        raise SystemExit(f"Failed to calculate metrics: {exc}") from exc

    print(f"Calculated metrics for {len(metrics_df):,} rows at {args.output}")


if __name__ == "__main__":
    main()
