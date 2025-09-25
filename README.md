# 🧠 Global Mental Disorders Data Analysis Portfolio

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data](https://img.shields.io/badge/Data-1.8GB-red.svg)](#dataset)

A comprehensive data analysis portfolio examining global mental health trends from 1980-2021, showcasing advanced Python skills for data science and analytics.

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
- **Temporal Analysis**: 42-year mental health evolution tracking
- **Geographic Insights**: Country and regional pattern analysis
- **Memory Optimization**: Efficient data types and chunk processing

### 📈 Analytics & Insights
- **Temporal Trends**: Long-term mental health evolution
- **Geographic Analysis**: Country and regional comparisons
- **Demographic Insights**: Age and gender-based patterns
- **Statistical Modeling**: Prevalence analysis and correlations

## 🗂️ Repository Structure

```
mental-disorders-analysis/
├── 📁 data/                          # Raw datasets
│   └── Mental_Disorders_Raw_Data.csv # Place dataset here (1.8GB)
├── 📁 scripts/                       # Python analysis scripts
│   ├── mental_disorders_analysis.py # Main analysis engine
│   └── Mental_Disorders_Portfolio.ipynb # Interactive Jupyter analysis
├── 📁 sql/                          # SQL queries and database scripts
│   ├── create_schema.sql            # Database schema setup
│   └── analysis_queries.sql         # Key analytical queries
├── 📁 reports/                      # Generated analysis reports
├── 📝 README.md                     # Project documentation
├── 📋 requirements.txt              # Python dependencies
├── ⚖️ LICENSE                       # MIT License
└── 🚫 .gitignore                    # Git exclusions
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
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

3. **Download and place dataset**
```bash
# Create data directory and place the CSV file
mkdir data
# Place Mental_Disorders_Raw_Data.csv in the data/ folder
```

4. **Run analysis**
```bash
# Python analysis
python scripts/mental_disorders_analysis.py

# Open Jupyter notebooks
jupyter notebook scripts/

# Run SQL queries (if using PostgreSQL)
psql your_database < sql/create_schema.sql
psql your_database < sql/analysis_queries.sql
```

## 📊 Dataset Information

### Source
Global mental health data covering:

**Note**: The dataset (1.8GB) is not included in this repository due to size limitations. Download instructions are provided in the setup guide.
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
- Growth rate calculations and pattern detection

### 2. Geographic Insights
- Country-level prevalence comparisons
- Regional clustering and patterns
- Geographic hotspot identification

### 3. Demographic Patterns
- Age-specific mental health trends
- Gender-based prevalence differences
- Life-cycle mental health analysis

### 4. Statistical Analysis
- Comprehensive exploratory data analysis
- Correlation analysis between disorders
- Data quality assessment and validation

## 🛠️ Technical Skills Demonstrated

### Python
- **Data Processing**: pandas, numpy for large dataset handling
- **Visualization**: matplotlib, seaborn for professional charts
- **Statistical Analysis**: scipy for hypothesis testing
- **Memory Optimization**: Efficient data type usage and chunk processing

### Data Science
- **Exploratory Data Analysis**: Statistical summaries, pattern identification
- **Data Cleaning**: Quality assessment and preprocessing
- **Visualization**: Clear, informative charts and insights
- **Large Dataset Processing**: Handling 1.8GB+ datasets efficiently

## 📈 Sample Insights

> **Finding 1**: Mental health disorder prevalence shows significant regional variations, with developed countries reporting higher rates, potentially indicating better diagnostic capabilities.

> **Finding 2**: Gender differences are notable across disorders, with females showing higher prevalence in anxiety and eating disorders, while males show higher rates in autism spectrum disorders.

> **Finding 3**: Temporal analysis reveals increasing trends in anxiety and depressive disorders over the 42-year period, with accelerated growth in recent decades.

## 🤝 Contributing

This is a portfolio project showcasing data science skills. Feedback and suggestions are welcome!

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

`data-analysis` `python` `data-science` `mental-health` `epidemiology` `data-visualization` `portfolio` `jupyter` `pandas` `time-series-analysis` `demographic-analysis` `public-health`