#!/usr/bin/env python3
"""
Create Sample Cleaned Dataset
============================

Extract 1000 rows from the raw data and apply cleaning transformations
to create a sample cleaned CSV file for testing and examples.

Question 1: Clean & Reshape Raw Data
"""

import pandas as pd
import os
from pathlib import Path

def create_sample_cleaned_data():
    """Create a sample of 1000 cleaned rows from the raw data"""
    
    # File paths
    base_dir = Path(__file__).parent.parent
    raw_data_path = base_dir / "data" / "Mental_Disorders_Raw_Data.csv"
    cleaned_sample_path = base_dir / "data" / "mental_disorders_sample_cleaned.csv"
    
    print("🔄 Creating sample cleaned dataset...")
    print(f"📂 Reading from: {raw_data_path}")
    
    try:
        # Use chunked reading to sample across all measures
        print("📊 Reading dataset in chunks to find all measures...")
        
        chunk_size = 1000000  # 1M rows per chunk
        df_samples = []
        measures_found = set()
        target_measures = {'Deaths', 'DALYs (Disability-Adjusted Life Years)', 
                          'YLDs (Years Lived with Disability)', 'YLLs (Years of Life Lost)',
                          'Prevalence', 'Incidence'}
        samples_per_measure = 166  # ~1000/6 measures
        
        for chunk in pd.read_csv(raw_data_path, chunksize=chunk_size):
            chunk_measures = set(chunk['measure_name'].unique())
            new_measures = chunk_measures - measures_found
            
            if new_measures:
                print(f"📊 Found new measures in chunk: {new_measures}")
                
                for measure in new_measures:
                    measure_data = chunk[chunk['measure_name'] == measure]
                    if len(measure_data) >= samples_per_measure:
                        sample = measure_data.sample(n=samples_per_measure, random_state=42)
                        df_samples.append(sample)
                        measures_found.add(measure)
                        print(f"   ✅ Sampled {len(sample)} rows for {measure}")
            
            # If we've found all target measures, we can stop
            if measures_found == target_measures:
                print("✅ Found all target measures!")
                break
                
            # Show progress
            if len(measures_found) > 0:
                print(f"📊 Progress: Found {len(measures_found)}/6 measures: {measures_found}")
        
        if df_samples:
            df_sample = pd.concat(df_samples, ignore_index=True)
        else:
            # Fallback to first chunk if no samples found
            print("⚠️ Fallback: Using first chunk...")
            df_sample = pd.read_csv(raw_data_path, nrows=1000)
        
        # Get overall statistics
        print(f"\n✅ Created diverse sample with {len(df_sample)} rows")
        measures_in_sample = df_sample['measure_name'].unique()
        years_range = f"{df_sample['year'].min()} - {df_sample['year'].max()}"
        countries_count = df_sample['location_name'].nunique()
        
        print(f"📊 Measures in sample: {measures_in_sample}")
        print(f"📅 Year range: {years_range}")
        print(f"🌍 Countries: {countries_count} unique")
        print(f"📋 Original columns: {list(df_sample.columns)}")
        
        # Show sample distribution
        print(f"📊 Sample distribution by measure:")
        print(df_sample['measure_name'].value_counts())
        print(f"📅 Sample year range: {df_sample['year'].min()} - {df_sample['year'].max()}")
        print(f"🌍 Sample countries: {df_sample['location_name'].nunique()} unique countries")
        
        # Apply cleaning transformations based on our SQL query
        print("🧹 Applying cleaning transformations...")
        
        # Select and rename columns (excluding ID columns)
        df_cleaned = df_sample[[
            'measure_name',
            'location_name', 
            'sex_name',
            'age_name',
            'cause_name',
            'year',
            'metric_name',
            'val',
            'upper',
            'lower'
        ]].copy()
        
        # Rename columns
        df_cleaned = df_cleaned.rename(columns={
            'measure_name': 'measure',
            'location_name': 'country',
            'sex_name': 'sex',
            'age_name': 'age_group',
            'cause_name': 'disorder',
            'metric_name': 'metric',
            'val': 'value',
            'upper': 'value_upper_bounce',
            'lower': 'value_lower_bounce'
        })
        
        # Clean age data - remove " years" suffix
        if 'age_group' in df_cleaned.columns:
            df_cleaned['age_group'] = df_cleaned['age_group'].str.replace(' years', '', regex=False)
        
        print(f"📋 Cleaned columns: {list(df_cleaned.columns)}")
        print(f"🎯 Sample age groups after cleaning: {df_cleaned['age_group'].unique()[:5]}")
        
        # Save cleaned sample
        print(f"💾 Saving cleaned sample to: {cleaned_sample_path}")
        df_cleaned.to_csv(cleaned_sample_path, index=False)
        
        print("✅ Sample cleaned dataset created successfully!")
        print(f"📊 Rows: {len(df_cleaned)}")
        print(f"📋 Columns: {len(df_cleaned.columns)}")
        
        # Display sample of cleaned data
        print("\n📋 Sample of cleaned data:")
        print(df_cleaned.head())
        
        return df_cleaned
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find {raw_data_path}")
        print("Please ensure the Mental_Disorders_Raw_Data.csv file is in the data folder")
        return None
    except Exception as e:
        print(f"❌ Error processing data: {e}")
        return None

if __name__ == "__main__":
    create_sample_cleaned_data()
