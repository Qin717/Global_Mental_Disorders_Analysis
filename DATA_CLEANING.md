# Data Cleaning and Reshaping Guide

## Question 1: Clean & Reshape Raw Data

**Question**: How can we clean and reshape the raw database to remove unnecessary columns, standardize naming conventions, and optimize the data structure for analysis?

## Overview
This document explains the process of cleaning and reshaping the raw mental disorders database to create a more usable dataset for analysis.

## Data Transformation Process

### Source Data
- **Original Table**: `mental_disorders_raw_data`
- **Source**: Raw CSV data loaded into database
- **Size**: Large dataset with multiple ID columns and verbose naming

### Target Data
- **Cleaned Table**: `mental_disorders_raw_data_cleaned`
- **Purpose**: Streamlined structure optimized for analysis
- **Benefits**: Simplified column names, removed redundant data, cleaner age formatting

## Transformations Applied

### 1. Column Removal
Removed redundant ID columns that are not needed for analysis:
- `measure_id`
- `location_id` 
- `sex_id`
- `age_id`
- `metric_id`

### 2. Column Renaming
Renamed columns for clarity and consistency:

| Original Column | New Column | Purpose |
|----------------|------------|---------|
| `measure_name` | `measure` | Health measure type |
| `location_name` | `country` | Country/location |
| `sex_name` | `sex` | Gender classification |
| `age_name` | `age_group` | Age group (cleaned) |
| `cause_name` | `disorder` | Mental disorder type |
| `metric_name` | `metric` | Metric type |
| `val` | `value` | Primary value |
| `upper` | `value_upper_bounce` | Upper confidence bound |
| `lower` | `value_lower_bounce` | Lower confidence bound |

### 3. Data Cleaning
- **Age Groups**: Removed " years" suffix from age group names
  - Example: "25-29 years" → "25-29"
  - Makes age data more consistent and easier to work with

## SQL Implementation

The cleaning process is implemented in `sql/analysis_queries.sql` with these main steps:

1. **Create Cleaned Table**: Transform and copy data with new structure
2. **Add Indexes**: Optimize for common query patterns
3. **Verify Results**: Check record count and sample data

### Key SQL Query
```sql
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
```

## Benefits of Cleaned Data

- **Simplified Structure**: Easier to query and analyze
- **Consistent Naming**: Clear, descriptive column names
- **Optimized Performance**: Indexes on key columns
- **Clean Age Data**: Standardized age group formatting
- **Reduced Redundancy**: Removed unnecessary ID columns

## Usage

After running the cleaning queries, use the `mental_disorders_raw_data_cleaned` table for all analysis work. This table provides a clean, consistent foundation for:

- Trend analysis by country and year
- Demographic comparisons by age and sex
- Mental disorder prevalence studies
- Statistical modeling and visualization

## Next Steps

With the cleaned data in place, you can now:
1. Build analytical queries on the cleaned table
2. Create visualizations using the standardized columns
3. Perform statistical analysis with confidence in data quality
4. Export subsets for specific research questions
