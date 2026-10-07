from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_FILE = PROJECT_ROOT / "data" / "raw" / "experiment_data.csv"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def analyze_experiment():
    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = pd.read_csv(RAW_DATA_FILE)

    group_summary = (
        df.groupby("experiment_group")
        .agg(
            users=("user_id", "count"),
            conversions=("converted", "sum"),
            conversion_rate=("converted", "mean"),
            total_revenue=("revenue", "sum"),
            average_order_value=("order_value", "mean"),
            average_sessions=("sessions", "mean"),
        )
        .reset_index()
    )

    group_summary["conversion_rate"] *= 100

    group_summary["revenue_per_user"] = (
        group_summary["total_revenue"]
        / group_summary["users"]
    )

    group_summary["revenue_per_user"] = group_summary[
        "revenue_per_user"
    ].round(2)

    group_summary["total_revenue"] = group_summary[
        "total_revenue"
    ].round(2)

    group_summary["average_order_value"] = group_summary[
        "average_order_value"
    ].round(2)

    group_summary["average_sessions"] = group_summary[
        "average_sessions"
    ].round(2)

    group_summary["conversion_rate"] = group_summary[
        "conversion_rate"
    ].round(2)

    group_summary = group_summary.sort_values(
        "experiment_group"
    )

    output_file = (
        PROCESSED_DATA_DIR
        / "experiment_group_summary.csv"
    )

    group_summary.to_csv(
        output_file,
        index=False,
    )

    control = group_summary[
        group_summary["experiment_group"] == "Control"
    ].iloc[0]

    print("EXPERIMENT GROUP ANALYSIS")
    print("=" * 60)
    print()
    print(group_summary.to_string(index=False))
    print()

    for variant_name in ["Variant_A", "Variant_B"]:
        variant = group_summary[
            group_summary["experiment_group"]
            == variant_name
        ].iloc[0]

        conversion_lift = (
            (
                variant["conversion_rate"]
                - control["conversion_rate"]
            )
            / control["conversion_rate"]
        ) * 100

        revenue_lift = (
            (
                variant["revenue_per_user"]
                - control["revenue_per_user"]
            )
            / control["revenue_per_user"]
        ) * 100

        print(f"{variant_name} vs Control")
        print(
            f"Conversion lift: {conversion_lift:.2f}%"
        )
        print(
            f"Revenue per user lift: {revenue_lift:.2f}%"
        )
        print()

    best_conversion_group = group_summary.loc[
        group_summary["conversion_rate"].idxmax(),
        "experiment_group",
    ]

    best_revenue_group = group_summary.loc[
        group_summary["revenue_per_user"].idxmax(),
        "experiment_group",
    ]

    print(
        f"Best conversion group: {best_conversion_group}"
    )

    print(
        f"Best revenue-per-user group: {best_revenue_group}"
    )

    print()
    print(f"Saved: {output_file}")


if __name__ == "__main__":
    analyze_experiment()