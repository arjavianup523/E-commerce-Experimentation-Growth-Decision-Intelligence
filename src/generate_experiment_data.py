from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

RANDOM_SEED = 42
NUM_USERS = 50000

rng = np.random.default_rng(RANDOM_SEED)


def generate_experiment_data():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    user_ids = np.arange(1, NUM_USERS + 1)

    experiment_groups = rng.choice(
        ["Control", "Variant_A", "Variant_B"],
        size=NUM_USERS,
        p=[0.34, 0.33, 0.33],
    )

    device_types = rng.choice(
        ["Mobile", "Desktop", "Tablet"],
        size=NUM_USERS,
        p=[0.60, 0.32, 0.08],
    )

    traffic_sources = rng.choice(
        ["Organic", "Paid Search", "Social", "Email", "Referral"],
        size=NUM_USERS,
        p=[0.30, 0.25, 0.20, 0.15, 0.10],
    )

    customer_segments = rng.choice(
        ["New", "Returning", "Loyal"],
        size=NUM_USERS,
        p=[0.50, 0.35, 0.15],
    )

    base_conversion_probability = np.select(
        [
            customer_segments == "New",
            customer_segments == "Returning",
            customer_segments == "Loyal",
        ],
        [
            0.055,
            0.095,
            0.145,
        ],
    )

    device_adjustment = np.select(
        [
            device_types == "Mobile",
            device_types == "Desktop",
            device_types == "Tablet",
        ],
        [
            -0.005,
            0.010,
            -0.002,
        ],
    )

    traffic_adjustment = np.select(
        [
            traffic_sources == "Organic",
            traffic_sources == "Paid Search",
            traffic_sources == "Social",
            traffic_sources == "Email",
            traffic_sources == "Referral",
        ],
        [
            0.005,
            0.000,
            -0.003,
            0.012,
            0.008,
        ],
    )

    experiment_effect = np.select(
        [
            experiment_groups == "Control",
            experiment_groups == "Variant_A",
            experiment_groups == "Variant_B",
        ],
        [
            0.000,
            0.010,
            0.018,
        ],
    )

    conversion_probability = (
        base_conversion_probability
        + device_adjustment
        + traffic_adjustment
        + experiment_effect
    )

    conversion_probability = np.clip(
        conversion_probability,
        0.01,
        0.30,
    )

    converted = rng.random(NUM_USERS) < conversion_probability

    order_value = np.where(
        converted,
        rng.lognormal(
            mean=np.log(220),
            sigma=0.45,
            size=NUM_USERS,
        ),
        0,
    )

    sessions = rng.poisson(
        lam=np.where(
            customer_segments == "New",
            1.4,
            np.where(
                customer_segments == "Returning",
                2.1,
                3.0,
            ),
        )
    ) + 1

    experiment_date = pd.to_datetime("2026-01-01") + pd.to_timedelta(
        rng.integers(
            0,
            90,
            size=NUM_USERS,
        ),
        unit="D",
    )

    revenue = np.where(
        converted,
        order_value,
        0,
    )

    data = pd.DataFrame(
        {
            "user_id": user_ids,
            "experiment_date": experiment_date,
            "experiment_group": experiment_groups,
            "device_type": device_types,
            "traffic_source": traffic_sources,
            "customer_segment": customer_segments,
            "sessions": sessions,
            "converted": converted.astype(int),
            "order_value": np.round(order_value, 2),
            "revenue": np.round(revenue, 2),
        }
    )

    output_path = RAW_DATA_DIR / "experiment_data.csv"

    data.to_csv(
        output_path,
        index=False,
    )

    print("EXPERIMENT DATA GENERATED")
    print(f"Rows: {len(data):,}")
    print(f"Columns: {len(data.columns)}")
    print(f"Output: {output_path}")
    print()
    print("Experiment groups:")
    print(data["experiment_group"].value_counts())
    print()
    print("Overall conversion rate:")
    print(f"{data['converted'].mean():.2%}")
    print()
    print("Total revenue:")
    print(f"₹{data['revenue'].sum():,.2f}")


if __name__ == "__main__":
    generate_experiment_data()