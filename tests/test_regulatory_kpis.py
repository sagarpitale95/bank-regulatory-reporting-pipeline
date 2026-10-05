import duckdb


DATABASE_PATH = "data/warehouse/regulatory_reporting.duckdb"


def test_total_rwa_is_positive():
    con = duckdb.connect(DATABASE_PATH)

    result = con.execute("""
        SELECT SUM(rwa)
        FROM fact_regulatory_loan
    """).fetchone()[0]

    con.close()

    assert result > 0


def test_total_exposure_is_positive():
    con = duckdb.connect(DATABASE_PATH)

    result = con.execute("""
        SELECT SUM(outstanding_amount)
        FROM fact_regulatory_loan
    """).fetchone()[0]

    con.close()

    assert result > 0


def test_rwa_does_not_exceed_exposure():
    con = duckdb.connect(DATABASE_PATH)

    result = con.execute("""
        SELECT
            SUM(rwa),
            SUM(outstanding_amount)
        FROM fact_regulatory_loan
    """).fetchone()

    con.close()

    total_rwa, total_exposure = result

    assert total_rwa <= total_exposure


def test_high_risk_rwa_exists():
    con = duckdb.connect(DATABASE_PATH)

    result = con.execute("""
        SELECT SUM(rwa)
        FROM fact_regulatory_loan
        WHERE risk_category = 'HIGH'
    """).fetchone()[0]

    con.close()

    assert result > 0


def test_all_risk_categories_are_valid():
    con = duckdb.connect(DATABASE_PATH)

    result = con.execute("""
        SELECT DISTINCT risk_category
        FROM fact_regulatory_loan
    """).fetchall()

    con.close()

    categories = {row[0] for row in result}

    assert categories.issubset({"LOW", "MEDIUM", "HIGH"})