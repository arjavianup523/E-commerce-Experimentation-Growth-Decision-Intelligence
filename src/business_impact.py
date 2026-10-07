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
    / "business_impact.csv"
)


GUARDRAIL_REVENUE_TOLERANCE = -0.05
GUARDRAIL_AOV_TOLERANCE = -0.05
GUARDRAIL_SESSION_TOLERANCE = -0.05


def calculate_group_metrics(df):
    result = (
        df.groupby("experiment_group")
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

    result["conversion_rate"] = (
        result["conversions"]
        / result["users"]
    )

    result["revenue_per_user"] = (
        result["total_revenue"]
        / result["users"]
    )

    return result


def main():
    df = pd.read_csv(INPUT_FILE)

    metrics = calculate_group_metrics(df)

    control = metrics[
        metrics["experiment_group"]
        == "Control"
    ].iloc[0]

    results = []

    for _, variant in metrics.iterrows():

        if variant["experiment_group"] == "Control":
            continue

        revenue_lift = (
            variant["revenue_per_user"]
            / control["revenue_per_user"]
        ) - 1

        aov_lift = (
            variant["average_order_value"]
            / control["average_order_value"]
        ) - 1

        session_lift = (
            variant["average_sessions"]
            / control["average_sessions"]
        ) - 1

        conversion_lift = (
            variant["conversion_rate"]
            / control["conversion_rate"]
        ) - 1

        revenue_impact = (
            variant["revenue_per_user"]
            - control["revenue_per_user"]
        ) * variant["users"]

        revenue_guardrail = (
            revenue_lift
            >= GUARDRAIL_REVENUE_TOLERANCE
        )

        aov_guardrail = (
            aov_lift
            >= GUARDRAIL_AOV_TOLERANCE
        )

        session_guardrail = (
            session_lift
            >= GUARDRAIL_SESSION_TOLERANCE
        )

        all_guardrails_pass = (
            revenue_guardrail
            and aov_guardrail
            and session_guardrail
        )

        results.append(
            {
                "variant": variant[
                    "experiment_group"
                ],
                "control_conversion_rate": (
                    control["conversion_rate"]
                ),
                "variant_conversion_rate": (
                    variant["conversion_rate"]
                ),
                "conversion_lift": (
                    conversion_lift
                ),
                "control_revenue_per_user": (
                    control["revenue_per_user"]
                ),
                "variant_revenue_per_user": (
                    variant["revenue_per_user"]
                ),
                "revenue_per_user_lift": (
                    revenue_lift
                ),
                "estimated_revenue_impact": (
                    revenue_impact
                ),
                "average_order_value_lift": (
                    aov_lift
                ),
                "average_sessions_lift": (
                    session_lift
                ),
                "revenue_guardrail_pass": (
                    revenue_guardrail
                ),
                "aov_guardrail_pass": (
                    aov_guardrail
                ),
                "session_guardrail_pass": (
                    session_guardrail
                ),
                "all_guardrails_pass": (
                    all_guardrails_pass
                ),
            }
        )

    results_df = pd.DataFrame(results)

    percentage_columns = [
        "control_conversion_rate",
        "variant_conversion_rate",
        "conversion_lift",
        "revenue_per_user_lift",
        "average_order_value_lift",
        "average_sessions_lift",
    ]

    for column in percentage_columns:
        results_df[column] *= 100

    results_df = results_df.round(
        {
            column: 2
            for column in percentage_columns
        }
        | {
            "control_revenue_per_user": 2,
            "variant_revenue_per_user": 2,
            "estimated_revenue_impact": 2,
        }
    )

    results_df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("=" * 70)
    print("BUSINESS IMPACT & GUARDRAIL ANALYSIS")
    print("=" * 70)
    print()

    for _, row in results_df.iterrows():

        print(
            f"{row['variant']} vs Control"
        )

        print(
            f"Conversion lift: "
            f"{row['conversion_lift']:.2f}%"
        )

        print(
            f"Revenue/user lift: "
            f"{row['revenue_per_user_lift']:.2f}%"
        )

        print(
            f"Estimated revenue impact: "
            f"{row['estimated_revenue_impact']:.2f}"
        )

        print(
            f"AOV guardrail: "
            f"{'PASS' if row['aov_guardrail_pass'] else 'FAIL'}"
        )

        print(
            f"Session guardrail: "
            f"{'PASS' if row['session_guardrail_pass'] else 'FAIL'}"
        )

        print(
            f"Revenue guardrail: "
            f"{'PASS' if row['revenue_guardrail_pass'] else 'FAIL'}"
        )

        print(
            f"All guardrails: "
            f"{'PASS' if row['all_guardrails_pass'] else 'FAIL'}"
        )

        print()

    print(
        f"Saved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()