from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

STATISTICAL_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "multiple_testing_results.csv"
)

BUSINESS_IMPACT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "business_impact.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "experiment_decision.csv"
)


def make_decision(
    statistical_row,
    business_row,
):
    conversion_lift = (
        statistical_row[
            "relative_conversion_lift"
        ]
    )

    statistically_significant = (
        statistical_row[
            "significant_after_holm"
        ]
    )

    guardrails_pass = (
        business_row[
            "all_guardrails_pass"
        ]
    )

    if (
        conversion_lift < 0
        and statistically_significant
    ):
        return (
            "STOP",
            "Statistically significant negative "
            "conversion impact.",
        )

    if not guardrails_pass:
        return (
            "STOP",
            "One or more business guardrails failed.",
        )

    if (
        statistically_significant
        and conversion_lift > 0
    ):
        return (
            "SHIP",
            "Statistically significant positive "
            "conversion impact and all guardrails passed.",
        )

    if conversion_lift > 0:
        return (
            "ITERATE",
            "Positive conversion movement, but "
            "statistical evidence is insufficient.",
        )

    return (
        "ITERATE",
        "No convincing positive business impact.",
    )


def main():
    statistical_df = pd.read_csv(
        STATISTICAL_FILE
    )

    business_df = pd.read_csv(
        BUSINESS_IMPACT_FILE
    )

    results = []

    for _, statistical_row in statistical_df.iterrows():

        variant = statistical_row[
            "variant"
        ]

        business_matches = business_df[
            business_df["variant"]
            == variant
        ]

        if business_matches.empty:
            continue

        business_row = (
            business_matches.iloc[0]
        )

        decision, reason = make_decision(
            statistical_row,
            business_row,
        )

        results.append(
            {
                "variant": variant,
                "conversion_lift": (
                    statistical_row[
                        "relative_conversion_lift"
                    ]
                ),
                "adjusted_p_value": (
                    statistical_row[
                        "holm_adjusted_p_value"
                    ]
                ),
                "statistically_significant": (
                    statistical_row[
                        "significant_after_holm"
                    ]
                ),
                "revenue_per_user_lift": (
                    business_row[
                        "revenue_per_user_lift"
                    ]
                ),
                "estimated_revenue_impact": (
                    business_row[
                        "estimated_revenue_impact"
                    ]
                ),
                "guardrails_pass": (
                    business_row[
                        "all_guardrails_pass"
                    ]
                ),
                "decision": decision,
                "decision_reason": reason,
            }
        )

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("=" * 70)
    print("EXPERIMENT DECISION ENGINE")
    print("=" * 70)
    print()

    for _, row in results_df.iterrows():

        print(
            f"{row['variant']}: "
            f"{row['decision']}"
        )

        print(
            f"Conversion lift: "
            f"{row['conversion_lift']:.2f}%"
        )

        print(
            f"Adjusted p-value: "
            f"{row['adjusted_p_value']:.8f}"
        )

        print(
            f"Revenue/user lift: "
            f"{row['revenue_per_user_lift']:.2f}%"
        )

        print(
            f"Guardrails: "
            f"{'PASS' if row['guardrails_pass'] else 'FAIL'}"
        )

        print(
            f"Reason: "
            f"{row['decision_reason']}"
        )

        print()

    print(
        f"Saved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()