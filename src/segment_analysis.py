from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "experiment_data.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "segment_analysis.csv"
)


SEGMENT_COLUMNS = [
    "device_type",
    "traffic_source",
    "customer_segment",
]


def calculate_segment_metrics(
    df,
    segment_column,
):
    grouped = (
        df.groupby(
            [
                segment_column,
                "experiment_group",
            ]
        )
        .agg(
            users=("user_id", "count"),
            conversions=("converted", "sum"),
            total_revenue=("revenue", "sum"),
            average_order_value=(
                "order_value",
                "mean",
            ),
            average_sessions=(
                "sessions",
                "mean",
            ),
        )
        .reset_index()
    )

    grouped["conversion_rate"] = (
        grouped["conversions"]
        / grouped["users"]
    )

    grouped["revenue_per_user"] = (
        grouped["total_revenue"]
        / grouped["users"]
    )

    grouped["segment_type"] = (
        segment_column
    )

    grouped = grouped.rename(
        columns={
            segment_column: "segment",
        }
    )

    return grouped


def main():
    df = pd.read_csv(INPUT_FILE)

    all_results = []

    for segment_column in SEGMENT_COLUMNS:
        result = calculate_segment_metrics(
            df,
            segment_column,
        )

        all_results.append(result)

    results = pd.concat(
        all_results,
        ignore_index=True,
    )

    results["conversion_rate"] *= 100

    results = results.round(
        {
            "conversion_rate": 2,
            "revenue_per_user": 2,
            "average_order_value": 2,
            "average_sessions": 2,
        }
    )

    results.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("=" * 70)
    print("SEGMENT ANALYSIS")
    print("=" * 70)
    print()

    for segment_type in results[
        "segment_type"
    ].unique():

        print(
            f"--- {segment_type.upper()} ---"
        )

        segment_results = results[
            results["segment_type"]
            == segment_type
        ]

        print(
            segment_results[
                [
                    "segment",
                    "experiment_group",
                    "users",
                    "conversion_rate",
                    "revenue_per_user",
                ]
            ].to_string(index=False)
        )

        print()

    print(
        f"Saved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()