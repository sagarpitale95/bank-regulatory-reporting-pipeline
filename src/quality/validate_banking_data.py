from pathlib import Path

import pandas as pd


PROCESSED_DIR = Path("data/processed")


def validate_customers(df: pd.DataFrame) -> list[str]:
    errors = []

    required_columns = [
        "customer_id",
        "customer_name",
        "country",
        "customer_type",
    ]

    for column in required_columns:
        if column not in df.columns:
            errors.append(f"Missing customer column: {column}")

    if "customer_id" in df.columns:
        if df["customer_id"].isna().any():
            errors.append("Customer ID contains null values.")

        if df["customer_id"].duplicated().any():
            errors.append("Duplicate customer IDs found.")

    if "customer_type" in df.columns:
        allowed_types = {"RETAIL", "CORPORATE"}

        invalid_types = set(df["customer_type"].dropna()) - allowed_types

        if invalid_types:
            errors.append(
                f"Invalid customer types found: {invalid_types}"
            )

    return errors


def validate_accounts(df: pd.DataFrame) -> list[str]:
    errors = []

    required_columns = [
        "account_id",
        "customer_id",
        "account_type",
        "currency",
        "balance",
    ]

    for column in required_columns:
        if column not in df.columns:
            errors.append(f"Missing account column: {column}")

    if "account_id" in df.columns:
        if df["account_id"].isna().any():
            errors.append("Account ID contains null values.")

        if df["account_id"].duplicated().any():
            errors.append("Duplicate account IDs found.")

    if "balance" in df.columns:
        if (df["balance"] < 0).any():
            errors.append("Account balance contains negative values.")

    return errors


def validate_loans(df: pd.DataFrame) -> list[str]:
    errors = []

    required_columns = [
        "loan_id",
        "customer_id",
        "loan_type",
        "outstanding_amount",
        "currency",
    ]

    for column in required_columns:
        if column not in df.columns:
            errors.append(f"Missing loan column: {column}")

    if "loan_id" in df.columns:
        if df["loan_id"].isna().any():
            errors.append("Loan ID contains null values.")

        if df["loan_id"].duplicated().any():
            errors.append("Duplicate loan IDs found.")

    if "outstanding_amount" in df.columns:
        if (df["outstanding_amount"] < 0).any():
            errors.append("Loan amount contains negative values.")

    return errors


def validate_risk(df: pd.DataFrame) -> list[str]:
    errors = []

    required_columns = [
        "loan_id",
        "risk_weight",
        "risk_category",
    ]

    for column in required_columns:
        if column not in df.columns:
            errors.append(f"Missing risk column: {column}")

    if "loan_id" in df.columns:
        if df["loan_id"].isna().any():
            errors.append("Risk data contains null loan IDs.")

        if df["loan_id"].duplicated().any():
            errors.append("Duplicate risk loan IDs found.")

    if "risk_weight" in df.columns:
        if ((df["risk_weight"] < 0) | (df["risk_weight"] > 1)).any():
            errors.append("Risk weight must be between 0 and 1.")

    return errors


def validate_referential_integrity(
    customers: pd.DataFrame,
    accounts: pd.DataFrame,
    loans: pd.DataFrame,
    risk: pd.DataFrame,
) -> list[str]:
    errors = []

    customer_ids = set(customers["customer_id"].dropna())
    loan_ids = set(loans["loan_id"].dropna())

    invalid_account_customers = (
        set(accounts["customer_id"].dropna()) - customer_ids
    )

    if invalid_account_customers:
        errors.append(
            "Accounts reference unknown customers: "
            f"{invalid_account_customers}"
        )

    invalid_loan_customers = (
        set(loans["customer_id"].dropna()) - customer_ids
    )

    if invalid_loan_customers:
        errors.append(
            "Loans reference unknown customers: "
            f"{invalid_loan_customers}"
        )

    invalid_risk_loans = (
        set(risk["loan_id"].dropna()) - loan_ids
    )

    if invalid_risk_loans:
        errors.append(
            "Risk records reference unknown loans: "
            f"{invalid_risk_loans}"
        )

    return errors


def load_parquet(filename: str) -> pd.DataFrame:
    path = PROCESSED_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    return pd.read_parquet(path)


def main() -> None:
    customers = load_parquet("customers.parquet")
    accounts = load_parquet("accounts.parquet")
    loans = load_parquet("loans.parquet")
    risk = load_parquet("risk_exposures.parquet")

    all_errors = []

    all_errors.extend(validate_customers(customers))
    all_errors.extend(validate_accounts(accounts))
    all_errors.extend(validate_loans(loans))
    all_errors.extend(validate_risk(risk))

    all_errors.extend(
        validate_referential_integrity(
            customers,
            accounts,
            loans,
            risk,
        )
    )

    if all_errors:
        print("DATA QUALITY FAILED")

        for error in all_errors:
            print(f"- {error}")

        raise SystemExit(1)

    print("DATA QUALITY PASSED")
    print(f"Customers checked: {len(customers)}")
    print(f"Accounts checked: {len(accounts)}")
    print(f"Loans checked: {len(loans)}")
    print(f"Risk records checked: {len(risk)}")


if __name__ == "__main__":
    main()