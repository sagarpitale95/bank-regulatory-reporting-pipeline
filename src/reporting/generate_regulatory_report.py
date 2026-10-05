import duckdb
from pathlib import Path


DATABASE_PATH = "data/warehouse/regulatory_reporting.duckdb"
OUTPUT_PATH = "data/processed/regulatory_kpis.csv"


def generate_report():
    print("Starting regulatory KPI report generation...")

    con = duckdb.connect(DATABASE_PATH)

    query = """
    SELECT
        COUNT(*) AS total_loans,
        ROUND(SUM(outstanding_amount), 2) AS total_exposure,
        ROUND(SUM(rwa), 2) AS total_rwa,
        ROUND(
            SUM(rwa) / NULLIF(SUM(outstanding_amount), 0),
            4
        ) AS average_risk_weight,
        ROUND(
            100.0 * SUM(
                CASE
                    WHEN risk_category = 'HIGH'
                    THEN outstanding_amount
                    ELSE 0
                END
            ) / NULLIF(SUM(outstanding_amount), 0),
            2
        ) AS high_risk_exposure_pct,
        ROUND(
            100.0 * SUM(
                CASE
                    WHEN risk_category = 'HIGH'
                    THEN rwa
                    ELSE 0
                END
            ) / NULLIF(SUM(rwa), 0),
            2
        ) AS high_risk_rwa_pct
    FROM fact_regulatory_loan
    """

    result = con.execute(query).fetchdf()

    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)

    result.to_csv(OUTPUT_PATH, index=False)

    con.close()

    print("REGULATORY KPI REPORT CREATED")
    print(f"Output: {OUTPUT_PATH}")
    print()
    print(result.to_string(index=False))


if __name__ == "__main__":
    generate_report()