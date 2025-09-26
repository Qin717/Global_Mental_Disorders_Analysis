-- Question 1: Clean & Reshape Raw Data
-- Clean and reshape mental disorders raw data
-- Remove ID columns, clean age data, and rename columns

CREATE TABLE mental_disorders_raw_data_cleaned AS
SELECT 
    measure_name as measure,
    location_name as country,
    sex_name as sex,
    REPLACE(age_name, ' years', '') as age_group,
    cause_name as disorder,
    year,
    metric_name as metric,
    val as value,
    upper as value_upper_bounce,
    lower as value_lower_bounce
FROM mental_disorders_raw_data;

-- Create indexes for better query performance
CREATE INDEX idx_country ON mental_disorders_raw_data_cleaned(country);
CREATE INDEX idx_disorder ON mental_disorders_raw_data_cleaned(disorder);
CREATE INDEX idx_year ON mental_disorders_raw_data_cleaned(year);

-- Verify the cleaned data
SELECT COUNT(*) as total_records FROM mental_disorders_raw_data_cleaned;

-- Sample the cleaned data
SELECT * FROM mental_disorders_raw_data_cleaned LIMIT 5;

-- =====================================================
-- Question 2: Mental Disorder Growth Analysis (1990-2021)
-- Which mental disorders have grown the most over the last 30+ years?
-- =====================================================

WITH baseline AS (
    SELECT disorder, AVG(value) AS val_1990
    FROM mental_disorders_raw_data_cleaned
    WHERE year = 1990
      AND metric = 'Percent'
      AND sex = 'Both'
      AND disorder IN ('Depressive disorders',
                       'Anxiety disorders',
                       'Schizophrenia',
                       'Bipolar disorder',
                       'Eating disorders')
    GROUP BY disorder
),
latest AS (
    SELECT disorder, AVG(value) AS val_2021
    FROM mental_disorders_raw_data_cleaned
    WHERE year = 2021
      AND metric = 'Percent'
      AND sex = 'Both'
      AND disorder IN ('Depressive disorders',
                       'Anxiety disorders',
                       'Schizophrenia',
                       'Bipolar disorder',
                       'Eating disorders')
    GROUP BY disorder
)
SELECT l.disorder,
       ROUND((b.val_1990 * 100)::numeric, 2) AS prevalence_1990_percent,
       ROUND((l.val_2021 * 100)::numeric, 2) AS prevalence_2021_percent,
       ROUND(((l.val_2021 - b.val_1990) * 100)::numeric, 2) AS change_percentage_points,
       ROUND(((l.val_2021 - b.val_1990) / NULLIF(b.val_1990,0) * 100)::numeric, 1) AS relative_growth_percent
FROM latest l
JOIN baseline b USING (disorder)
ORDER BY relative_growth_percent DESC;

-- =====================================================
-- Question 3: Age Group Trends Analysis (1990-2021)
-- Which age group have been showing increase trend from 1990 to 2021?
-- =====================================================

WITH baseline AS (
    SELECT age_group, AVG(value) AS val_1990
    FROM mental_disorders_raw_data_cleaned
    WHERE year = 1990
      AND sex = 'Both'
    GROUP BY age_group
),
latest AS (
    SELECT age_group, AVG(value) AS val_2021
    FROM mental_disorders_raw_data_cleaned
    WHERE year = 2021
      AND sex = 'Both'
    GROUP BY age_group
)
SELECT l.age_group,
       ROUND((b.val_1990 * 100)::numeric, 2) AS prevalence_1990_percent,
       ROUND((l.val_2021 * 100)::numeric, 2) AS prevalence_2021_percent,
       ROUND(((l.val_2021 - b.val_1990) * 100)::numeric, 2) AS change_percentage_points,
       ROUND(((l.val_2021 - b.val_1990) / NULLIF(b.val_1990,0) * 100)::numeric, 1) AS relative_growth_percent
FROM latest l
JOIN baseline b USING (age_group)
ORDER BY relative_growth_percent DESC;
