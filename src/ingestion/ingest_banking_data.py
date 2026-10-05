from pathlib import Path

import pandas as pd


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


FILES = [
    "customers.csv",
    "accounts.csv",
    "loans.csv",
    "risk_exposures.csv",
]


def ingest_file(filename: str) -> None:
    source_path = RAW_DIR / filename
    output_path = PROCESSED_DIR / filename.replace(".csv", ".parquet")

    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    df = pd.read_csv(source_path)

    df.to_parquet(output_path, index=False)

    print(
        f"INGESTED | {filename} | "
        f"Records: {len(df)} | "
        f"Output: {output_path}"
    )


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    for filename in FILES:
        ingest_file(filename)

    print("Banking data ingestion completed successfully.")


if __name__ == "__main__":
    main()