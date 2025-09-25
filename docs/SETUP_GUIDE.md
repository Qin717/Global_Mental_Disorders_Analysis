# Setup Guide - Mental Disorders Analysis Portfolio

## 🚀 Quick Start Guide

This guide will help you set up the mental disorders analysis environment on your local machine.

## Prerequisites

- **Python 3.8+**
- **PostgreSQL 12+** 
- **Git**
- **8GB+ RAM** (recommended for full dataset)

## Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/mental-disorders-analysis.git
cd mental-disorders-analysis
```

### 2. Python Environment Setup

#### Using venv (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Using conda
```bash
# Create conda environment
conda create -n mental_health python=3.9
conda activate mental_health

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

#### Install PostgreSQL
- **macOS**: `brew install postgresql`
- **Ubuntu**: `sudo apt-get install postgresql postgresql-contrib`
- **Windows**: Download from [postgresql.org](https://www.postgresql.org/download/)

#### Create Database
```bash
# Start PostgreSQL service
# macOS: brew services start postgresql
# Ubuntu: sudo service postgresql start

# Create database
createdb mental_health_db

# Create user (optional)
psql -c "CREATE USER analyst WITH PASSWORD 'analyst_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE mental_health_db TO analyst;"
```

#### Set up Schema
```bash
# Run schema creation
psql mental_health_db < src/sql/schema/create_tables.sql

# Or using Python script
python src/python/sql_integration.py setup-database
```

### 4. Environment Configuration

Create `.env` file in project root:
```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mental_health_db
DB_USER=postgres
DB_PASSWORD=your_password

# Analysis Configuration
CHUNK_SIZE=10000
SAMPLE_SIZE=500000
```

### 5. Data Loading

#### Download Dataset
- Place `Mental_Disorders_Raw_Data.csv` in the `data/` directory
- Ensure the file is approximately 1.8GB

#### Load Data to Database
```bash
# Load data using Python script
python src/python/sql_integration.py load-data --csv-path data/Mental_Disorders_Raw_Data.csv

# Monitor progress
python src/python/sql_integration.py quality-report
```

### 6. Verify Installation

#### Test Python Analysis
```bash
# Run basic analysis
python src/python/mental_disorders_analysis.py

# Test database connection
python -c "from src.python.sql_integration import MentalHealthDatabase; db = MentalHealthDatabase(); print('✅ Success' if db.connect() else '❌ Failed')"
```

#### Test Jupyter Notebooks
```bash
# Start Jupyter
jupyter notebook

# Open notebooks/Mental_Disorders_Portfolio.ipynb
```

#### Test SQL Queries
```bash
# Run sample queries
psql mental_health_db < src/sql/analysis/temporal_trends.sql
```

## 🔧 Troubleshooting

### Common Issues

#### Database Connection Error
```bash
# Check PostgreSQL status
pg_ctl status

# Restart if needed
brew services restart postgresql  # macOS
sudo service postgresql restart   # Ubuntu
```

#### Memory Issues with Large Dataset
```python
# Reduce sample size in config
SAMPLE_SIZE=100000  # Instead of 500000
CHUNK_SIZE=5000     # Instead of 10000
```

#### Python Package Conflicts
```bash
# Clear and reinstall
pip freeze > packages.txt
pip uninstall -r packages.txt -y
pip install -r requirements.txt
```

#### Jupyter Notebook Issues
```bash
# Register kernel
python -m ipykernel install --user --name=mental_health

# Start with specific kernel
jupyter notebook --kernel=mental_health
```

### Performance Optimization

#### Database Indexing
```sql
-- Create additional indexes if needed
CREATE INDEX idx_custom_analysis ON mental_health_data(year, disorder_id, country_id);
```

#### Memory Management
```python
# Use chunked processing for large operations
chunk_size = 10000  # Adjust based on available RAM
```

## 📊 Verification Steps

### 1. Data Quality Check
```bash
python src/python/sql_integration.py quality-report
```

Expected output:
- Total records: 500,000+ (sample) or 12,600,000+ (full)
- Countries covered: 204+
- Disorders covered: 10
- Time range: 1980-2021

### 2. SQL Analysis Test
```sql
-- Test query
SELECT 
    disorder_name, 
    COUNT(*) as records,
    AVG(value) as avg_prevalence
FROM mental_health_data mhd
JOIN mental_disorders d ON mhd.disorder_id = d.disorder_id
GROUP BY disorder_name
ORDER BY avg_prevalence DESC;
```

### 3. Python Analysis Test
```python
import pandas as pd
from src.python.mental_disorders_analysis import MentalDisordersAnalyzer

# Test analysis
analyzer = MentalDisordersAnalyzer('data/Mental_Disorders_Raw_Data.csv')
analyzer.load_data(sample_size=10000)
analyzer.explore_data()
```

## 🎯 Next Steps

1. **Explore Notebooks**: Start with `notebooks/Mental_Disorders_Portfolio.ipynb`
2. **Run SQL Analysis**: Execute queries in `src/sql/analysis/`
3. **Generate Reports**: Use Python scripts to create visualizations
4. **Customize Analysis**: Modify parameters in `config/`

## 📧 Support

If you encounter issues:
1. Check this troubleshooting guide
2. Review error logs
3. Open an issue on GitHub
4. Contact: your.email@example.com

---

**Happy Analyzing! 🧠📊**
