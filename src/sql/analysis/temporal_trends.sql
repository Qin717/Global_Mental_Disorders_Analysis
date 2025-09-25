-- Temporal Trends Analysis Queries
-- Advanced SQL queries for analyzing mental health trends over time
-- Author: Data Analysis Portfolio

-- 1. Year-over-Year Growth Rate by Disorder
WITH yearly_averages AS (
    SELECT 
        d.disorder_name,
        mhd.year,
        AVG(mhd.value) as avg_prevalence
    FROM mental_health_data mhd
    JOIN mental_disorders d ON mhd.disorder_id = d.disorder_id
    GROUP BY d.disorder_name, mhd.year
),
growth_rates AS (
    SELECT 
        disorder_name,
        year,
        avg_prevalence,
        LAG(avg_prevalence) OVER (PARTITION BY disorder_name ORDER BY year) as prev_year_prevalence,
        CASE 
            WHEN LAG(avg_prevalence) OVER (PARTITION BY disorder_name ORDER BY year) > 0 
            THEN ((avg_prevalence - LAG(avg_prevalence) OVER (PARTITION BY disorder_name ORDER BY year)) 
                  / LAG(avg_prevalence) OVER (PARTITION BY disorder_name ORDER BY year)) * 100
            ELSE NULL 
        END as yoy_growth_rate
    FROM yearly_averages
)
SELECT 
    disorder_name,
    year,
    avg_prevalence,
    yoy_growth_rate,
    AVG(yoy_growth_rate) OVER (PARTITION BY disorder_name ORDER BY year ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) as five_year_avg_growth
FROM growth_rates
WHERE yoy_growth_rate IS NOT NULL
ORDER BY disorder_name, year;

-- 2. Trend Detection using Linear Regression (PostgreSQL)
WITH trend_analysis AS (
    SELECT 
        d.disorder_name,
        COUNT(*) as data_points,
        -- Calculate linear trend slope
        (COUNT(*) * SUM(mhd.year * AVG(mhd.value)) - SUM(mhd.year) * SUM(AVG(mhd.value))) /
        (COUNT(*) * SUM(mhd.year * mhd.year) - SUM(mhd.year) * SUM(mhd.year)) as trend_slope,
        
        -- Calculate correlation coefficient
        (COUNT(*) * SUM(mhd.year * AVG(mhd.value)) - SUM(mhd.year) * SUM(AVG(mhd.value))) /
        SQRT(
            (COUNT(*) * SUM(mhd.year * mhd.year) - SUM(mhd.year) * SUM(mhd.year)) *
            (COUNT(*) * SUM(AVG(mhd.value) * AVG(mhd.value)) - SUM(AVG(mhd.value)) * SUM(AVG(mhd.value)))
        ) as correlation,
        
        MIN(mhd.year) as start_year,
        MAX(mhd.year) as end_year,
        AVG(AVG(mhd.value)) as avg_prevalence
    FROM mental_health_data mhd
    JOIN mental_disorders d ON mhd.disorder_id = d.disorder_id
    GROUP BY d.disorder_name, mhd.year
    HAVING COUNT(*) >= 10  -- At least 10 years of data
)
SELECT 
    disorder_name,
    data_points,
    trend_slope,
    correlation,
    CASE 
        WHEN trend_slope > 0.001 AND correlation > 0.7 THEN 'Strong Increasing'
        WHEN trend_slope > 0.0001 AND correlation > 0.5 THEN 'Moderate Increasing'
        WHEN trend_slope < -0.001 AND correlation < -0.7 THEN 'Strong Decreasing'
        WHEN trend_slope < -0.0001 AND correlation < -0.5 THEN 'Moderate Decreasing'
        ELSE 'Stable/Unclear'
    END as trend_direction,
    start_year,
    end_year,
    avg_prevalence
FROM trend_analysis
ORDER BY ABS(correlation) DESC;

-- 3. Seasonal/Cyclical Pattern Detection (if data has monthly breakdowns)
-- Note: This query assumes we might have sub-yearly data in the future
WITH decade_analysis AS (
    SELECT 
        d.disorder_name,
        FLOOR(mhd.year / 10) * 10 as decade,
        AVG(mhd.value) as avg_prevalence,
        STDDEV(mhd.value) as std_prevalence,
        COUNT(*) as data_points
    FROM mental_health_data mhd
    JOIN mental_disorders d ON mhd.disorder_id = d.disorder_id
    GROUP BY d.disorder_name, FLOOR(mhd.year / 10) * 10
    HAVING COUNT(*) >= 5  -- At least 5 years of data per decade
)
SELECT 
    disorder_name,
    decade,
    avg_prevalence,
    std_prevalence,
    data_points,
    LAG(avg_prevalence) OVER (PARTITION BY disorder_name ORDER BY decade) as prev_decade_avg,
    CASE 
        WHEN LAG(avg_prevalence) OVER (PARTITION BY disorder_name ORDER BY decade) > 0 
        THEN ((avg_prevalence - LAG(avg_prevalence) OVER (PARTITION BY disorder_name ORDER BY decade)) 
              / LAG(avg_prevalence) OVER (PARTITION BY disorder_name ORDER BY decade)) * 100
        ELSE NULL 
    END as decade_change_pct
FROM decade_analysis
ORDER BY disorder_name, decade;

-- 4. Identify Turning Points and Trend Changes
WITH ranked_years AS (
    SELECT 
        d.disorder_name,
        mhd.year,
        AVG(mhd.value) as avg_prevalence,
        ROW_NUMBER() OVER (PARTITION BY d.disorder_name ORDER BY mhd.year) as year_rank
    FROM mental_health_data mhd
    JOIN mental_disorders d ON mhd.disorder_id = d.disorder_id
    GROUP BY d.disorder_name, mhd.year
),
trend_changes AS (
    SELECT 
        disorder_name,
        year,
        avg_prevalence,
        LAG(avg_prevalence, 1) OVER (PARTITION BY disorder_name ORDER BY year) as prev1_prevalence,
        LAG(avg_prevalence, 2) OVER (PARTITION BY disorder_name ORDER BY year) as prev2_prevalence,
        LEAD(avg_prevalence, 1) OVER (PARTITION BY disorder_name ORDER BY year) as next1_prevalence,
        LEAD(avg_prevalence, 2) OVER (PARTITION BY disorder_name ORDER BY year) as next2_prevalence
    FROM ranked_years
)
SELECT 
    disorder_name,
    year,
    avg_prevalence,
    CASE 
        WHEN (prev2_prevalence < prev1_prevalence AND prev1_prevalence < avg_prevalence 
              AND avg_prevalence > next1_prevalence AND next1_prevalence > next2_prevalence) 
        THEN 'Peak'
        WHEN (prev2_prevalence > prev1_prevalence AND prev1_prevalence > avg_prevalence 
              AND avg_prevalence < next1_prevalence AND next1_prevalence < next2_prevalence) 
        THEN 'Valley'
        WHEN (prev1_prevalence < avg_prevalence AND avg_prevalence < next1_prevalence) 
        THEN 'Increasing'
        WHEN (prev1_prevalence > avg_prevalence AND avg_prevalence > next1_prevalence) 
        THEN 'Decreasing'
        ELSE 'Stable'
    END as trend_point_type
FROM trend_changes
WHERE prev2_prevalence IS NOT NULL 
  AND next2_prevalence IS NOT NULL
ORDER BY disorder_name, year;

-- 5. Moving Averages and Smoothed Trends
SELECT 
    d.disorder_name,
    mhd.year,
    AVG(mhd.value) as current_year_avg,
    
    -- 3-year moving average
    AVG(AVG(mhd.value)) OVER (
        PARTITION BY d.disorder_name 
        ORDER BY mhd.year 
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ) as three_year_ma,
    
    -- 5-year moving average
    AVG(AVG(mhd.value)) OVER (
        PARTITION BY d.disorder_name 
        ORDER BY mhd.year 
        ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
    ) as five_year_ma,
    
    -- Exponential moving average approximation
    AVG(mhd.value) * 0.4 + 
    LAG(AVG(mhd.value), 1) OVER (PARTITION BY d.disorder_name ORDER BY mhd.year) * 0.3 +
    LAG(AVG(mhd.value), 2) OVER (PARTITION BY d.disorder_name ORDER BY mhd.year) * 0.2 +
    LAG(AVG(mhd.value), 3) OVER (PARTITION BY d.disorder_name ORDER BY mhd.year) * 0.1 
    as ema_approximation,
    
    -- Volatility (rolling standard deviation)
    STDDEV(AVG(mhd.value)) OVER (
        PARTITION BY d.disorder_name 
        ORDER BY mhd.year 
        ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
    ) as five_year_volatility
    
FROM mental_health_data mhd
JOIN mental_disorders d ON mhd.disorder_id = d.disorder_id
GROUP BY d.disorder_name, mhd.year
ORDER BY d.disorder_name, mhd.year;

-- 6. Compare Pre and Post specific years (e.g., 2000, 2010, 2020)
WITH period_comparison AS (
    SELECT 
        d.disorder_name,
        CASE 
            WHEN mhd.year < 2000 THEN '1980-1999'
            WHEN mhd.year BETWEEN 2000 AND 2009 THEN '2000-2009' 
            WHEN mhd.year BETWEEN 2010 AND 2019 THEN '2010-2019'
            WHEN mhd.year >= 2020 THEN '2020+'
        END as period,
        AVG(mhd.value) as avg_prevalence,
        STDDEV(mhd.value) as std_prevalence,
        COUNT(*) as data_points,
        MIN(mhd.value) as min_prevalence,
        MAX(mhd.value) as max_prevalence
    FROM mental_health_data mhd
    JOIN mental_disorders d ON mhd.disorder_id = d.disorder_id
    GROUP BY d.disorder_name, 
        CASE 
            WHEN mhd.year < 2000 THEN '1980-1999'
            WHEN mhd.year BETWEEN 2000 AND 2009 THEN '2000-2009' 
            WHEN mhd.year BETWEEN 2010 AND 2019 THEN '2010-2019'
            WHEN mhd.year >= 2020 THEN '2020+'
        END
)
SELECT 
    disorder_name,
    period,
    avg_prevalence,
    std_prevalence,
    data_points,
    min_prevalence,
    max_prevalence,
    LAG(avg_prevalence) OVER (PARTITION BY disorder_name ORDER BY period) as prev_period_avg,
    CASE 
        WHEN LAG(avg_prevalence) OVER (PARTITION BY disorder_name ORDER BY period) > 0 
        THEN ((avg_prevalence - LAG(avg_prevalence) OVER (PARTITION BY disorder_name ORDER BY period)) 
              / LAG(avg_prevalence) OVER (PARTITION BY disorder_name ORDER BY period)) * 100
        ELSE NULL 
    END as period_change_pct
FROM period_comparison
ORDER BY disorder_name, period;
