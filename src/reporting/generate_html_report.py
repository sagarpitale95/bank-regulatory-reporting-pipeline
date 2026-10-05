import duckdb
from pathlib import Path
from datetime import datetime


DATABASE_PATH = "data/warehouse/regulatory_reporting.duckdb"
OUTPUT_PATH = "data/processed/regulatory_report.html"


def generate_report():
    con = duckdb.connect(DATABASE_PATH)

    # Overall KPIs
    kpi = con.execute("""
        SELECT
            COUNT(*) AS total_loans,
            SUM(outstanding_amount) AS total_exposure,
            SUM(rwa) AS total_rwa,
            SUM(rwa) / NULLIF(SUM(outstanding_amount), 0)
                AS average_risk_weight
        FROM fact_regulatory_loan
    """).fetchone()

    total_loans, total_exposure, total_rwa, average_risk_weight = kpi

    # RWA by risk category
    risk_data = con.execute("""
        SELECT
            risk_category,
            COUNT(*) AS loan_count,
            SUM(outstanding_amount) AS exposure,
            SUM(rwa) AS rwa
        FROM fact_regulatory_loan
        GROUP BY risk_category
        ORDER BY rwa DESC
    """).fetchall()

    # RWA by customer type
    customer_data = con.execute("""
        SELECT
            c.customer_type,
            COUNT(*) AS loan_count,
            SUM(f.outstanding_amount) AS exposure,
            SUM(f.rwa) AS rwa
        FROM fact_regulatory_loan f
        JOIN dim_customer c
            ON f.customer_id = c.customer_id
        GROUP BY c.customer_type
        ORDER BY rwa DESC
    """).fetchall()

    con.close()

    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)

    risk_rows = ""

    for row in risk_data:
        risk_rows += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>€{row[2]:,.2f}</td>
            <td>€{row[3]:,.2f}</td>
        </tr>
        """

    customer_rows = ""

    for row in customer_data:
        customer_rows += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>€{row[2]:,.2f}</td>
            <td>€{row[3]:,.2f}</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Regulatory Reporting Dashboard</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f5f7fa;
        }}

        h1 {{
            margin-bottom: 5px;
        }}

        .subtitle {{
            color: #666;
            margin-bottom: 30px;
        }}

        .cards {{
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
        }}

        .card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            min-width: 200px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}

        .card h3 {{
            margin-top: 0;
            color: #555;
        }}

        .value {{
            font-size: 26px;
            font-weight: bold;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            margin-bottom: 30px;
        }}

        th, td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
            text-align: left;
        }}

        th {{
            background: #eeeeee;
        }}

        .section {{
            margin-top: 35px;
        }}
    </style>
</head>

<body>

<h1>Bank Regulatory Reporting Dashboard</h1>

<p class="subtitle">
    Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
</p>

<div class="cards">

    <div class="card">
        <h3>Total Loans</h3>
        <div class="value">{total_loans}</div>
    </div>

    <div class="card">
        <h3>Total Exposure</h3>
        <div class="value">€{total_exposure:,.0f}</div>
    </div>

    <div class="card">
        <h3>Total RWA</h3>
        <div class="value">€{total_rwa:,.0f}</div>
    </div>

    <div class="card">
        <h3>Average Risk Weight</h3>
        <div class="value">
            {average_risk_weight:.2%}
        </div>
    </div>

</div>


<div class="section">

<h2>RWA by Risk Category</h2>

<table>

<tr>
    <th>Risk Category</th>
    <th>Loan Count</th>
    <th>Exposure</th>
    <th>RWA</th>
</tr>

{risk_rows}

</table>

</div>


<div class="section">

<h2>RWA by Customer Type</h2>

<table>

<tr>
    <th>Customer Type</th>
    <th>Loan Count</th>
    <th>Exposure</th>
    <th>RWA</th>
</tr>

{customer_rows}

</table>

</div>

</body>
</html>
"""

    Path(OUTPUT_PATH).write_text(html, encoding="utf-8")

    print("REGULATORY HTML REPORT CREATED")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_report()