-- ============================================================
-- Regulatory KPI Analysis
-- Project 2: Bank Regulatory Reporting Pipeline
-- ============================================================


-- 1. Overall Regulatory KPIs
SELECT
    COUNT(*) AS total_loans,
    ROUND(SUM(outstanding_amount), 2) AS total_exposure,
    ROUND(SUM(rwa), 2) AS total_rwa,
    ROUND(
        SUM(rwa) / NULLIF(SUM(outstanding_amount), 0),
        4
    ) AS average_risk_weight
FROM fact_regulatory_loan;


-- 2. High-Risk Exposure Percentage
SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN risk_category = 'HIGH'
                THEN outstanding_amount
                ELSE 0
            END
        ) / NULLIF(SUM(outstanding_amount), 0),
        2
    ) AS high_risk_exposure_pct
FROM fact_regulatory_loan;


-- 3. High-Risk RWA Percentage
SELECT
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
FROM fact_regulatory_loan;


-- 4. RWA by Customer Type
SELECT
    c.customer_type,
    COUNT(*) AS loan_count,
    ROUND(SUM(f.outstanding_amount), 2) AS total_exposure,
    ROUND(SUM(f.rwa), 2) AS total_rwa,
    ROUND(
        SUM(f.rwa) / NULLIF(SUM(f.outstanding_amount), 0),
        4
    ) AS average_risk_weight
FROM fact_regulatory_loan f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY c.customer_type
ORDER BY total_rwa DESC;


-- 5. Top 5 Customers by RWA
SELECT
    c.customer_id,
    c.customer_name,
    c.customer_type,
    c.country,
    COUNT(*) AS loan_count,
    ROUND(SUM(f.outstanding_amount), 2) AS total_exposure,
    ROUND(SUM(f.rwa), 2) AS total_rwa
FROM fact_regulatory_loan f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.customer_type,
    c.country
ORDER BY total_rwa DESC
LIMIT 5;