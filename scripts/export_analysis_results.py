#!/usr/bin/env python3
"""
Export Analysis Results to CSV Files
=====================================

Generates CSV files for the two main analysis questions:
1. Mental Disorder Growth Analysis (1990-2021)
2. Age Group Trends Analysis (1990-2021)

Author: Data Analysis Portfolio
Date: September 2024
"""

import pandas as pd
import sqlite3
from pathlib import Path

class AnalysisResultsExporter:
    """Export analysis results to CSV files"""
    
    def __init__(self, db_path, output_dir=""):
        self.db_path = Path(db_path)
        self.output_dir = Path(output_dir) if output_dir else Path(".")
        self.conn = sqlite3.connect(self.db_path)
        
    def execute_query(self, query):
        """Execute SQL query and return DataFrame"""
        return pd.read_sql_query(query, self.conn)
    
    def export_disorder_growth_analysis(self):
        """Question 2: Mental Disorder Growth Analysis (1990-2021)"""
        
        print("📊 Exporting Mental Disorder Growth Analysis...")
        
        query = """
        WITH baseline AS (
            SELECT disorder, AVG(value) AS val_1990
            FROM mental_disorders_raw_data_cleaned
            WHERE year = 1990
              AND metric = 'Percent'
              AND sex = 'Both'
              AND disorder IN ('Depressive disorders',
                               'Anxiety disorders',
                               'Schizophrenia',
                               'Bipolar disorder',
                               'Eating disorders')
            GROUP BY disorder
        ),
        latest AS (
            SELECT disorder, AVG(value) AS val_2021
            FROM mental_disorders_raw_data_cleaned
            WHERE year = 2021
              AND metric = 'Percent'
              AND sex = 'Both'
              AND disorder IN ('Depressive disorders',
                               'Anxiety disorders',
                               'Schizophrenia',
                               'Bipolar disorder',
                               'Eating disorders')
            GROUP BY disorder
        )
        SELECT l.disorder,
               ROUND((b.val_1990 * 100), 2) AS prevalence_1990_percent,
               ROUND((l.val_2021 * 100), 2) AS prevalence_2021_percent,
               ROUND(((l.val_2021 - b.val_1990) * 100), 2) AS change_percentage_points,
               ROUND(((l.val_2021 - b.val_1990) / NULLIF(b.val_1990,0) * 100), 1) AS relative_growth_percent
        FROM latest l
        JOIN baseline b USING (disorder)
        ORDER BY relative_growth_percent DESC;
        """
        
        df = self.execute_query(query)
        
        # Add metadata columns
        df['analysis_period'] = '1990-2021'
        df['analysis_type'] = 'Mental Disorder Growth'
        df['data_source'] = 'Global Burden of Disease Study'
        
        # Save to CSV
        output_path = self.output_dir / 'mental_disorder_growth_analysis.csv'
        df.to_csv(output_path, index=False)
        
        print(f"✅ Mental Disorder Growth Analysis exported to: {output_path}")
        print(f"   📋 {len(df)} disorders analyzed")
        
        return df
    
    def export_age_group_trends_analysis(self):
        """Question 3: Age Group Trends Analysis (1990-2021)"""
        
        print("\n📊 Exporting Age Group Trends Analysis...")
        
        query = """
        WITH baseline AS (
            SELECT age_group, AVG(value) AS val_1990
            FROM mental_disorders_raw_data_cleaned
            WHERE year = 1990
              AND sex = 'Both'
            GROUP BY age_group
        ),
        latest AS (
            SELECT age_group, AVG(value) AS val_2021
            FROM mental_disorders_raw_data_cleaned
            WHERE year = 2021
              AND sex = 'Both'
            GROUP BY age_group
        )
        SELECT l.age_group,
               ROUND((b.val_1990 * 100), 2) AS prevalence_1990_percent,
               ROUND((l.val_2021 * 100), 2) AS prevalence_2021_percent,
               ROUND(((l.val_2021 - b.val_1990) * 100), 2) AS change_percentage_points,
               ROUND(((l.val_2021 - b.val_1990) / NULLIF(b.val_1990,0) * 100), 1) AS relative_growth_percent
        FROM latest l
        JOIN baseline b USING (age_group)
        ORDER BY relative_growth_percent DESC;
        """
        
        df = self.execute_query(query)
        
        # Add metadata columns
        df['analysis_period'] = '1990-2021'
        df['analysis_type'] = 'Age Group Trends'
        df['data_source'] = 'Global Burden of Disease Study'
        
        # Add trend classification
        df['trend_category'] = df['relative_growth_percent'].apply(
            lambda x: 'High Growth' if x > 20 else 
                     'Moderate Growth' if x > 10 else 
                     'Low Growth' if x > 0 else 'Decline'
        )
        
        # Save to CSV
        output_path = self.output_dir / 'age_group_trends_analysis.csv'
        df.to_csv(output_path, index=False)
        
        print(f"✅ Age Group Trends Analysis exported to: {output_path}")
        print(f"   📋 {len(df)} age groups analyzed")
        
        return df
    
    def export_summary_report(self, disorder_df, age_df):
        """Create a summary report combining both analyses"""
        
        print("\n📊 Creating Summary Report...")
        
        # Create summary statistics
        summary_data = {
            'Analysis Type': ['Mental Disorder Growth', 'Age Group Trends'],
            'Total Records': [len(disorder_df), len(age_df)],
            'Highest Growth Item': [
                disorder_df.iloc[0]['disorder'],
                age_df.iloc[0]['age_group']
            ],
            'Highest Growth Rate (%)': [
                disorder_df.iloc[0]['relative_growth_percent'],
                age_df.iloc[0]['relative_growth_percent']
            ],
            'Average Growth Rate (%)': [
                disorder_df['relative_growth_percent'].mean(),
                age_df['relative_growth_percent'].mean()
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        
        # Save summary
        output_path = self.output_dir / 'analysis_summary_report.csv'
        summary_df.to_csv(output_path, index=False)
        
        print(f"✅ Summary Report exported to: {output_path}")
        
        return summary_df
    
    def export_all_results(self):
        """Export all analysis results to CSV files"""
        print("🚀 Mental Disorders Analysis - CSV Export")
        print("=" * 60)
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
        
        # Export both analyses
        disorder_results = self.export_disorder_growth_analysis()
        age_results = self.export_age_group_trends_analysis()
        summary_results = self.export_summary_report(disorder_results, age_results)
        
        print(f"\n🎉 All CSV files exported successfully!")
        print(f"📁 Output directory: {self.output_dir.absolute()}")
        
        # Print key findings
        print(f"\n📈 Key Findings Summary:")
        print(f"   🧠 Top Growing Disorder: {disorder_results.iloc[0]['disorder']} ({disorder_results.iloc[0]['relative_growth_percent']:.1f}%)")
        print(f"   👥 Top Growing Age Group: {age_results.iloc[0]['age_group']} ({age_results.iloc[0]['relative_growth_percent']:.1f}%)")
        
        return {
            'disorder_growth': disorder_results,
            'age_trends': age_results,
            'summary': summary_results
        }
    
    def close(self):
        """Close database connection"""
        self.conn.close()

def main():
    """Main execution function"""
    print("🚀 Mental Disorders Analysis - CSV Results Exporter")
    print("=" * 70)
    
    # Database and output paths
    db_path = "/Users/qinqin/Desktop/Mental_Disorders/mental_disorders.db"
    output_dir = "/Users/qinqin/Desktop/Mental_Disorders/reports"
    
    # Check if database exists
    if not Path(db_path).exists():
        print(f"❌ Database not found: {db_path}")
        print("Please ensure the database has been created from your SQL queries.")
        return
    
    # Create exporter
    exporter = AnalysisResultsExporter(db_path, output_dir)
    
    try:
        # Export all results
        results = exporter.export_all_results()
        
    except Exception as e:
        print(f"❌ Error exporting results: {e}")
        print("Please check that your database contains the required tables and data.")
    
    finally:
        exporter.close()

if __name__ == "__main__":
    main()
