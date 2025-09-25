-- Mental Health Analysis Queries
-- Key analytical queries for mental disorders data

-- 1. Top 10 countries by average disorder prevalence
SELECT 
    country,
    AVG(value) as avg_prevalence,
    COUNT(*) as data_points
FROM mental_health_data 
GROUP BY country 
ORDER BY avg_prevalence DESC 
LIMIT 10;

-- 2. Disorder trends over time
SELECT 
    disorder,
    year,
    AVG(value) as avg_prevalence
FROM mental_health_data 
GROUP BY disorder, year 
ORDER BY disorder, year;

-- 3. Gender differences in mental health
SELECT 
    disorder,
    sex,
    AVG(value) as avg_prevalence
FROM mental_health_data 
WHERE sex IN ('Male', 'Female')
GROUP BY disorder, sex 
ORDER BY disorder, avg_prevalence DESC;

-- 4. Age group analysis
SELECT 
    age_group,
    disorder,
    AVG(value) as avg_prevalence
FROM mental_health_data 
GROUP BY age_group, disorder 
ORDER BY age_group, avg_prevalence DESC;
