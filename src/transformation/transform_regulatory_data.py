from pathlib import Path

import pandas as pd


PROCESSED_DIR = Path("data/processed")


def load_data() -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    customers = pd.read_parquet(
        PROCESSED_DIR / "customers.parquet"
    )

    accounts = pd.read_parquet(
        PROCESSED_DIR / "accounts.parquet"
    )

    loans = pd.read_parquet(
        PROCESSED_DIR / "loans.parquet"
    )

    risk = pd.read_parquet(
        PROCESSED_DIR / "risk_exposures.parquet"
    )

    return customers, accounts, loans, risk


def transform_regulatory_data(
    customers: pd.DataFrame,
    accounts: pd.DataFrame,
    loans: pd.DataFrame,
    risk: pd.DataFrame,
) -> pd.DataFrame:

    # Join loans with customer information
    regulatory_data = loans.merge(
        customers,
        on="customer_id",
        how="left",
    )

    # Join loans with risk information
    regulatory_data = regulatory_data.merge(
        risk,
        on="loan_id",
        how="left",
    )

    # Calculate Risk-Weighted Assets
    regulatory_data["rwa"] = (
        regulatory_data["outstanding_amount"]
        * regulatory_data["risk_weight"]
    )

    # Add a reporting classification
    regulatory_data["reporting_segment"] = (
        regulatory_data["customer_type"]
        + "_"
        + regulatory_data["loan_type"]
    )

    # Select the final regulatory columns
    regulatory_data = regulatory_data[
        [
            "loan_id",
            "customer_id",
            "customer_name",
            "country",
            "customer_type",
            "loan_type",
            "currency",
            "outstanding_amount",
            "risk_weight",
            "risk_category",
            "rwa",
            "reporting_segment",
        ]
    ]

    return regulatory_data


def main() -> None:

    customers, accounts, loans, risk = load_data()

    regulatory_data = transform_regulatory_data(
        customers,
        accounts,
        loans,
        risk,
    )

    output_path = (
        PROCESSED_DIR / "regulatory_loans.parquet"
    )

    regulatory_data.to_parquet(
        output_path,
        index=False,
    )

    print("REGULATORY TRANSFORMATION COMPLETED")
    print(f"Records created: {len(regulatory_data)}")
    print(f"Output: {output_path}")
    print()
    print("Preview:")
    print(regulatory_data.to_string(index=False))


if __name__ == "__main__":
    main()