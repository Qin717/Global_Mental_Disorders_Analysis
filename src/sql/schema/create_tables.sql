-- Mental Health Database Schema
-- Global Mental Disorders Analysis Database Design
-- Author: Data Analysis Portfolio
-- Date: September 2024

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS mental_health_data CASCADE;
DROP TABLE IF EXISTS countries CASCADE;
DROP TABLE IF EXISTS mental_disorders CASCADE;
DROP TABLE IF EXISTS health_measures CASCADE;
DROP TABLE IF EXISTS age_groups CASCADE;
DROP TABLE IF EXISTS sex_categories CASCADE;

-- Create dimension tables

-- Countries dimension
CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(100) UNIQUE NOT NULL,
    region VARCHAR(50),
    sub_region VARCHAR(50),
    country_code VARCHAR(3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mental disorders dimension
CREATE TABLE mental_disorders (
    disorder_id SERIAL PRIMARY KEY,
    disorder_name VARCHAR(100) UNIQUE NOT NULL,
    disorder_category VARCHAR(50),
    icd_code VARCHAR(20),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Health measures dimension
CREATE TABLE health_measures (
    measure_id SERIAL PRIMARY KEY,
    measure_name VARCHAR(100) UNIQUE NOT NULL,
    measure_description TEXT,
    unit_of_measurement VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Age groups dimension
CREATE TABLE age_groups (
    age_group_id SERIAL PRIMARY KEY,
    age_group_name VARCHAR(50) UNIQUE NOT NULL,
    age_start INTEGER,
    age_end INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sex categories dimension
CREATE TABLE sex_categories (
    sex_id SERIAL PRIMARY KEY,
    sex_name VARCHAR(20) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Main fact table
CREATE TABLE mental_health_data (
    id BIGSERIAL PRIMARY KEY,
    country_id INTEGER REFERENCES countries(country_id),
    disorder_id INTEGER REFERENCES mental_disorders(disorder_id),
    measure_id INTEGER REFERENCES health_measures(measure_id),
    age_group_id INTEGER REFERENCES age_groups(age_group_id),
    sex_id INTEGER REFERENCES sex_categories(sex_id),
    year INTEGER NOT NULL,
    value DECIMAL(15,10) NOT NULL,
    upper_bound DECIMAL(15,10),
    lower_bound DECIMAL(15,10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_mental_health_country ON mental_health_data(country_id);
CREATE INDEX idx_mental_health_disorder ON mental_health_data(disorder_id);
CREATE INDEX idx_mental_health_measure ON mental_health_data(measure_id);
CREATE INDEX idx_mental_health_year ON mental_health_data(year);
CREATE INDEX idx_mental_health_composite ON mental_health_data(country_id, disorder_id, year);

-- Create composite index for common queries
CREATE INDEX idx_mental_health_analysis ON mental_health_data(disorder_id, country_id, year, sex_id, age_group_id);

-- Add constraints
ALTER TABLE mental_health_data ADD CONSTRAINT chk_year_range 
    CHECK (year >= 1980 AND year <= 2030);

ALTER TABLE mental_health_data ADD CONSTRAINT chk_value_positive 
    CHECK (value >= 0);

ALTER TABLE mental_health_data ADD CONSTRAINT chk_bounds_valid 
    CHECK (upper_bound >= lower_bound);

-- Create update trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_mental_health_data_updated_at 
    BEFORE UPDATE ON mental_health_data 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert reference data
INSERT INTO sex_categories (sex_name) VALUES 
    ('Male'),
    ('Female'),
    ('Both');

INSERT INTO health_measures (measure_name, measure_description, unit_of_measurement) VALUES 
    ('Deaths', 'Number of deaths attributed to mental disorders', 'Percentage'),
    ('DALYs (Disability-Adjusted Life Years)', 'Disability-Adjusted Life Years lost due to mental disorders', 'Percentage'),
    ('YLDs (Years Lived with Disability)', 'Years lived with disability due to mental disorders', 'Percentage'),
    ('YLLs (Years of Life Lost)', 'Years of life lost due to mental disorders', 'Percentage');

INSERT INTO mental_disorders (disorder_name, disorder_category) VALUES 
    ('Anxiety disorders', 'Anxiety and Stress-Related'),
    ('Attention-deficit/hyperactivity disorder', 'Neurodevelopmental'),
    ('Autism spectrum disorders', 'Neurodevelopmental'),
    ('Bipolar disorder', 'Mood Disorders'),
    ('Conduct disorder', 'Behavioral Disorders'),
    ('Depressive disorders', 'Mood Disorders'),
    ('Eating disorders', 'Eating and Body Image'),
    ('Idiopathic developmental intellectual disability', 'Neurodevelopmental'),
    ('Other mental disorders', 'Other'),
    ('Schizophrenia', 'Psychotic Disorders');

-- Sample age groups (will be populated from data)
INSERT INTO age_groups (age_group_name, age_start, age_end) VALUES 
    ('5-14 years', 5, 14),
    ('15-19 years', 15, 19),
    ('20-24 years', 20, 24),
    ('25-29 years', 25, 29),
    ('30-34 years', 30, 34),
    ('35-39 years', 35, 39),
    ('40-44 years', 40, 44),
    ('45-49 years', 45, 49),
    ('50-54 years', 50, 54),
    ('55-59 years', 55, 59),
    ('60-64 years', 60, 64),
    ('65-69 years', 65, 69),
    ('70-74 years', 70, 74),
    ('75-79 years', 75, 79),
    ('80-84 years', 80, 84),
    ('85-89 years', 85, 89);

-- Create materialized views for common queries
CREATE MATERIALIZED VIEW mv_yearly_disorder_summary AS
SELECT 
    d.disorder_name,
    mhd.year,
    COUNT(*) as record_count,
    AVG(mhd.value) as avg_prevalence,
    STDDEV(mhd.value) as std_prevalence,
    MIN(mhd.value) as min_prevalence,
    MAX(mhd.value) as max_prevalence
FROM mental_health_data mhd
JOIN mental_disorders d ON mhd.disorder_id = d.disorder_id
GROUP BY d.disorder_name, mhd.year
ORDER BY mhd.year, d.disorder_name;

CREATE MATERIALIZED VIEW mv_country_disorder_summary AS
SELECT 
    c.country_name,
    d.disorder_name,
    COUNT(*) as record_count,
    AVG(mhd.value) as avg_prevalence,
    MIN(mhd.year) as first_year,
    MAX(mhd.year) as last_year
FROM mental_health_data mhd
JOIN countries c ON mhd.country_id = c.country_id
JOIN mental_disorders d ON mhd.disorder_id = d.disorder_id
GROUP BY c.country_name, d.disorder_name
ORDER BY c.country_name, d.disorder_name;

-- Create indexes on materialized views
CREATE INDEX idx_mv_yearly_disorder ON mv_yearly_disorder_summary(disorder_name, year);
CREATE INDEX idx_mv_country_disorder ON mv_country_disorder_summary(country_name, disorder_name);

-- Refresh materialized views function
CREATE OR REPLACE FUNCTION refresh_all_materialized_views()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW mv_yearly_disorder_summary;
    REFRESH MATERIALIZED VIEW mv_country_disorder_summary;
    RAISE NOTICE 'All materialized views refreshed successfully';
END;
$$ LANGUAGE plpgsql;

COMMENT ON TABLE mental_health_data IS 'Main fact table containing mental health prevalence data';
COMMENT ON TABLE countries IS 'Dimension table for countries and regions';
COMMENT ON TABLE mental_disorders IS 'Dimension table for mental health disorders';
COMMENT ON TABLE health_measures IS 'Dimension table for health outcome measures';
COMMENT ON MATERIALIZED VIEW mv_yearly_disorder_summary IS 'Aggregated yearly statistics by disorder';
COMMENT ON MATERIALIZED VIEW mv_country_disorder_summary IS 'Aggregated statistics by country and disorder';

-- Grant permissions (adjust as needed)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO analyst_role;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO analyst_role;
