from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "raw" / "adops_performance_raw.csv"

COLUMNS = [
    "date",
    "site_section",
    "device",
    "country",
    "ad_unit",
    "ad_requests",
    "matched_requests",
    "impressions",
    "clicks",
    "estimated_revenue",
]

SITE_SECTIONS = {
    "home": 12000,
    "news": 9000,
    "sports": 7600,
    "technology": 6100,
}
DEVICES = {"mobile": 1.25, "desktop": 0.85, "tablet": 0.35}
COUNTRIES = {"BR": 1.00, "US": 0.65, "MX": 0.42, "AR": 0.35}
AD_UNITS = {
    "top_banner": 1.00,
    "in_article": 0.78,
    "sidebar_rectangle": 0.54,
    "video_preroll": 0.28,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate fictitious AdOps performance data.")
    parser.add_argument("--days", type=int, default=90, help="Number of days to generate.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible data.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="CSV output path.",
    )
    return parser.parse_args()


def build_date_range(days: int) -> list[date]:
    if days < 1:
        raise ValueError("--days must be greater than zero.")

    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=days - 1)
    return [start_date + timedelta(days=offset) for offset in range(days)]


def calculate_requests(
    section_base: int,
    device_factor: float,
    country_factor: float,
    ad_unit_factor: float,
    day_index: int,
    rng: np.random.Generator,
) -> int:
    weekly_cycle = 1 + 0.14 * np.sin((2 * np.pi * day_index) / 7)
    noise = rng.normal(loc=1.0, scale=0.08)
    value = section_base * device_factor * country_factor * ad_unit_factor * weekly_cycle * noise
    return max(120, int(round(value)))


def generate_rows(days: int, seed: int) -> list[dict[str, object]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, object]] = []

    for day_index, current_date in enumerate(build_date_range(days)):
        for site_section, section_base in SITE_SECTIONS.items():
            for device, device_factor in DEVICES.items():
                for country, country_factor in COUNTRIES.items():
                    for ad_unit, ad_unit_factor in AD_UNITS.items():
                        ad_requests = calculate_requests(
                            section_base,
                            device_factor,
                            country_factor,
                            ad_unit_factor,
                            day_index,
                            rng,
                        )
                        match_rate = rng.uniform(0.78, 0.97)
                        fill_rate = rng.uniform(0.76, 0.98)
                        ctr = rng.uniform(0.004, 0.032)

                        if ad_unit == "video_preroll":
                            ctr *= 0.65

                        matched_requests = int(ad_requests * match_rate)
                        impressions = int(matched_requests * fill_rate)
                        clicks = int(impressions * ctr)
                        ecpm = rng.uniform(0.65, 4.25)

                        if country == "US":
                            ecpm *= 1.55
                        if ad_unit == "video_preroll":
                            ecpm *= 1.8

                        estimated_revenue = round((impressions / 1000) * ecpm, 2)

                        rows.append(
                            {
                                "date": current_date.isoformat(),
                                "site_section": site_section,
                                "device": device,
                                "country": country,
                                "ad_unit": ad_unit,
                                "ad_requests": ad_requests,
                                "matched_requests": matched_requests,
                                "impressions": impressions,
                                "clicks": clicks,
                                "estimated_revenue": estimated_revenue,
                            }
                        )

    return rows


def inject_sample_quality_issues(df: pd.DataFrame, seed: int) -> pd.DataFrame:
    """Add realistic data quality issues so the cleaning and anomaly steps have work to do."""
    rng = np.random.default_rng(seed + 1000)
    output = df.copy()
    all_indices = output.index.to_numpy()
    issue_indices = rng.choice(all_indices, size=72, replace=False)

    logical_issue_groups = np.array_split(issue_indices[:48], 6)

    output.loc[logical_issue_groups[0], "impressions"] = (
        output.loc[logical_issue_groups[0], "matched_requests"] + rng.integers(20, 900, size=8)
    )
    output.loc[logical_issue_groups[1], "clicks"] = (
        output.loc[logical_issue_groups[1], "impressions"] + rng.integers(5, 120, size=8)
    )
    output.loc[logical_issue_groups[2], "estimated_revenue"] = 0
    output.loc[logical_issue_groups[3], "impressions"] = (
        output.loc[logical_issue_groups[3], "matched_requests"] * rng.uniform(0.25, 0.58, size=8)
    ).astype(int)
    output.loc[logical_issue_groups[4], "estimated_revenue"] = (
        output.loc[logical_issue_groups[4], "estimated_revenue"] * rng.uniform(0.10, 0.35, size=8)
    ).round(2)
    output.loc[logical_issue_groups[5], "clicks"] = (
        output.loc[logical_issue_groups[5], "impressions"] * rng.uniform(0.12, 0.24, size=8)
    ).astype(int)

    missing_value_indices = issue_indices[48:64]
    output.loc[missing_value_indices[:6], "device"] = None
    output.loc[missing_value_indices[6:12], "clicks"] = None
    output.loc[missing_value_indices[12:], "estimated_revenue"] = None

    duplicate_rows = output.sample(n=16, random_state=seed)
    return pd.concat([output, duplicate_rows], ignore_index=True)


def generate_sample_data(days: int = 90, seed: int = 42) -> pd.DataFrame:
    rows = generate_rows(days=days, seed=seed)
    df = pd.DataFrame(rows, columns=COLUMNS)
    return inject_sample_quality_issues(df, seed=seed)


def save_csv(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def main() -> None:
    args = parse_args()

    try:
        df = generate_sample_data(days=args.days, seed=args.seed)
        save_csv(df, args.output)
    except Exception as exc:
        raise SystemExit(f"Failed to generate sample data: {exc}") from exc

    print(f"Generated {len(df):,} rows at {args.output}")


if __name__ == "__main__":
    main()
