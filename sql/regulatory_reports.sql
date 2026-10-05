-- ============================================================
-- Regulatory Reporting Analysis
-- Project 2: Bank Regulatory Reporting Pipeline
-- ============================================================


-- 1. Overall regulatory exposure
SELECT
    COUNT(*) AS total_loans,
    ROUND(SUM(outstanding_amount), 2) AS total_exposure,
    ROUND(SUM(rwa), 2) AS total_rwa
FROM fact_regulatory_loan;


-- 2. RWA by risk category
SELECT
    risk_category,
    COUNT(*) AS loan_count,
    ROUND(SUM(outstanding_amount), 2) AS total_exposure,
    ROUND(SUM(rwa), 2) AS total_rwa
FROM fact_regulatory_loan
GROUP BY risk_category
ORDER BY total_rwa DESC;


-- 3. RWA by loan type
SELECT
    loan_type,
    COUNT(*) AS loan_count,
    ROUND(SUM(outstanding_amount), 2) AS total_exposure,
    ROUND(SUM(rwa), 2) AS total_rwa
FROM fact_regulatory_loan
GROUP BY loan_type
ORDER BY total_rwa DESC;


-- 4. RWA by country
-- Country is stored in dim_customer.
-- Join the fact table to the customer dimension.
SELECT
    c.country,
    COUNT(*) AS loan_count,
    ROUND(SUM(f.outstanding_amount), 2) AS total_exposure,
    ROUND(SUM(f.rwa), 2) AS total_rwa
FROM fact_regulatory_loan f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY c.country
ORDER BY total_rwa DESC;


-- 5. Highest-risk exposures
-- Customer details come from dim_customer.
SELECT
    f.loan_id,
    c.customer_name,
    c.country,
    f.loan_type,
    f.outstanding_amount,
    f.risk_weight,
    f.risk_category,
    f.rwa
FROM fact_regulatory_loan f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
WHERE f.risk_category = 'HIGH'
ORDER BY f.rwa DESC;