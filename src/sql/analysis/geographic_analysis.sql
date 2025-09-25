-- Geographic Analysis Queries
-- Advanced SQL queries for analyzing mental health patterns by geography
-- Author: Data Analysis Portfolio

-- 1. Country Rankings by Disorder Prevalence
WITH country_disorder_stats AS (
    SELECT 
        c.country_name,
        c.region,
        d.disorder_name,
        AVG(mhd.value) as avg_prevalence,
        STDDEV(mhd.value) as std_prevalence,
        COUNT(*) as data_points,
        MIN(mhd.year) as first_year,
        MAX(mhd.year) as last_year
    FROM mental_health_data mhd
    JOIN countries c ON mhd.country_id = c.country_id
    JOIN mental_disorders d ON mhd.disorder_id = d.disorder_id
    GROUP BY c.country_name, c.region, d.disorder_name
    HAVING COUNT(*) >= 5  -- At least 5 data points
),
ranked_countries AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY disorder_name ORDER BY avg_prevalence DESC) as prevalence_rank,
        NTILE(4) OVER (PARTITION BY disorder_name ORDER BY avg_prevalence) as quartile
    FROM country_disorder_stats
)
SELECT 
    disorder_name,
    country_name,
    region,
    avg_prevalence,
    std_prevalence,
    prevalence_rank,
    quartile,
    CASE 
        WHEN quartile = 4 THEN 'High Prevalence'
        WHEN quartile = 3 THEN 'Medium-High'
        WHEN quartile = 2 THEN 'Medium-Low'
        ELSE 'Low Prevalence'
    END as prevalence_category,
    data_points,
    last_year - first_year + 1 as years_covered
FROM ranked_countries
ORDER BY disorder_name, prevalence_rank;

-- 2. Regional Comparison Analysis
WITH regional_stats AS (
    SELECT 
        c.region,
        d.disorder_name,
        AVG(mhd.value) as avg_prevalence,
        STDDEV(mhd.value) as std_prevalence,
        COUNT(*) as total_data_points,
        COUNT(DISTINCT c.country_id) as countries_in_region,
        MIN(mhd.value) as min_prevalence,
        MAX(mhd.value) as max_prevalence,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY mhd.value) as q1_prevalence,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY mhd.value) as median_prevalence,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY mhd.value) as q3_prevalence
    FROM mental_health_data mhd
    JOIN countries c ON mhd.country_id = c.country_id
    JOIN mental_disorders d ON mhd.disorder_id = d.disorder_id
    GROUP BY c.region, d.disorder_name
    HAVING COUNT(DISTINCT c.country_id) >= 3  -- At least 3 countries per region
),
regional_rankings AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY disorder_name ORDER BY avg_prevalence DESC) as region_rank,
        AVG(avg_prevalence) OVER (PARTITION BY disorder_name) as global_avg
    FROM regional_stats
)
SELECT 
    disorder_name,
    region,
    avg_prevalence,
    region_rank,
    avg_prevalence - global_avg as deviation_from_global,
    ((avg_prevalence - global_avg) / global_avg) * 100 as pct_deviation_from_global,
    std_prevalence,
    countries_in_region,
    median_prevalence,
    q3_prevalence - q1_prevalence as iqr,
    total_data_points
FROM regional_rankings
ORDER BY disorder_name, region_rank;

-- 3. Geographic Clustering Analysis (Countries with Similar Patterns)
WITH country_profiles AS (
    SELECT 
        c.country_name,
        c.region,
        d.disorder_name,
        AVG(mhd.value) as avg_prevalence
    FROM mental_health_data mhd
    JOIN countries c ON mhd.country_id = c.country_id
    JOIN mental_disorders d ON mhd.disorder_id = d.disorder_id
    GROUP BY c.country_name, c.region, d.disorder_name
),
country_disorder_matrix AS (
    SELECT 
        country_name,
        region,
        MAX(CASE WHEN disorder_name = 'Anxiety disorders' THEN avg_prevalence END) as anxiety_prev,
        MAX(CASE WHEN disorder_name = 'Depressive disorders' THEN avg_prevalence END) as depression_prev,
        MAX(CASE WHEN disorder_name = 'Bipolar disorder' THEN avg_prevalence END) as bipolar_prev,
        MAX(CASE WHEN disorder_name = 'Schizophrenia' THEN avg_prevalence END) as schizophrenia_prev,
        MAX(CASE WHEN disorder_name = 'Eating disorders' THEN avg_prevalence END) as eating_prev
    FROM country_profiles
    GROUP BY country_name, region
    HAVING COUNT(DISTINCT disorder_name) >= 5  -- Countries with data for at least 5 disorders
)
SELECT 
    c1.country_name as country1,
    c1.region as region1,
    c2.country_name as country2,
    c2.region as region2,
    -- Calculate Euclidean distance between countries based on disorder prevalence
    SQRT(
        POWER(COALESCE(c1.anxiety_prev, 0) - COALESCE(c2.anxiety_prev, 0), 2) +
        POWER(COALESCE(c1.depression_prev, 0) - COALESCE(c2.depression_prev, 0), 2) +
        POWER(COALESCE(c1.bipolar_prev, 0) - COALESCE(c2.bipolar_prev, 0), 2) +
        POWER(COALESCE(c1.schizophrenia_prev, 0) - COALESCE(c2.schizophrenia_prev, 0), 2) +
        POWER(COALESCE(c1.eating_prev, 0) - COALESCE(c2.eating_prev, 0), 2)
    ) as similarity_distance,
    CASE 
        WHEN c1.region = c2.region THEN 'Same Region'
        ELSE 'Different Region'
    END as region_comparison
FROM country_disorder_matrix c1
JOIN country_disorder_matrix c2 ON c1.country_name < c2.country_name
WHERE SQRT(
    POWER(COALESCE(c1.anxiety_prev, 0) - COALESCE(c2.anxiety_prev, 0), 2) +
    POWER(COALESCE(c1.depression_prev, 0) - COALESCE(c2.depression_prev, 0), 2) +
    POWER(COALESCE(c1.bipolar_prev, 0) - COALESCE(c2.bipolar_prev, 0), 2) +
    POWER(COALESCE(c1.schizophrenia_prev, 0) - COALESCE(c2.schizophrenia_prev, 0), 2) +
    POWER(COALESCE(c1.eating_prev, 0) - COALESCE(c2.eating_prev, 0), 2)
) < 0.001  -- Only show very similar countries
ORDER BY similarity_distance;

-- 4. Geographic Hotspot Analysis
WITH country_severity_scores AS (
    SELECT 
        c.country_name,
        c.region,
        d.disorder_name,
        AVG(mhd.value) as avg_prevalence,
        -- Calculate z-score for each country-disorder combination
        (AVG(mhd.value) - AVG(AVG(mhd.value)) OVER (PARTITION BY d.disorder_name)) / 
        STDDEV(AVG(mhd.value)) OVER (PARTITION BY d.disorder_name) as z_score
    FROM mental_health_data mhd
    JOIN countries c ON mhd.country_id = c.country_id
    JOIN mental_disorders d ON mhd.disorder_id = d.disorder_id
    GROUP BY c.country_name, c.region, d.disorder_name
),
hotspot_analysis AS (
    SELECT 
        country_name,
        region,
        COUNT(CASE WHEN z_score > 2 THEN 1 END) as high_severity_disorders,
        COUNT(CASE WHEN z_score > 1 THEN 1 END) as elevated_disorders,
        COUNT(CASE WHEN z_score < -1 THEN 1 END) as low_disorders,
        AVG(z_score) as avg_severity_score,
        COUNT(*) as total_disorders_measured
    FROM country_severity_scores
    GROUP BY country_name, region
)
SELECT 
    country_name,
    region,
    high_severity_disorders,
    elevated_disorders,
    low_disorders,
    avg_severity_score,
    total_disorders_measured,
    ROUND((high_severity_disorders::DECIMAL / total_disorders_measured) * 100, 1) as pct_high_severity,
    CASE 
        WHEN high_severity_disorders >= 3 THEN 'Critical Hotspot'
        WHEN high_severity_disorders >= 2 OR elevated_disorders >= 5 THEN 'High Risk'
        WHEN elevated_disorders >= 3 THEN 'Moderate Risk'
        WHEN low_disorders >= 5 THEN 'Low Prevalence'
        ELSE 'Average'
    END as risk_category
FROM hotspot_analysis
WHERE total_disorders_measured >= 5
ORDER BY high_severity_disorders DESC, avg_severity_score DESC;

-- 5. Cross-Border Analysis (Geographic Neighbors with Similar Patterns)
-- Note: This is a simplified analysis - in practice, you'd have a separate table with country borders
WITH border_analysis AS (
    SELECT 
        c1.country_name as country1,
        c1.region as region1,
        c2.country_name as country2,
        c2.region as region2,
        d.disorder_name,
        AVG(mhd1.value) as country1_prevalence,
        AVG(mhd2.value) as country2_prevalence,
        ABS(AVG(mhd1.value) - AVG(mhd2.value)) as prevalence_difference,
        (AVG(mhd1.value) + AVG(mhd2.value)) / 2 as avg_prevalence
    FROM mental_health_data mhd1
    JOIN countries c1 ON mhd1.country_id = c1.country_id
    JOIN mental_health_data mhd2 ON mhd1.disorder_id = mhd2.disorder_id 
        AND mhd1.year = mhd2.year
        AND mhd1.age_group_id = mhd2.age_group_id
        AND mhd1.sex_id = mhd2.sex_id
    JOIN countries c2 ON mhd2.country_id = c2.country_id
    JOIN mental_disorders d ON mhd1.disorder_id = d.disorder_id
    WHERE c1.country_name < c2.country_name  -- Avoid duplicates
        AND c1.region = c2.region  -- Same region analysis
    GROUP BY c1.country_name, c1.region, c2.country_name, c2.region, d.disorder_name
    HAVING COUNT(*) >= 10  -- Sufficient data points
)
SELECT 
    disorder_name,
    country1,
    country2,
    region1 as common_region,
    country1_prevalence,
    country2_prevalence,
    prevalence_difference,
    prevalence_difference / avg_prevalence * 100 as pct_difference,
    CASE 
        WHEN prevalence_difference / avg_prevalence < 0.1 THEN 'Very Similar'
        WHEN prevalence_difference / avg_prevalence < 0.25 THEN 'Similar'
        WHEN prevalence_difference / avg_prevalence < 0.5 THEN 'Moderate Difference'
        ELSE 'Large Difference'
    END as similarity_level
FROM border_analysis
ORDER BY disorder_name, prevalence_difference;

-- 6. Economic Development vs Mental Health Analysis (Simplified)
-- Note: In practice, you'd join with economic indicators table
WITH country_development_proxy AS (
    SELECT 
        c.country_name,
        c.region,
        -- Use data completeness as a proxy for development level
        COUNT(DISTINCT d.disorder_id) as disorders_measured,
        COUNT(DISTINCT mhd.year) as years_covered,
        COUNT(*) as total_data_points,
        AVG(mhd.value) as overall_avg_prevalence
    FROM mental_health_data mhd
    JOIN countries c ON mhd.country_id = c.country_id
    JOIN mental_disorders d ON mhd.disorder_id = d.disorder_id
    GROUP BY c.country_name, c.region
),
development_categories AS (
    SELECT 
        *,
        CASE 
            WHEN disorders_measured >= 8 AND years_covered >= 30 THEN 'High Development'
            WHEN disorders_measured >= 6 AND years_covered >= 20 THEN 'Medium Development'
            WHEN disorders_measured >= 4 AND years_covered >= 10 THEN 'Low-Medium Development'
            ELSE 'Limited Data'
        END as development_proxy
    FROM country_development_proxy
)
SELECT 
    development_proxy,
    COUNT(*) as country_count,
    AVG(overall_avg_prevalence) as avg_reported_prevalence,
    STDDEV(overall_avg_prevalence) as std_reported_prevalence,
    MIN(overall_avg_prevalence) as min_prevalence,
    MAX(overall_avg_prevalence) as max_prevalence,
    AVG(disorders_measured) as avg_disorders_measured,
    AVG(years_covered) as avg_years_covered
FROM development_categories
GROUP BY development_proxy
ORDER BY 
    CASE development_proxy
        WHEN 'High Development' THEN 1
        WHEN 'Medium Development' THEN 2
        WHEN 'Low-Medium Development' THEN 3
        ELSE 4
    END;
