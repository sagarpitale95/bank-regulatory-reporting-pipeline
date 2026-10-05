-- ============================================================
-- BANK REGULATORY REPORTING
-- Analytical SQL Queries
-- ============================================================


-- ============================================================
-- 1. TOTAL EXPOSURE AND TOTAL RWA
-- ============================================================

SELECT
    SUM(outstanding_amount) AS total_exposure,
    SUM(rwa) AS total_rwa
FROM fact_regulatory_loan;


-- ============================================================
-- 2. EXPOSURE AND RWA BY CUSTOMER TYPE
-- ============================================================

SELECT
    c.customer_type,
    COUNT(DISTINCT f.loan_id) AS loan_count,
    SUM(f.outstanding_amount) AS total_exposure,
    SUM(f.rwa) AS total_rwa
FROM fact_regulatory_loan f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY c.customer_type
ORDER BY total_rwa DESC;


-- ============================================================
-- 3. EXPOSURE AND RWA BY RISK CATEGORY
-- ============================================================

SELECT
    risk_category,
    COUNT(*) AS loan_count,
    SUM(outstanding_amount) AS total_exposure,
    SUM(rwa) AS total_rwa
FROM fact_regulatory_loan
GROUP BY risk_category
ORDER BY total_rwa DESC;


-- ============================================================
-- 4. EXPOSURE AND RWA BY LOAN TYPE
-- ============================================================

SELECT
    loan_type,
    COUNT(*) AS loan_count,
    SUM(outstanding_amount) AS total_exposure,
    SUM(rwa) AS total_rwa
FROM fact_regulatory_loan
GROUP BY loan_type
ORDER BY total_rwa DESC;


-- ============================================================
-- 5. TOP 5 LOANS BY RWA
-- ============================================================

SELECT
    loan_id,
    customer_id,
    loan_type,
    outstanding_amount,
    risk_weight,
    risk_category,
    rwa
FROM fact_regulatory_loan
ORDER BY rwa DESC
LIMIT 5;


-- ============================================================
-- 6. CUSTOMER-LEVEL RISK SUMMARY
-- ============================================================

SELECT
    c.customer_id,
    c.customer_name,
    c.customer_type,
    COUNT(f.loan_id) AS loan_count,
    SUM(f.outstanding_amount) AS total_exposure,
    SUM(f.rwa) AS total_rwa
FROM dim_customer c
JOIN fact_regulatory_loan f
    ON c.customer_id = f.customer_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.customer_type
ORDER BY total_rwa DESC;


-- ============================================================
-- 7. HIGH-RISK EXPOSURES
-- ============================================================

SELECT
    loan_id,
    customer_id,
    loan_type,
    outstanding_amount,
    risk_weight,
    risk_category,
    rwa
FROM fact_regulatory_loan
WHERE risk_category = 'HIGH'
ORDER BY rwa DESC;


-- ============================================================
-- 8. COUNTRY-LEVEL EXPOSURE
-- ============================================================

SELECT
    c.country,
    COUNT(f.loan_id) AS loan_count,
    SUM(f.outstanding_amount) AS total_exposure,
    SUM(f.rwa) AS total_rwa
FROM fact_regulatory_loan f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY c.country
ORDER BY total_rwa DESC;