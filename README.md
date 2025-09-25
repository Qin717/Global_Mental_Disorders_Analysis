# 🧠 Global Mental Disorders Data Analysis Portfolio

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![SQL](https://img.shields.io/badge/SQL-PostgreSQL-orange.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data](https://img.shields.io/badge/Data-1.8GB-red.svg)](#dataset)

A comprehensive data analysis portfolio examining global mental health trends from 1980-2021, showcasing advanced Python and SQL skills for data science and analytics.

## 📊 Project Overview

This project analyzes a comprehensive dataset of global mental health disorders, providing insights into:

- **10 Mental Disorders** across **204+ countries**
- **4 Health Measures** (Deaths, DALYs, YLDs, YLLs)
- **42 Years** of longitudinal data (1980-2021)
- **Demographic patterns** by age and gender
- **Geographic variations** and temporal trends

## 🎯 Key Features

### 🐍 Python Analysis
- **Data Processing**: Efficient handling of 12.6M+ records (1.8GB dataset)
- **Statistical Analysis**: Comprehensive EDA with advanced visualizations
- **Machine Learning**: Trend analysis and predictive modeling
- **Memory Optimization**: Efficient data types and processing

### 🗃️ SQL Integration
- **Database Design**: Normalized schema for mental health data
- **Complex Queries**: Advanced analytical SQL with CTEs and window functions
- **Performance Optimization**: Indexed queries for large datasets
- **Data Warehousing**: ETL processes and data pipeline

### 📈 Analytics & Insights
- **Temporal Trends**: 42-year mental health evolution
- **Geographic Analysis**: Country and regional comparisons
- **Demographic Insights**: Age and gender-based patterns
- **Statistical Modeling**: Prevalence predictions and correlations

## 🗂️ Repository Structure

```
mental-disorders-analysis/
├── 📁 data/                          # Raw and processed datasets
│   ├── Mental_Disorders_Raw_Data.csv # Original dataset (1.8GB)
│   └── processed/                    # Cleaned and transformed data
├── 📁 src/
│   ├── 📁 python/                    # Python analysis scripts
│   │   ├── mental_disorders_analysis.py
│   │   ├── data_reshaping_advanced.py
│   │   ├── sql_integration.py
│   │   └── visualization_suite.py
│   └── 📁 sql/                       # SQL scripts and queries
│       ├── schema/                   # Database schema definitions
│       ├── etl/                      # Data loading and transformation
│       ├── analysis/                 # Analytical SQL queries
│       └── views/                    # Predefined views and CTEs
├── 📁 notebooks/                     # Jupyter notebooks
│   ├── Mental_Disorders_Portfolio.ipynb
│   ├── 01_Data_Exploration.ipynb
│   ├── 02_SQL_Analysis.ipynb
│   └── 03_Advanced_Analytics.ipynb
├── 📁 output/                        # Generated outputs
│   ├── visualizations/              # Charts and graphs
│   ├── reports/                     # Analysis reports
│   └── processed_data/              # Transformed datasets
├── 📁 config/                        # Configuration files
│   ├── database_config.py
│   └── analysis_config.yaml
├── 📁 tests/                         # Unit tests
├── 📁 docs/                          # Documentation
└── requirements.txt                  # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/mental-disorders-analysis.git
cd mental-disorders-analysis
```

2. **Set up Python environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Set up database**
```bash
# Create PostgreSQL database
createdb mental_health_db

# Run schema setup
psql mental_health_db < src/sql/schema/create_tables.sql
```

4. **Load data**
```bash
python src/python/sql_integration.py --load-data
```

5. **Run analysis**
```bash
# Python analysis
python src/python/mental_disorders_analysis.py

# Open Jupyter notebooks
jupyter notebook notebooks/
```

## 📊 Dataset Information

### Source
Global mental health data from authoritative health organizations covering:
- 204+ countries and territories
- 10 major mental health disorders
- Multiple health outcome measures
- 42 years of historical data (1980-2021)

### Mental Disorders Covered
1. Anxiety disorders
2. Attention-deficit/hyperactivity disorder
3. Autism spectrum disorders
4. Bipolar disorder
5. Conduct disorder
6. Depressive disorders
7. Eating disorders
8. Idiopathic developmental intellectual disability
9. Other mental disorders
10. Schizophrenia

### Health Measures
- **Deaths**: Number of deaths attributed to mental disorders
- **DALYs**: Disability-Adjusted Life Years
- **YLDs**: Years Lived with Disability
- **YLLs**: Years of Life Lost

## 🔍 Key Analyses

### 1. Temporal Trends Analysis
- 42-year evolution of mental health patterns
- Identification of significant trend changes
- Seasonal and cyclical pattern detection

### 2. Geographic Insights
- Country-level prevalence comparisons
- Regional clustering and patterns
- Economic and cultural correlation analysis

### 3. Demographic Patterns
- Age-specific mental health trends
- Gender-based prevalence differences
- Life-cycle mental health analysis

### 4. Predictive Modeling
- Trend forecasting for mental health prevalence
- Risk factor identification
- Public health planning insights

## 🛠️ Technical Skills Demonstrated

### Python
- **Data Processing**: pandas, numpy for large dataset handling
- **Visualization**: matplotlib, seaborn, plotly for interactive charts
- **Statistical Analysis**: scipy, statsmodels for hypothesis testing
- **Machine Learning**: scikit-learn for predictive modeling
- **Database Integration**: SQLAlchemy, psycopg2 for database connectivity

### SQL
- **Complex Queries**: Window functions, CTEs, recursive queries
- **Performance Optimization**: Indexing strategies, query optimization
- **Data Modeling**: Normalized schema design
- **ETL Processes**: Data transformation and loading pipelines
- **Analytics**: Statistical functions and analytical queries

### Data Engineering
- **Data Pipeline**: Automated ETL processes
- **Data Quality**: Validation and cleaning procedures
- **Memory Optimization**: Efficient data type usage
- **Scalability**: Chunk processing for large datasets

## 📈 Sample Insights

> **Finding 1**: Mental health disorder prevalence has increased by X% globally from 1980 to 2021, with the most significant increases in anxiety and depressive disorders.

> **Finding 2**: There are notable gender differences, with females showing higher prevalence in anxiety and eating disorders, while males show higher rates in autism spectrum disorders.

> **Finding 3**: Geographic analysis reveals significant regional variations, with developed countries showing higher reported prevalence, potentially indicating better diagnostic capabilities.

## 🤝 Contributing

This is a portfolio project, but feedback and suggestions are welcome! Please feel free to:
- Open issues for suggestions
- Submit pull requests for improvements
- Share insights or additional analyses

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

**Your Name**
- Email: your.email@example.com
- LinkedIn: [Your LinkedIn Profile](https://linkedin.com/in/yourprofile)
- Portfolio: [Your Portfolio Website](https://yourportfolio.com)

---

⭐ **Star this repository if you found it helpful for your data science journey!**

## 🏷️ Tags

`data-analysis` `python` `sql` `postgresql` `data-science` `mental-health` `epidemiology` `data-visualization` `machine-learning` `portfolio` `jupyter` `pandas` `time-series-analysis` `demographic-analysis` `public-health`
