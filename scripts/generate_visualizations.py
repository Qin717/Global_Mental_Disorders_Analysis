#!/usr/bin/env python3
"""
Mental Disorders Analysis - Visualization Generator
================================================

Generates visualizations for the three main analysis questions:
1. Data overview and distribution
2. Mental disorder growth trends (1990-2021)
3. Age group trend analysis (1990-2021)

Author: Data Analysis Portfolio
Date: September 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up visualization style to match the original mental_disorder_analysis_results.png exactly
plt.style.use('seaborn-v0_8')
# Use the exact colors from the original chart
original_colors = ['#5B9BD5', '#70AD47', '#4F81BD', '#9BBB59', '#F79646']  # Blue, Green, Dark Blue, Light Green, Orange
sns.set_palette(original_colors)
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

class MentalDisordersVisualizer:
    """Generate comprehensive visualizations for mental disorders analysis"""
    
    def __init__(self, db_path, output_dir=""):
        self.db_path = Path(db_path)
        self.output_dir = Path(output_dir) if output_dir else Path(".")
        self.conn = sqlite3.connect(self.db_path)
        
    def execute_query(self, query):
        """Execute SQL query and return DataFrame"""
        return pd.read_sql_query(query, self.conn)
    
    def visualize_disorder_growth_trends(self):
        """Question 2: Mental Disorder Growth Analysis (1990-2021)"""
        
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
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Mental Disorder Growth Analysis (1990-2021)', fontsize=16, fontweight='bold')
        
        # 1. Prevalence comparison (1990 vs 2021)
        x = np.arange(len(df))
        width = 0.35
        
        ax1.bar(x - width/2, df['prevalence_1990_percent'], width, 
                label='1990', alpha=0.8)
        ax1.bar(x + width/2, df['prevalence_2021_percent'], width,
                label='2021', alpha=0.8)
        
        ax1.set_xlabel('Mental Disorders')
        ax1.set_ylabel('Prevalence (%)')
        ax1.set_title('Prevalence Comparison: 1990 vs 2021')
        ax1.set_xticks(x)
        ax1.set_xticklabels(df['disorder'], rotation=45, ha='right')
        ax1.legend()
        
        # 2. Absolute change in percentage points
        bars = ax2.bar(df['disorder'], df['change_percentage_points'], alpha=0.7)
        ax2.set_xlabel('Mental Disorders')
        ax2.set_ylabel('Change (Percentage Points)')
        ax2.set_title('Absolute Change in Prevalence (1990-2021)')
        ax2.tick_params(axis='x', rotation=45)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va='bottom' if height > 0 else 'top')
        
        # 3. Relative growth percentage
        bars = ax3.bar(df['disorder'], df['relative_growth_percent'], alpha=0.7)
        ax3.set_xlabel('Mental Disorders')
        ax3.set_ylabel('Relative Growth (%)')
        ax3.set_title('Relative Growth Rate (1990-2021)')
        ax3.tick_params(axis='x', rotation=45)
        ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom' if height > 0 else 'top')
        
        # 4. Time series trend for top disorders
        trend_query = """
        SELECT year, disorder, AVG(value * 100) as prevalence
        FROM mental_disorders_raw_data_cleaned
        WHERE metric = 'Percent'
          AND sex = 'Both'
          AND disorder IN ('Depressive disorders', 'Anxiety disorders', 'Eating disorders')
          AND year BETWEEN 1990 AND 2021
        GROUP BY year, disorder
        ORDER BY year, disorder;
        """
        
        trend_df = self.execute_query(trend_query)
        
        for disorder in trend_df['disorder'].unique():
            disorder_data = trend_df[trend_df['disorder'] == disorder]
            ax4.plot(disorder_data['year'], disorder_data['prevalence'], 
                    marker='o', linewidth=2, label=disorder)
        
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Prevalence (%)')
        ax4.set_title('Prevalence Trends Over Time')
        ax4.legend()
        
        plt.tight_layout()
        
        # Save the plot
        output_path = self.output_dir / 'mental_disorder_growth_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved disorder growth analysis: {output_path}")
        
        return df
    
    def visualize_age_group_trends(self):
        """Question 3: Age Group Trends Analysis (1990-2021)"""
        
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
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Age Group Mental Health Trends (1990-2021)', fontsize=16, fontweight='bold')
        
        # 1. Prevalence comparison by age group
        x = np.arange(len(df))
        width = 0.35
        
        ax1.bar(x - width/2, df['prevalence_1990_percent'], width,
                label='1990', alpha=0.8)
        ax1.bar(x + width/2, df['prevalence_2021_percent'], width,
                label='2021', alpha=0.8)
        
        ax1.set_xlabel('Age Groups')
        ax1.set_ylabel('Prevalence (%)')
        ax1.set_title('Mental Health Prevalence by Age Group')
        ax1.set_xticks(x)
        ax1.set_xticklabels(df['age_group'], rotation=45, ha='right')
        ax1.legend()
        
        # 2. Change in percentage points
        bars = ax2.bar(df['age_group'], df['change_percentage_points'], alpha=0.7)
        ax2.set_xlabel('Age Groups')
        ax2.set_ylabel('Change (Percentage Points)')
        ax2.set_title('Absolute Change by Age Group')
        ax2.tick_params(axis='x', rotation=45)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va='bottom' if height > 0 else 'top')
        
        # 3. Relative growth by age group - use green color scheme
        bars = ax3.bar(df['age_group'], df['relative_growth_percent'], alpha=0.7, color='#70AD47')
        ax3.set_xlabel('Age Groups')
        ax3.set_ylabel('Relative Growth (%)')
        ax3.set_title('Relative Growth Rate by Age Group')
        ax3.tick_params(axis='x', rotation=45)
        ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom' if height > 0 else 'top')
        
        # 4. Heatmap of trends by age group
        # Get time series data for all age groups
        heatmap_query = """
        SELECT year, age_group, AVG(value * 100) as prevalence
        FROM mental_disorders_raw_data_cleaned
        WHERE metric = 'Percent'
          AND sex = 'Both'
          AND year BETWEEN 1990 AND 2021
          AND year % 5 = 0  -- Every 5 years for readability
        GROUP BY year, age_group
        ORDER BY year, age_group;
        """
        
        heatmap_df = self.execute_query(heatmap_query)
        pivot_df = heatmap_df.pivot(index='age_group', columns='year', values='prevalence')
        
        # Create custom colormap using the same blue-green colors from the original
        from matplotlib.colors import LinearSegmentedColormap
        colors_for_heatmap = ['#E8F4FD', '#5B9BD5', '#4F81BD', '#70AD47']  # Light blue to dark blue to green
        custom_cmap = LinearSegmentedColormap.from_list('custom_blue_green', colors_for_heatmap)
        
        sns.heatmap(pivot_df, annot=True, fmt='.1f', ax=ax4, cmap=custom_cmap, cbar_kws={'label': 'Prevalence (%)'})
        ax4.set_title('Mental Health Prevalence Heatmap (Every 5 Years)')
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Age Group')
        
        plt.tight_layout()
        
        # Save the plot
        output_path = self.output_dir / 'age_group_trends_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved age group trends analysis: {output_path}")
        
        return df
    
    def create_overview_dashboard(self):
        """Create a comprehensive overview dashboard"""
        
        # Get basic data overview
        overview_query = """
        SELECT 
            COUNT(*) as total_records,
            COUNT(DISTINCT country) as countries,
            COUNT(DISTINCT disorder) as disorders,
            COUNT(DISTINCT age_group) as age_groups,
            MIN(year) as min_year,
            MAX(year) as max_year
        FROM mental_disorders_raw_data_cleaned;
        """
        
        overview = self.execute_query(overview_query).iloc[0]
        
        # Get disorder distribution
        disorder_query = """
        SELECT disorder, COUNT(*) as records
        FROM mental_disorders_raw_data_cleaned
        GROUP BY disorder
        ORDER BY records DESC;
        """
        
        disorder_df = self.execute_query(disorder_query)
        
        # Create overview figure
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Mental Disorders Dataset Overview', fontsize=16, fontweight='bold')
        
        # 1. Dataset statistics
        stats_text = f"""
        Dataset Overview:
        
        📊 Total Records: {overview['total_records']:,}
        🌍 Countries: {overview['countries']}
        🧠 Mental Disorders: {overview['disorders']}
        👥 Age Groups: {overview['age_groups']}
        📅 Time Period: {overview['min_year']} - {overview['max_year']}
        """
        
        ax1.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.axis('off')
        ax1.set_title('Dataset Statistics')
        
        # 2. Disorder distribution pie chart
        ax2.pie(disorder_df['records'], labels=disorder_df['disorder'], autopct='%1.1f%%',
                startangle=90)
        ax2.set_title('Distribution of Records by Disorder')
        
        # 3. Records by year
        year_query = """
        SELECT year, COUNT(*) as records
        FROM mental_disorders_raw_data_cleaned
        GROUP BY year
        ORDER BY year;
        """
        
        year_df = self.execute_query(year_query)
        ax3.plot(year_df['year'], year_df['records'], marker='o', linewidth=2)
        ax3.set_xlabel('Year')
        ax3.set_ylabel('Number of Records')
        ax3.set_title('Data Coverage by Year')
        
        # 4. Top countries by data points
        country_query = """
        SELECT country, COUNT(*) as records
        FROM mental_disorders_raw_data_cleaned
        GROUP BY country
        ORDER BY records DESC
        LIMIT 10;
        """
        
        country_df = self.execute_query(country_query)
        ax4.barh(country_df['country'], country_df['records'])
        ax4.set_xlabel('Number of Records')
        ax4.set_title('Top 10 Countries by Data Points')
        
        plt.tight_layout()
        
        # Save the plot
        output_path = self.output_dir / 'dataset_overview_dashboard.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved overview dashboard: {output_path}")
    
    def generate_all_visualizations(self):
        """Generate remaining visualizations with consistent color scheme"""
        print("🎨 Generating Mental Disorders Analysis Visualizations...")
        print("=" * 60)
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
        
        # Generate only age group trends analysis
        print("\n🔄 Creating age group trends analysis with consistent colors...")
        age_results = self.visualize_age_group_trends()
        
        print(f"\n🎉 Visualization generated successfully!")
        print(f"📁 Output directory: {self.output_dir.absolute()}")
        
        return {
            'age_trends': age_results
        }
    
    def close(self):
        """Close database connection"""
        self.conn.close()

def main():
    """Main execution function"""
    print("🚀 Mental Disorders Analysis - Visualization Generator")
    print("=" * 70)
    
    # Database and output paths
    db_path = "/Users/qinqin/Desktop/Mental_Disorders/mental_disorders.db"
    output_dir = "/Users/qinqin/Desktop/Mental_Disorders/reports/figures"
    
    # Check if database exists
    if not Path(db_path).exists():
        print(f"❌ Database not found: {db_path}")
        print("Please ensure the database has been created from your SQL queries.")
        return
    
    # Create visualizer
    visualizer = MentalDisordersVisualizer(db_path, output_dir)
    
    try:
        # Generate all visualizations
        results = visualizer.generate_all_visualizations()
        
        print("\n📊 Analysis Results Summary:")
        print("-" * 40)
        
        if 'age_trends' in results:
            print("\n👥 Age Group Trends (1990-2021):")
            top_age_growth = results['age_trends'].head(3)
            for _, row in top_age_growth.iterrows():
                print(f"   • {row['age_group']}: {row['relative_growth_percent']:.1f}% growth")
        
    except Exception as e:
        print(f"❌ Error generating visualizations: {e}")
        print("Please check that your database contains the required tables and data.")
    
    finally:
        visualizer.close()

if __name__ == "__main__":
    main()
