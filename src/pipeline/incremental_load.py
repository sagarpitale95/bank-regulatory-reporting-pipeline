import duckdb
from pathlib import Path


DATABASE_PATH = "data/warehouse/regulatory_reporting.duckdb"
PROCESSED_DATA_PATH = "data/processed"


def get_database_connection():
    """Create a connection to the regulatory warehouse."""
    return duckdb.connect(DATABASE_PATH)


def get_processed_files():
    """Return processed parquet files available for loading."""
    path = Path(PROCESSED_DATA_PATH)

    return sorted(
        path.glob("*.parquet")
    )


def get_row_count(con):
    """Return current warehouse fact-table row count."""
    return con.execute(
        "SELECT COUNT(*) FROM fact_regulatory_loan"
    ).fetchone()[0]


def run_incremental_check():
    """Check available processed data before an incremental load."""

    print("Starting incremental load check...")

    con = get_database_connection()

    before_count = get_row_count(con)

    files = get_processed_files()

    print(f"Current warehouse rows: {before_count}")
    print(f"Processed Parquet files found: {len(files)}")

    for file in files:
        print(f"  - {file}")

    con.close()

    print("Incremental load check completed.")


if __name__ == "__main__":
    run_incremental_check()