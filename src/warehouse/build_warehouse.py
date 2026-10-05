from pathlib import Path

import duckdb


PROCESSED_DIR = Path("data/processed")
WAREHOUSE_DIR = Path("data/warehouse")

DATABASE_PATH = WAREHOUSE_DIR / "regulatory_reporting.duckdb"


def main() -> None:
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(DATABASE_PATH))

    regulatory_path = PROCESSED_DIR / "regulatory_loans.parquet"

    # Customer dimension
    con.execute(
        f"""
        CREATE OR REPLACE TABLE dim_customer AS
        SELECT DISTINCT
            customer_id,
            customer_name,
            country,
            customer_type
        FROM read_parquet('{regulatory_path}');
        """
    )

    # Risk dimension
    con.execute(
        f"""
        CREATE OR REPLACE TABLE dim_risk_category AS
        SELECT DISTINCT
            risk_category,
            risk_weight
        FROM read_parquet('{regulatory_path}');
        """
    )

    # Regulatory loan fact table
    con.execute(
        f"""
        CREATE OR REPLACE TABLE fact_regulatory_loan AS
        SELECT
            loan_id,
            customer_id,
            loan_type,
            currency,
            outstanding_amount,
            risk_weight,
            risk_category,
            rwa,
            reporting_segment
        FROM read_parquet('{regulatory_path}');
        """
    )

    print("WAREHOUSE CREATED")
    print(f"Database: {DATABASE_PATH}")

    print()
    print("Tables:")

    tables = con.execute("SHOW TABLES").fetchall()

    for table in tables:
        print(f"- {table[0]}")

    con.close()


if __name__ == "__main__":
    main()