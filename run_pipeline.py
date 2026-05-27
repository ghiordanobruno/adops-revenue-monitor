from __future__ import annotations

import argparse

from calculate_metrics import DEFAULT_OUTPUT as METRICS_PATH, calculate_metrics, save_csv as save_metrics
from clean_data import DEFAULT_OUTPUT as CLEAN_PATH, clean_data, load_csv, save_csv as save_clean
from detect_anomalies import DEFAULT_OUTPUT as ANOMALIES_PATH, detect_anomalies, save_csv as save_anomalies
from export_dashboard import DEFAULT_OUTPUT as DASHBOARD_PATH, export_dashboard
from generate_sample_data import DEFAULT_OUTPUT as RAW_PATH, generate_sample_data, save_csv as save_raw


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the full AdOps revenue monitor pipeline.")
    parser.add_argument("--days", type=int, default=90, help="Number of days to generate.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible data.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        raw_df = generate_sample_data(days=args.days, seed=args.seed)
        save_raw(raw_df, RAW_PATH)

        clean_df = clean_data(load_csv(RAW_PATH))
        save_clean(clean_df, CLEAN_PATH)

        metrics_df = calculate_metrics(load_csv(CLEAN_PATH))
        save_metrics(metrics_df, METRICS_PATH)

        anomalies_df = detect_anomalies(load_csv(METRICS_PATH))
        save_anomalies(anomalies_df, ANOMALIES_PATH)

        export_dashboard(raw_df, clean_df, metrics_df, anomalies_df, DASHBOARD_PATH)
    except Exception as exc:
        raise SystemExit(f"Pipeline failed: {exc}") from exc

    print("Pipeline finished successfully.")
    print(f"Raw data: {RAW_PATH}")
    print(f"Clean data: {CLEAN_PATH}")
    print(f"Metrics: {METRICS_PATH}")
    print(f"Anomalies: {ANOMALIES_PATH}")
    print(f"Dashboard: {DASHBOARD_PATH}")


if __name__ == "__main__":
    main()
