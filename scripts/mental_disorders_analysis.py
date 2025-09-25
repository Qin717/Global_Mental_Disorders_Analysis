#!/usr/bin/env python3
"""
Mental Disorders Global Analysis - Data Portfolio
==================================================

A comprehensive analysis of global mental health data covering:
- 10 mental disorders across 204+ countries
- 4 health measures (Deaths, DALYs, YLDs, YLLs) 
- 42 years of data (1980-2021)
- Demographic breakdowns by age and sex

Author: Data Analysis Portfolio
Date: September 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up visualization style
plt.style.use('default')
sns.set_palette("husl")

class MentalDisordersAnalyzer:
    """
    A comprehensive analyzer for global mental disorders data
    """
    
    def __init__(self, data_path):
        self.data_path = Path(data_path)
        self.df = None
        self.df_clean = None
        
    def load_data(self, sample_size=None):
        """Load the mental disorders dataset"""
        print("🔄 Loading mental disorders dataset...")
        
        if sample_size:
            self.df = pd.read_csv(self.data_path, nrows=sample_size)
            print(f"📊 Loaded sample dataset: {self.df.shape[0]:,} rows")
        else:
            # For full dataset, use chunks to manage memory
            chunks = []
            chunk_size = 100000
            
            for i, chunk in enumerate(pd.read_csv(self.data_path, chunksize=chunk_size)):
                chunks.append(chunk)
                if (i + 1) % 10 == 0:
                    print(f"   Processed {(i + 1) * chunk_size:,} rows...")
                    
            self.df = pd.concat(chunks, ignore_index=True)
            print(f"📊 Loaded full dataset: {self.df.shape[0]:,} rows")
            
        print(f"📋 Columns: {list(self.df.columns)}")
        return self.df
    
    def explore_data(self):
        """Perform initial data exploration"""
        print("\n" + "="*60)
        print("🔍 DATA EXPLORATION")
        print("="*60)
        
        print(f"\n📐 Dataset Shape: {self.df.shape}")
        
        print(f"\n🌍 Geographic Coverage:")
        print(f"   • Total countries/locations: {self.df['location_name'].nunique()}")
        print(f"   • Sample locations: {', '.join(sorted(self.df['location_name'].unique())[:8])}...")
        
        print(f"\n🧠 Mental Disorders ({self.df['cause_name'].nunique()}):")
        for disorder in sorted(self.df['cause_name'].unique()):
            print(f"   • {disorder}")
            
        print(f"\n📊 Health Measures ({self.df['measure_name'].nunique()}):")
        for measure in sorted(self.df['measure_name'].unique()):
            print(f"   • {measure}")
            
        print(f"\n👥 Demographics:")
        print(f"   • Sex categories: {', '.join(self.df['sex_name'].unique())}")
        print(f"   • Age groups ({self.df['age_name'].nunique()}): {', '.join(sorted(self.df['age_name'].unique()))}")
        
        print(f"\n📅 Time Coverage:")
        print(f"   • Years: {self.df['year'].min()} - {self.df['year'].max()}")
        print(f"   • Total years: {self.df['year'].nunique()}")
        
        return self.df.describe()
    
    def clean_data(self):
        """Clean and preprocess the dataset"""
        print("\n" + "="*60)
        print("🧹 DATA CLEANING")
        print("="*60)
        
        self.df_clean = self.df.copy()
        
        print(f"\n🔍 Checking data quality...")
        
        # Check for missing values
        missing_values = self.df_clean.isnull().sum()
        print(f"\n❌ Missing values:")
        if missing_values.sum() == 0:
            print("   ✅ No missing values found!")
        else:
            print(missing_values[missing_values > 0])
        
        # Check for duplicates
        duplicates = self.df_clean.duplicated().sum()
        print(f"\n🔄 Duplicate rows: {duplicates}")
        if duplicates > 0:
            self.df_clean = self.df_clean.drop_duplicates()
            print(f"   ✅ Removed {duplicates} duplicates")
        
        # Data type optimization
        print(f"\n🔧 Optimizing data types...")
        
        # Convert categorical columns to category type for memory efficiency
        categorical_cols = ['measure_name', 'location_name', 'sex_name', 'age_name', 'cause_name', 'metric_name']
        for col in categorical_cols:
            self.df_clean[col] = self.df_clean[col].astype('category')
        
        # Ensure numeric columns are proper types
        numeric_cols = ['val', 'upper', 'lower']
        for col in numeric_cols:
            self.df_clean[col] = pd.to_numeric(self.df_clean[col], errors='coerce')
        
        # Convert year to proper integer
        self.df_clean['year'] = self.df_clean['year'].astype(int)
        
        print(f"   ✅ Optimized data types")
        
        # Remove extreme outliers (values beyond 99.9th percentile)
        for col in numeric_cols:
            q99_9 = self.df_clean[col].quantile(0.999)
            outliers = (self.df_clean[col] > q99_9).sum()
            if outliers > 0:
                print(f"   ⚠️  Found {outliers} extreme outliers in {col} (>{q99_9:.2e})")
        
        # Add derived columns for analysis
        self.df_clean['confidence_interval_width'] = self.df_clean['upper'] - self.df_clean['lower']
        self.df_clean['relative_uncertainty'] = self.df_clean['confidence_interval_width'] / self.df_clean['val']
        
        print(f"\n✅ Data cleaning complete!")
        print(f"   📊 Clean dataset shape: {self.df_clean.shape}")
        
        return self.df_clean
    
    def create_summary_statistics(self):
        """Create comprehensive summary statistics"""
        print("\n" + "="*60)
        print("📈 SUMMARY STATISTICS")
        print("="*60)
        
        # Overall statistics by mental disorder
        disorder_stats = (self.df_clean.groupby('cause_name')['val']
                         .agg(['count', 'mean', 'median', 'std', 'min', 'max'])
                         .round(6))
        
        print(f"\n🧠 Statistics by Mental Disorder:")
        print(disorder_stats)
        
        # Statistics by health measure
        measure_stats = (self.df_clean.groupby('measure_name')['val']
                        .agg(['count', 'mean', 'median', 'std', 'min', 'max'])
                        .round(6))
        
        print(f"\n📊 Statistics by Health Measure:")
        print(measure_stats)
        
        # Temporal trends
        yearly_stats = (self.df_clean.groupby('year')['val']
                       .agg(['count', 'mean', 'std'])
                       .round(6))
        
        print(f"\n📅 Yearly Statistics (Sample):")
        print(yearly_stats.head(10))
        
        return {
            'disorders': disorder_stats,
            'measures': measure_stats,
            'yearly': yearly_stats
        }

def main():
    """Main analysis pipeline"""
    print("🚀 Mental Disorders Global Analysis - Data Portfolio")
    print("="*70)
    
    # Initialize analyzer
    data_path = "/Users/qinqin/Desktop/Mental_Disorders/Mental_Disorders_Raw_Data.csv"
    analyzer = MentalDisordersAnalyzer(data_path)
    
    # Load sample data first for initial analysis
    print("📥 Loading sample data for initial analysis...")
    analyzer.load_data(sample_size=500000)  # 500K rows sample
    
    # Explore the data
    basic_stats = analyzer.explore_data()
    
    # Clean the data  
    clean_data = analyzer.clean_data()
    
    # Generate summary statistics
    summary_stats = analyzer.create_summary_statistics()
    
    print(f"\n🎉 Initial analysis complete!")
    print(f"   📊 Ready for advanced analysis and visualization")
    print(f"   💾 Clean dataset available with {clean_data.shape[0]:,} rows")
    
    return analyzer

if __name__ == "__main__":
    analyzer = main()
