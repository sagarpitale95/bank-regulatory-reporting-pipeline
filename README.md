# Bank Regulatory Reporting Data Pipeline

<p align="center">
  <strong>Beginner-friendly, end-to-end Data Engineering project for banking regulatory reporting</strong><br>
  <sub>Python  SQL  DuckDB  Parquet  Pytest  GitHub Actions  HTML Reporting</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/SQL-Analytics-F29111">
  <img src="https://img.shields.io/badge/DuckDB-Warehouse-FFF000">
  <img src="https://img.shields.io/badge/Parquet-Storage-50ABF1">
  <img src="https://img.shields.io/badge/Pytest-Testing-0A9EDC?logo=pytest&logoColor=white">
  <img src="https://img.shields.io/badge/GitHub_Actions-CI-2088FF?logo=githubactions&logoColor=white">
</p>

---

## Overview

This project simulates a simplified **banking regulatory reporting pipeline**.

```text
Raw CSV
  v
Validation
  v
Transformation
  v
Parquet
  v
DuckDB Warehouse
  v
Fact + Dimension Model
  v
Regulatory KPIs / RWA
  v
Automated Tests
  v
CSV + HTML Reports
  v
GitHub Actions CI
```

It is intentionally designed to run **locally and for free**, so beginners can learn the fundamentals before moving to AWS, Azure, Spark or Databricks.

> WARNING: **Educational only:** The banking data, risk weights and calculations are simplified examples. They are not suitable for real regulatory submissions, capital decisions or compliance reporting.

---

## What You Learn

| Area | Learning |
|---|---|
|  Python | Data processing and automation |
|  SQL | Analytical and regulatory queries |
|  Pandas | Transformations |
|  Parquet | Columnar data storage |
|  DuckDB | Local analytical warehouse |
|  Data Modelling | Facts, dimensions and star schemas |
|  Data Quality | Validation and business rules |
|  Pytest | Automated testing |
|  Reporting | KPI, CSV and HTML outputs |
|  Git | Version control |
|  GitHub Actions | Continuous Integration |
|  Cloud | AWS/Azure architecture concepts |
|  Big Data | Spark/Databricks concepts |

---

##  Technology Stack

**Core:** Python 3.11+, Pandas, SQL, DuckDB, Parquet

**Engineering:** Pytest, Git, GitHub, GitHub Actions

**Reporting:** CSV, HTML

**Optional extensions:** PySpark, Databricks, AWS S3/Glue/Athena/Redshift, Azure Data Lake/Data Factory/Databricks/Synapse, Power BI, Airflow

---

##  Project Structure

```text
bank-regulatory-reporting-pipeline/
|
|--- config/
|--- data/
|   |--- raw/
|   |--- processed/
|   `--- warehouse/
|--- sql/
|--- src/
|   |--- pipeline/
|   |--- reporting/
|   `--- warehouse/
|--- tests/
|--- .github/
|   `--- workflows/
|--- .gitignore
|--- requirements.txt
`--- README.md
```

> The exact filenames in the repository are the source of truth. If your checkout uses a different filename, use that filename in the command.

---

#  Quick Start

## 1. Prerequisites

Install:

- Python **3.11+**
- Git
- PowerShell (Windows) or another terminal

No paid cloud account is required.

---

## 2. Clone

```powershell
git clone https://github.com/sagarpitale95/bank-regulatory-reporting-pipeline.git
cd bank-regulatory-reporting-pipeline
```

If you already have the repository locally, open the terminal in the project folder.

---

## 3. Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` in the terminal.

---

## 4. Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 5. Run Tests

Always test the environment first:

```powershell
python -m pytest -v
```

The expected outcome is that the test suite passes. The exact number of tests may change as the project evolves.

---

## 6. Build the Warehouse

```powershell
python src\warehouseuild_warehouse.py
```

This builds/updates the local DuckDB warehouse using the project's configured data.

---

## 7. Generate KPI Output

```powershell
python src
eporting\generate_regulatory_report.py
```

The KPI output is generated under the project's processed-data directory.

---

## 8. Generate the HTML Report

```powershell
python src
eporting\generate_html_report.py
```

If the generated file is:

```text
data/processed/regulatory_report.html
```

open it with:

```powershell
Start-Process .\data\processed
egulatory_report.html
```

---

## 9. Inspect DuckDB

If the warehouse file is:

```text
data/warehouse/regulatory_reporting.duckdb
```

run:

```powershell
python -c "import duckdb; con=duckdb.connect('data/warehouse/regulatory_reporting.duckdb'); print(con.execute('SHOW TABLES').fetchall()); con.close()"
```

If your repository uses a different database filename, use that filename instead.

---

#  Architecture

```text
                  .---------------------.
                  |   Raw Loan Data   |
                  |       CSV         |
                  `--------------------'-
                            v
                  .---------------------.
                  | Data Validation   |
                  | Python / Pytest   |
                  `--------------------'-
                            v
                  .---------------------.
                  | Transformation    |
                  | Python / Pandas   |
                  `--------------------'-
                            v
                  .---------------------.
                  |     Parquet       |
                  `--------------------'-
                            v
                  .---------------------.
                  | DuckDB Warehouse  |
                  `--------------------'-
                            v
                 .------------------------.
                 | Fact + Dimensions    |
                 `-----------------------'-
                            v
                 .------------------------.
                 | Regulatory SQL/KPIs  |
                 `-----------------------'-
                            v
                  .---------------------.
                  v                   v
             CSV Report          HTML Report
                            v
                    GitHub Actions CI
```

---

#  Data Model

The project introduces a simplified **star schema**.

### `dim_customer`

Typical descriptive fields:

```text
customer_id
customer_name
customer_type
country
```

### `dim_risk_category`

Typical risk information:

```text
risk_category
risk_weight
description
```

### `fact_regulatory_loan`

Typical measurable loan fields:

```text
loan_id
customer_id
loan_type
outstanding_amount
risk_weight
risk_category
rwa
```

Conceptually:

```text
dim_customer -------.
                    |--- fact_regulatory_loan
dim_risk_category -'-
```

---

#  Simplified RWA Calculation

The project demonstrates:

```text
RWA = Outstanding Exposure  Risk Weight
```

Example:

```text
Exposure    = 100,000
Risk Weight = 50%

RWA = 100,000  50%
    = 50,000
```

This is intentionally simplified for learning.

---

#  Example KPIs

The reporting layer can calculate:

- Total loans
- Total exposure
- Total RWA
- Average risk weight
- High-risk exposure %
- High-risk RWA %
- RWA by customer type
- RWA by risk category

---

#  Data Quality

Typical controls include:

```text
[OK] Required fields exist
[OK] Loan IDs are present
[OK] Customer IDs are valid
[OK] Exposure is not negative
[OK] Risk weights are valid
[OK] Risk categories are recognised
[OK] Duplicate records are detected
[OK] RWA calculations are consistent
```

Use the test suite to prove the rules work.

---

#  Testing

Run:

```powershell
python -m pytest -v
```

A useful learning exercise:

1. Add an invalid record.
2. Run the tests.
3. Observe the failure.
4. Investigate why it failed.
5. Fix the data.
6. Run the tests again.

This teaches:

```text
Change -> Test -> Fail/Pass -> Investigate -> Fix -> Improve
```

---

#  GitHub Actions

The repository uses CI to automatically validate changes.

```text
git push
   v
GitHub
   v
GitHub Actions
   v
Install dependencies
   v
Run tests
   v
PASS / FAIL
```

This introduces Continuous Integration and automated quality gates.

---

#  Extensions

## 1. Incremental Processing

Instead of processing everything every time:

```text
Existing Data + New Records
            v
      Incremental Load
            v
       Updated Data
```

Learn:

- Business keys
- Duplicate prevention
- Incremental loading
- Idempotency

**Challenge:** Run the pipeline twice without creating duplicate business records.

---

## 2. Audit Logging

Create an audit table with:

```text
run_id
pipeline_name
start_time
end_time
records_read
records_processed
records_rejected
status
error_message
```

Goal:

> Be able to explain exactly what happened during every pipeline run.

---

## 3. Data Lineage

Trace:

```text
Report
 v
KPI
 v
SQL
 v
Warehouse Table
 v
Processed Data
 v
Raw Source
```

This introduces traceability and governance.

---

## 4. Slowly Changing Dimensions

Preserve historical customer changes:

```text
Customer A | Ireland | 2024-01-01 -> 2025-06-30
Customer A | UK      | 2025-07-01 -> Current
```

Explore SCD Type 1 and Type 2.

---

## 5. Bronze -> Silver -> Gold

Modernise the pipeline:

```text
Raw Source
    v
 BRONZE       Raw
    v
 SILVER       Cleaned / validated
    v
 GOLD         Business-ready
    v
Regulatory Reporting
```

This is a strong bridge to lakehouse architecture.

---

#  AWS Bonus

Possible cloud version:

```text
Source
  v
Amazon S3
  v
AWS Glue / Spark
  v
Parquet
  v
Amazon Athena / Redshift
  v
Reporting
```

Explore:

- Amazon S3
- AWS Glue
- Amazon Athena
- Amazon Redshift
- AWS Lake Formation
- Amazon CloudWatch

**Challenge:** Put processed Parquet data into S3 and query it with Athena.

---

#  Azure Bonus

Possible Azure version:

```text
Source
  v
Azure Data Lake Storage
  v
Azure Data Factory
  v
Databricks / Spark
  v
Delta Lake
  v
Synapse / Databricks SQL
  v
Power BI
```

Explore:

- ADLS Gen2
- Azure Data Factory
- Azure Databricks
- Azure Synapse
- Power BI
- Microsoft Purview

---

#  Spark / PySpark Bonus

After understanding the Pandas pipeline, try PySpark:

```text
Pandas
  v
PySpark
  v
Distributed Processing
```

Example:

```python
df = spark.read.parquet("data/processed/")

result = (
    df.groupBy("risk_category")
      .sum("rwa")
)
```

Learn **when** distributed processing is useful, not just how to use Spark.

---

#  Databricks Bonus

A possible lakehouse version:

```text
Cloud Storage
      v
Databricks
      v
Spark
      v
Delta Lake
      v
Databricks SQL
      v
BI / Reporting
```

This introduces:

- Spark
- Delta Lake
- Lakehouse architecture
- Databricks SQL
- Cloud Data Engineering

---

#  AI Bonus

Once the traditional pipeline works, experiment with AI.

### Anomaly Detection

Look for unusual:

```text
Exposure changes
RWA changes
Risk weights
Portfolio concentration
```

### Natural-Language Analytics

Future flow:

```text
User Question
      v
AI
      v
SQL
      v
Warehouse
      v
Result
      v
Answer
```

### Regulatory Document RAG

```text
Public Documents
      v
Chunking
      v
Embeddings
      v
Vector Search
      v
RAG
      v
Question Answering
```

AI should support analysis; it should not bypass data controls or regulatory expertise.

---

#  Banking Extensions

Try adding:

### Credit Risk

Simplified concepts:

```text
Probability of Default
Loss Given Default
Exposure at Default
Expected Loss
```

### Portfolio Concentration

```text
RWA by Country
RWA by Sector
RWA by Product
RWA by Customer Type
```

### Stress Testing

Create simplified:

```text
BASE
ADVERSE
SEVERE
```

scenarios and compare exposure/RWA outcomes.

---

#  Beginner Challenge Ladder

| Level | Challenge |
|---|---|
| [LEVEL 1] Beginner | Add customer segment, maturity, interest rate and new KPIs |
| [LEVEL 2] Intermediate | Add country, sector and currency analysis |
| [LEVEL 3] Advanced | Incremental loading, audit logs, lineage, SCD Type 2 |
| [LEVEL 4] Cloud | Rebuild on AWS or Azure |
| [LEVEL 5] Big Data | Replace Pandas with PySpark |
| [LEVEL 6] Lakehouse | Bronze/Silver/Gold + Delta Lake + Databricks |

---

#  Local vs Cloud

| Local | AWS | Azure | Databricks |
|---|---|---|---|
| CSV | S3 | ADLS | Cloud Storage |
| Python | Glue | Data Factory | Workflows |
| Pandas | Spark/Glue | Spark/Databricks | Spark |
| Parquet | S3 | ADLS | Cloud Storage |
| DuckDB | Athena/Redshift | Synapse | Databricks SQL |
| Pytest | CI/CD | DevOps | CI/CD |

> **Learn the architecture first. Product names come second.**

---

#  Questions to Explore

- What happens if the source contains duplicate loans?
- What happens if exposure is negative?
- What happens at 1 billion rows?
- When does Pandas become unsuitable?
- Why use Parquet instead of CSV?
- When should DuckDB be replaced by a cloud warehouse?
- How would you make the pipeline idempotent?
- How would you recover from a failed pipeline?
- How would you prove where a KPI came from?
- How would you secure customer-level data?
- Where would S3 or ADLS fit?
- When is Spark useful?
- How would you implement Bronze/Silver/Gold?
- How could AI help without bypassing data controls?

---

#  Who Is This For?

This project is especially useful for:

-  Students
-  Data Engineering beginners
-  Data Analysts moving toward Data Engineering
-  Business Analysts moving into technical roles
-  Banking technology learners
-  Finance transformation professionals
-  Developers learning data platforms
-  Anyone building a Data Engineering portfolio

---

#  Learning Progression

A strong portfolio should make every project teach something new:

```text
Project 1
Data Engineering Fundamentals
        v
Project 2
 Bank Regulatory Reporting
        v
Project 3
 Pharmacy / Operations
        v
Project 4
 AI + Data Engineering
        v
Project 5
 Government / Budget / Policy Data
```

Recommended technical progression:

```text
ETL
 v
Data Quality
 v
Data Warehousing
 v
CI/CD
 v
Cloud
 v
Spark
 v
Lakehouse
 v
AI
 v
Governance
```

---

#  Portfolio Skills Demonstrated

```text
[OK] Python
[OK] SQL
[OK] Pandas
[OK] Parquet
[OK] DuckDB
[OK] ETL / ELT
[OK] Data Quality
[OK] Data Validation
[OK] Data Modelling
[OK] Fact / Dimension Tables
[OK] Star Schema
[OK] Regulatory Reporting Concepts
[OK] KPI Engineering
[OK] Automated Testing
[OK] Pytest
[OK] Git / GitHub
[OK] GitHub Actions / CI
[OK] Cloud Architecture Awareness
[OK] Spark Concepts
[OK] Databricks Concepts
[OK] Lakehouse Concepts
[OK] AI Extension Concepts
```

The key capability is translating:

```text
Business Problem
      v
Data
      v
Pipeline
      v
Warehouse
      v
Business Logic
      v
Quality Controls
      v
Reporting
```

---

# WARNING: Educational Disclaimer

This repository is an **educational simulation**.

The banking data, risk categories, risk weights, RWA calculations and regulatory logic are simplified for learning.

Do **not** use this project for:

- Actual regulatory submissions
- Production banking decisions
- Capital calculations
- Financial decisions
- Compliance certification
- Real-world regulatory reporting

Real implementations require detailed regulatory requirements, governance, reconciliation, validation, security and specialist regulatory expertise.

---

#  Core Scope

- [x] Data ingestion
- [x] Data validation
- [x] Transformation
- [x] Parquet processing
- [x] DuckDB warehouse
- [x] Fact/dimension modelling
- [x] Regulatory SQL
- [x] Simplified RWA calculation
- [x] Regulatory KPIs
- [x] Automated tests
- [x] CSV reporting
- [x] HTML reporting
- [x] GitHub repository
- [x] GitHub Actions CI

##  Suggested Extensions

- [ ] Incremental processing
- [ ] Idempotent loading
- [ ] Audit logging
- [ ] Data lineage
- [ ] SCD Type 2
- [ ] Airflow orchestration
- [ ] PySpark
- [ ] AWS
- [ ] Azure
- [ ] Databricks
- [ ] Delta Lake
- [ ] Power BI
- [ ] AI anomaly detection
- [ ] Natural-language SQL
- [ ] Regulatory-document RAG

---

#  Learn by Experimenting

Don't stop after the first successful run.

```text
Build
  v
Change
  v
Break
  v
Investigate
  v
Fix
  v
Test
  v
Improve
  v
Rebuild
```

The goal is not:

> I ran someone else's project.

The goal is:

> **I understand why it works, I can change it, and I can build the next version myself.**

---

<p align="center">
  <strong> Build  Break  Learn  Improve  Rebuild</strong><br><br>
  <sub>Start local. Master the fundamentals. Then scale to Cloud, Spark, Databricks and AI.</sub>
</p>
