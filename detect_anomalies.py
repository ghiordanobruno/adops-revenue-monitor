from __future__ import annotations

import argparse
from collections.abc import Callable
from pathlib import Path

import pandas as pd

from calculate_metrics import DEFAULT_OUTPUT as DEFAULT_METRICS_PATH
from clean_data import load_csv
from generate_sample_data import PROJECT_ROOT


DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "processed" / "anomalies.csv"

GROUP_COLUMNS = ["site_section", "device", "country", "ad_unit"]
HIGH_IMPRESSIONS_THRESHOLD = 1000
LOW_FILL_RATE_THRESHOLD = 0.70
RPM_DROP_THRESHOLD = 0.25
HIGH_CTR_THRESHOLD = 0.10


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect AdOps data and revenue anomalies.")
    parser.add_argument("--input", type=Path, default=DEFAULT_METRICS_PATH, help="Metrics CSV input path.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Anomalies CSV output path.")
    return parser.parse_args()


def add_rolling_rpm_average(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()
    output["date"] = pd.to_datetime(output["date"], errors="coerce")
    output = output.sort_values(GROUP_COLUMNS + ["date"])

    output["rpm_7d_avg"] = output.groupby(GROUP_COLUMNS)["rpm"].transform(
        lambda series: series.shift(1).rolling(window=7, min_periods=3).mean()
    )
    return output


def build_anomaly_rows(
    df: pd.DataFrame,
    mask: pd.Series,
    anomaly_type: str,
    detail_builder: Callable[[pd.Series], str],
) -> pd.DataFrame:
    rows = df.loc[mask].copy()
    if rows.empty:
        return rows

    rows["anomaly_type"] = anomaly_type
    rows["anomaly_detail"] = rows.apply(detail_builder, axis=1)
    return rows


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    working_df = add_rolling_rpm_average(df)

    anomaly_frames = [
        build_anomaly_rows(
            working_df,
            working_df["impressions"] > working_df["matched_requests"],
            "impressions_gt_matched_requests",
            lambda row: (
                f"impressions ({row['impressions']}) is greater than "
                f"matched_requests ({row['matched_requests']})."
            ),
        ),
        build_anomaly_rows(
            working_df,
            working_df["clicks"] > working_df["impressions"],
            "clicks_gt_impressions",
            lambda row: f"clicks ({row['clicks']}) is greater than impressions ({row['impressions']}).",
        ),
        build_anomaly_rows(
            working_df,
            (working_df["estimated_revenue"] == 0)
            & (working_df["impressions"] >= HIGH_IMPRESSIONS_THRESHOLD),
            "zero_revenue_high_impressions",
            lambda row: (
                f"estimated_revenue is zero with {row['impressions']} impressions "
                f"(threshold: {HIGH_IMPRESSIONS_THRESHOLD})."
            ),
        ),
        build_anomaly_rows(
            working_df,
            working_df["fill_rate"] < LOW_FILL_RATE_THRESHOLD,
            "low_fill_rate",
            lambda row: f"fill_rate is {row['fill_rate']:.2%} (threshold: {LOW_FILL_RATE_THRESHOLD:.0%}).",
        ),
        build_anomaly_rows(
            working_df,
            working_df["rpm_7d_avg"].notna()
            & (working_df["rpm"] < working_df["rpm_7d_avg"] * (1 - RPM_DROP_THRESHOLD)),
            "rpm_drop_gt_25pct_vs_7d_avg",
            lambda row: (
                f"rpm is {row['rpm']:.4f}; previous 7-day average is "
                f"{row['rpm_7d_avg']:.4f}."
            ),
        ),
        build_anomaly_rows(
            working_df,
            working_df["ctr"] > HIGH_CTR_THRESHOLD,
            "high_ctr",
            lambda row: f"ctr is {row['ctr']:.2%} (threshold: {HIGH_CTR_THRESHOLD:.0%}).",
        ),
    ]

    populated_frames = [frame for frame in anomaly_frames if not frame.empty]
    if not populated_frames:
        return pd.DataFrame(columns=list(working_df.columns) + ["anomaly_type", "anomaly_detail"])

    anomalies = pd.concat(populated_frames, ignore_index=True)
    anomalies["date"] = pd.to_datetime(anomalies["date"]).dt.strftime("%Y-%m-%d")
    return anomalies.sort_values(["date", "anomaly_type", "site_section", "device"]).reset_index(drop=True)


def save_csv(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def main() -> None:
    args = parse_args()

    try:
        metrics_df = load_csv(args.input)
        anomalies_df = detect_anomalies(metrics_df)
        save_csv(anomalies_df, args.output)
    except Exception as exc:
        raise SystemExit(f"Failed to detect anomalies: {exc}") from exc

    print(f"Detected {len(anomalies_df):,} anomalies at {args.output}")


if __name__ == "__main__":
    main()
