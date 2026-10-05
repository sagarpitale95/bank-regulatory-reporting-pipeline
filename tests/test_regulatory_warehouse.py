import duckdb
import pytest


DATABASE_PATH = "data/warehouse/regulatory_reporting.duckdb"


@pytest.fixture
def connection():
    con = duckdb.connect(DATABASE_PATH)
    yield con
    con.close()


def test_required_tables_exist(connection):
    tables = connection.execute(
        "SHOW TABLES"
    ).fetchdf()["name"].tolist()

    assert "dim_customer" in tables
    assert "dim_risk_category" in tables
    assert "fact_regulatory_loan" in tables


def test_fact_table_has_records(connection):
    result = connection.execute(
        "SELECT COUNT(*) FROM fact_regulatory_loan"
    ).fetchone()[0]

    assert result > 0


def test_loan_ids_are_unique(connection):
    result = connection.execute(
        """
        SELECT loan_id, COUNT(*) AS record_count
        FROM fact_regulatory_loan
        GROUP BY loan_id
        HAVING COUNT(*) > 1
        """
    ).fetchall()

    assert result == []


def test_no_missing_risk_weights(connection):
    result = connection.execute(
        """
        SELECT COUNT(*)
        FROM fact_regulatory_loan
        WHERE risk_weight IS NULL
        """
    ).fetchone()[0]

    assert result == 0


def test_no_missing_rwa(connection):
    result = connection.execute(
        """
        SELECT COUNT(*)
        FROM fact_regulatory_loan
        WHERE rwa IS NULL
        """
    ).fetchone()[0]

    assert result == 0


def test_no_negative_exposure(connection):
    result = connection.execute(
        """
        SELECT COUNT(*)
        FROM fact_regulatory_loan
        WHERE outstanding_amount < 0
        """
    ).fetchone()[0]

    assert result == 0


def test_rwa_calculation(connection):
    result = connection.execute(
        """
        SELECT COUNT(*)
        FROM fact_regulatory_loan
        WHERE ABS(
            rwa - (outstanding_amount * risk_weight)
        ) > 0.01
        """
    ).fetchone()[0]

    assert result == 0


def test_expected_loan_count(connection):
    result = connection.execute(
        """
        SELECT COUNT(*)
        FROM fact_regulatory_loan
        """
    ).fetchone()[0]

    assert result == 9