#!/usr/bin/env python3
"""
Advanced Data Reshaping for Mental Disorders Analysis
====================================================

This script provides advanced data reshaping capabilities for the mental disorders dataset,
creating pivot tables, aggregations, and analytical datasets ready for machine learning
and statistical modeling.

Author: Data Analysis Portfolio
Date: September 2024
"""

import pandas as pd
import numpy as np
from pathlib import Path

class MentalHealthDataReshaper:
    """
    Advanced data reshaping class for mental health analysis
    """
    
    def __init__(self, data_path, sample_size=500000):
        """Initialize with data path and sample size"""
        self.data_path = Path(data_path)
        self.sample_size = sample_size
        self.df = None
        self.reshaped_data = {}
        
    def load_and_clean_data(self):
        """Load and clean the dataset"""
        print("📥 Loading mental disorders dataset...")
        self.df = pd.read_csv(self.data_path, nrows=self.sample_size)
        
        # Data cleaning
        categorical_cols = ['measure_name', 'location_name', 'sex_name', 'age_name', 'cause_name', 'metric_name']
        for col in categorical_cols:
            self.df[col] = self.df[col].astype('category')
        
        # Ensure numeric columns are proper types
        numeric_cols = ['val', 'upper', 'lower']
        for col in numeric_cols:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        self.df['year'] = self.df['year'].astype(int)
        
        print(f"✅ Dataset loaded and cleaned: {self.df.shape[0]:,} rows")
        return self.df
    
    def create_disorder_country_matrix(self):
        """Create disorder-country prevalence matrix"""
        print("🔄 Creating disorder-country matrix...")
        
        matrix = self.df.pivot_table(
            values='val',
            index='location_name',
            columns='cause_name',
            aggfunc='mean',
            fill_value=0
        )
        
        self.reshaped_data['disorder_country_matrix'] = matrix
        print(f"✅ Matrix created: {matrix.shape[0]} countries x {matrix.shape[1]} disorders")
        return matrix
    
    def create_temporal_trends_data(self):
        """Create temporal trends dataset"""
        print("📈 Creating temporal trends data...")
        
        trends = self.df.groupby(['year', 'cause_name', 'measure_name'])['val'].agg([
            'mean', 'median', 'std', 'count'
        ]).reset_index()
        
        # Pivot to wide format for easier analysis
        trends_pivot = trends.pivot_table(
            values=['mean', 'median', 'std'],
            index=['year', 'cause_name'],
            columns='measure_name',
            fill_value=0
        )
        
        self.reshaped_data['temporal_trends'] = trends_pivot
        print(f"✅ Temporal trends created: {trends_pivot.shape[0]} time-disorder combinations")
        return trends_pivot
    
    def create_demographic_analysis_data(self):
        """Create demographic analysis datasets"""
        print("👥 Creating demographic analysis data...")
        
        # Age-Sex-Disorder analysis
        demo_data = self.df.groupby(['age_name', 'sex_name', 'cause_name'])['val'].agg([
            'mean', 'std', 'count'
        ]).reset_index()
        
        # Create age-sex matrix for each disorder
        demographic_matrices = {}
        for disorder in self.df['cause_name'].unique():
            disorder_data = self.df[self.df['cause_name'] == disorder]
            matrix = disorder_data.pivot_table(
                values='val',
                index='age_name',
                columns='sex_name',
                aggfunc='mean',
                fill_value=0
            )
            demographic_matrices[disorder] = matrix
        
        self.reshaped_data['demographic_summary'] = demo_data
        self.reshaped_data['demographic_matrices'] = demographic_matrices
        
        print(f"✅ Demographic data created: {len(demographic_matrices)} disorder-specific matrices")
        return demo_data, demographic_matrices
    
    def create_geographic_aggregations(self):
        """Create geographic aggregations and regional data"""
        print("🌍 Creating geographic aggregations...")
        
        # Simple regional classification
        def get_region(country):
            europe = ['United Kingdom', 'Germany', 'France', 'Spain', 'Italy', 'Netherlands', 
                     'Poland', 'Romania', 'Greece', 'Portugal', 'Belgium', 'Czech Republic',
                     'Hungary', 'Sweden', 'Austria', 'Belarus', 'Switzerland', 'Bulgaria',
                     'Serbia', 'Denmark', 'Finland', 'Slovakia', 'Norway', 'Ireland', 'Croatia']
            
            asia = ['China', 'India', 'Japan', 'Indonesia', 'Pakistan', 'Bangladesh', 'Vietnam',
                   'Philippines', 'Turkey', 'Iran', 'Thailand', 'Myanmar', 'South Korea',
                   'Iraq', 'Afghanistan', 'Uzbekistan', 'Malaysia', 'Nepal', 'Sri Lanka']
            
            africa = ['Nigeria', 'Ethiopia', 'Egypt', 'South Africa', 'Kenya', 'Uganda', 'Algeria',
                     'Sudan', 'Morocco', 'Angola', 'Ghana', 'Mozambique', 'Madagascar', 'Cameroon']
            
            americas = ['United States', 'Brazil', 'Mexico', 'Canada', 'Argentina', 'Colombia',
                       'Peru', 'Venezuela', 'Chile', 'Ecuador', 'Guatemala', 'Cuba', 'Bolivia']
            
            if country in europe:
                return 'Europe'
            elif country in asia:
                return 'Asia'
            elif country in africa:
                return 'Africa'
            elif country in americas:
                return 'Americas'
            else:
                return 'Other/Oceania'
        
        self.df['region'] = self.df['location_name'].apply(get_region)
        
        # Regional aggregations
        regional_data = self.df.groupby(['region', 'cause_name', 'measure_name'])['val'].agg([
            'mean', 'std', 'count', 'min', 'max'
        ]).reset_index()
        
        # Country rankings
        country_rankings = self.df.groupby(['location_name', 'cause_name'])['val'].mean().reset_index()
        country_rankings['rank'] = country_rankings.groupby('cause_name')['val'].rank(ascending=False)
        
        self.reshaped_data['regional_data'] = regional_data
        self.reshaped_data['country_rankings'] = country_rankings
        
        print(f"✅ Geographic data created: {len(regional_data)} regional aggregations")
        return regional_data, country_rankings
    
    def create_summary_statistics(self):
        """Create comprehensive summary statistics"""
        print("📊 Creating summary statistics...")
        
        # Overall statistics by disorder
        disorder_stats = self.df.groupby('cause_name')['val'].agg([
            'count', 'mean', 'median', 'std', 'min', 'max', 
            lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)
        ]).round(6)
        
        disorder_stats.columns = ['Count', 'Mean', 'Median', 'Std', 'Min', 'Max', 'Q25', 'Q75']
        
        # Statistics by health measure
        measure_stats = self.df.groupby('measure_name')['val'].agg([
            'count', 'mean', 'median', 'std', 'min', 'max'
        ]).round(6)
        
        # Temporal summary
        yearly_stats = self.df.groupby('year')['val'].agg([
            'count', 'mean', 'std'
        ]).round(6)
        
        self.reshaped_data['disorder_statistics'] = disorder_stats
        self.reshaped_data['measure_statistics'] = measure_stats
        self.reshaped_data['yearly_statistics'] = yearly_stats
        
        print(f"✅ Summary statistics created")
        return disorder_stats, measure_stats, yearly_stats
    
    def export_reshaped_data(self, output_dir=None):
        """Export all reshaped datasets to CSV files"""
        if output_dir is None:
            output_dir = self.data_path.parent / "reshaped_data"
        
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        print(f"💾 Exporting reshaped data to {output_dir}...")
        
        # Export each dataset
        for name, data in self.reshaped_data.items():
            if isinstance(data, dict):
                # Handle nested datasets (like demographic matrices)
                sub_dir = output_dir / name
                sub_dir.mkdir(exist_ok=True)
                for sub_name, sub_data in data.items():
                    filename = f"{sub_name.replace('/', '_').replace(' ', '_')}.csv"
                    sub_data.to_csv(sub_dir / filename)
            else:
                filename = f"{name}.csv"
                data.to_csv(output_dir / filename)
        
        print(f"✅ All datasets exported to {output_dir}")
        return output_dir
    
    def get_analysis_ready_dataset(self):
        """Create a final analysis-ready dataset with key features"""
        print("🎯 Creating analysis-ready dataset...")
        
        # Add derived features
        self.df['log_val'] = np.log1p(self.df['val'])  # Log transform for skewed data
        self.df['confidence_interval_width'] = self.df['upper'] - self.df['lower']
        self.df['relative_uncertainty'] = self.df['confidence_interval_width'] / self.df['val']
        self.df['relative_uncertainty'] = self.df['relative_uncertainty'].replace([np.inf, -np.inf], np.nan)
        
        # Add time-based features
        self.df['decade'] = (self.df['year'] // 10) * 10
        self.df['years_since_1980'] = self.df['year'] - 1980
        
        # Add categorical encodings for ML
        analysis_df = self.df.copy()
        
        # Label encoding for categorical variables
        categorical_columns = ['cause_name', 'measure_name', 'location_name', 'sex_name', 'age_name', 'region']
        for col in categorical_columns:
            if col in analysis_df.columns:
                analysis_df[f'{col}_encoded'] = pd.Categorical(analysis_df[col]).codes
        
        self.reshaped_data['analysis_ready'] = analysis_df
        
        print(f"✅ Analysis-ready dataset created: {analysis_df.shape[0]:,} rows x {analysis_df.shape[1]} columns")
        return analysis_df
    
    def run_complete_reshaping(self):
        """Run the complete data reshaping pipeline"""
        print("🚀 Starting complete data reshaping pipeline...")
        print("=" * 60)
        
        # Load data
        self.load_and_clean_data()
        
        # Create all reshaped datasets
        self.create_disorder_country_matrix()
        self.create_temporal_trends_data()
        self.create_demographic_analysis_data()
        self.create_geographic_aggregations()
        self.create_summary_statistics()
        self.get_analysis_ready_dataset()
        
        print("\n" + "=" * 60)
        print("🎉 Data reshaping complete!")
        print(f"📊 Created {len(self.reshaped_data)} reshaped datasets")
        print("🎯 Ready for advanced analysis and machine learning")
        
        return self.reshaped_data

def main():
    """Main execution function"""
    data_path = "/Users/qinqin/Desktop/Mental_Disorders/Mental_Disorders_Raw_Data.csv"
    
    # Initialize reshaper
    reshaper = MentalHealthDataReshaper(data_path, sample_size=500000)
    
    # Run complete reshaping
    reshaped_data = reshaper.run_complete_reshaping()
    
    # Export data
    output_dir = reshaper.export_reshaped_data()
    
    print(f"\n📋 Summary of reshaped datasets:")
    for name, data in reshaped_data.items():
        if isinstance(data, pd.DataFrame):
            print(f"   • {name}: {data.shape[0]:,} rows x {data.shape[1]} columns")
        else:
            print(f"   • {name}: Multiple sub-datasets")
    
    return reshaper

if __name__ == "__main__":
    reshaper = main()
