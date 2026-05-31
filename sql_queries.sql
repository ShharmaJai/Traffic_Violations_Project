-- =========================================================
-- Traffic Violations Project - SQL Summary Queries
-- Database: traffic_violations_db
-- Purpose: SQL-based analysis using summary tables
-- =========================================================


-- Select project database
USE traffic_violations_db;


-- =========================================================
-- 1. Show all SQL summary tables
-- =========================================================

SHOW TABLES;


-- =========================================================
-- 2. Violation Type Summary
-- Question: What are the most common violation types?
-- =========================================================

SELECT 
    violation_type,
    total_violations
FROM violation_type_summary
ORDER BY total_violations DESC;


-- =========================================================
-- 3. Top 10 High-Risk Locations
-- Question: Which locations have the highest traffic incidents?
-- =========================================================

SELECT 
    location,
    total_violations
FROM top_locations_summary
ORDER BY total_violations DESC
LIMIT 10;


-- =========================================================
-- 4. Monthly Violation Trend
-- Question: How does violation frequency vary by month?
-- =========================================================

SELECT 
    month,
    total_violations
FROM monthly_violation_summary
ORDER BY month;


-- =========================================================
-- 5. Top 10 Vehicle Makes
-- Question: What vehicle makes are most often involved in violations?
-- =========================================================

SELECT 
    vehicle_make,
    total_violations
FROM vehicle_make_summary
ORDER BY total_violations DESC
LIMIT 10;


-- =========================================================
-- 6. Violations by Gender
-- Question: How are violations distributed by gender?
-- =========================================================

SELECT 
    gender,
    total_violations
FROM gender_summary
ORDER BY total_violations DESC;


-- =========================================================
-- 7. Violations by Race
-- Question: How are violations distributed by race?
-- =========================================================

SELECT 
    race,
    total_violations
FROM race_summary
ORDER BY total_violations DESC;


-- =========================================================
-- 8. Accident-Related Summary
-- Question: How often do violations involve accidents, injuries, damage, alcohol, or fatality?
-- =========================================================

SELECT 
    metric,
    total_cases
FROM accident_summary
ORDER BY total_cases DESC;


-- =========================================================
-- 9. Highest Accident-Related Metric
-- Purpose: Find the most common safety-related issue
-- =========================================================

SELECT 
    metric,
    total_cases
FROM accident_summary
ORDER BY total_cases DESC
LIMIT 1;


-- =========================================================
-- 10. Top 5 Vehicle Makes
-- Purpose: Short vehicle make summary for README/report
-- =========================================================

SELECT 
    vehicle_make,
    total_violations
FROM vehicle_make_summary
ORDER BY total_violations DESC
LIMIT 5;


-- =========================================================
-- 11. Top 5 Locations
-- Purpose: Short high-risk location summary for README/report
-- =========================================================

SELECT 
    location,
    total_violations
FROM top_locations_summary
ORDER BY total_violations DESC
LIMIT 5;


-- =========================================================
-- 12. Total Accident, Injury, Damage, Fatal, and Alcohol Cases
-- Purpose: View all safety-related totals
-- =========================================================

SELECT 
    metric,
    total_cases
FROM accident_summary;