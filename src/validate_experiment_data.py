from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_FILE = PROJECT_ROOT / "data" / "raw" / "experiment_data.csv"


REQUIRED_COLUMNS = [
    "user_id",
    "experiment_date",
    "experiment_group",
    "device_type",
    "traffic_source",
    "customer_segment",
    "sessions",
    "converted",
    "order_value",
    "revenue",
]

VALID_GROUPS = {
    "Control",
    "Variant_A",
    "Variant_B",
}

VALID_DEVICES = {
    "Mobile",
    "Desktop",
    "Tablet",
}

VALID_TRAFFIC_SOURCES = {
    "Organic",
    "Paid Search",
    "Social",
    "Email",
    "Referral",
}

VALID_SEGMENTS = {
    "New",
    "Returning",
    "Loyal",
}


def validate_experiment_data():
    if not RAW_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_DATA_FILE}"
        )

    df = pd.read_csv(RAW_DATA_FILE)

    print("Starting experiment data validation...")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print()

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df["user_id"].duplicated().any():
        raise ValueError("Duplicate user_id values found.")

    if df["experiment_date"].isna().any():
        raise ValueError("Missing experiment dates found.")

    df["experiment_date"] = pd.to_datetime(
        df["experiment_date"],
        errors="coerce",
    )

    if df["experiment_date"].isna().any():
        raise ValueError("Invalid experiment dates found.")

    if df[REQUIRED_COLUMNS].isna().any().any():
        missing_values = df[REQUIRED_COLUMNS].isna().sum()
        missing_values = missing_values[
            missing_values > 0
        ]

        raise ValueError(
            f"Missing values found:\n{missing_values}"
        )

    invalid_groups = set(
        df["experiment_group"].unique()
    ) - VALID_GROUPS

    if invalid_groups:
        raise ValueError(
            f"Invalid experiment groups: {invalid_groups}"
        )

    invalid_devices = set(
        df["device_type"].unique()
    ) - VALID_DEVICES

    if invalid_devices:
        raise ValueError(
            f"Invalid device types: {invalid_devices}"
        )

    invalid_sources = set(
        df["traffic_source"].unique()
    ) - VALID_TRAFFIC_SOURCES

    if invalid_sources:
        raise ValueError(
            f"Invalid traffic sources: {invalid_sources}"
        )

    invalid_segments = set(
        df["customer_segment"].unique()
    ) - VALID_SEGMENTS

    if invalid_segments:
        raise ValueError(
            f"Invalid customer segments: {invalid_segments}"
        )

    if not df["converted"].isin([0, 1]).all():
        raise ValueError(
            "converted must contain only 0 or 1."
        )

    numeric_columns = [
        "sessions",
        "converted",
        "order_value",
        "revenue",
    ]

    for column in numeric_columns:
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise ValueError(
                f"{column} must be numeric."
            )

    if (df["sessions"] < 1).any():
        raise ValueError(
            "sessions cannot be less than 1."
        )

    if (df["order_value"] < 0).any():
        raise ValueError(
            "order_value cannot be negative."
        )

    if (df["revenue"] < 0).any():
        raise ValueError(
            "revenue cannot be negative."
        )

    revenue_mismatch = ~np.isclose(
        df["revenue"].values,
        np.where(
            df["converted"].values == 1,
            df["order_value"].values,
            0,
        ),
        atol=0.01,
    )

    if revenue_mismatch.any():
        raise ValueError(
            "Revenue consistency check failed."
        )

    group_counts = df["experiment_group"].value_counts()

    if len(group_counts) != 3:
        raise ValueError(
            "Expected exactly three experiment groups."
        )

    print("✓ Required columns check passed")
    print("✓ Duplicate user check passed")
    print("✓ Missing values check passed")
    print("✓ Date validation passed")
    print("✓ Experiment group validation passed")
    print("✓ Device validation passed")
    print("✓ Traffic source validation passed")
    print("✓ Customer segment validation passed")
    print("✓ Conversion validation passed")
    print("✓ Numeric validation passed")
    print("✓ Revenue consistency check passed")
    print()
    print("EXPERIMENT DATA VALIDATION PASSED")


if __name__ == "__main__":
    validate_experiment_data()