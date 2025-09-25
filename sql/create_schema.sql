-- Mental Health Database Schema
-- Create tables for mental disorders analysis

CREATE TABLE IF NOT EXISTS mental_health_data (
    id SERIAL PRIMARY KEY,
    country VARCHAR(100),
    disorder VARCHAR(100),
    measure VARCHAR(100),
    age_group VARCHAR(50),
    sex VARCHAR(20),
    year INTEGER,
    value DECIMAL(15,10),
    upper_bound DECIMAL(15,10),
    lower_bound DECIMAL(15,10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_country ON mental_health_data(country);
CREATE INDEX idx_disorder ON mental_health_data(disorder);
CREATE INDEX idx_year ON mental_health_data(year);
CREATE INDEX idx_country_disorder_year ON mental_health_data(country, disorder, year);
