#!/usr/bin/env python3
"""
SQL Integration for Mental Disorders Analysis
============================================

This module provides SQL database integration capabilities for the mental disorders
dataset, including ETL processes, data loading, and advanced SQL analytics.

Features:
- PostgreSQL database connection and management
- ETL pipeline for CSV to database loading
- Advanced SQL query execution
- Data validation and quality checks
- Performance optimization

Author: Data Analysis Portfolio
Date: September 2024
"""

import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine, text
import logging
from pathlib import Path
import yaml
from typing import Dict, List, Optional, Tuple
import click
from tqdm import tqdm

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MentalHealthDatabase:
    """
    Database management class for mental health data analysis
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize database connection"""
        self.config = self._load_config(config_path)
        self.engine = None
        self.connection = None
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load database configuration"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Default configuration for local development
        return {
            'database': {
                'host': 'localhost',
                'port': 5432,
                'dbname': 'mental_health_db',
                'user': 'postgres',
                'password': 'postgres'
            }
        }
    
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            db_config = self.config['database']
            connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
            
            self.engine = create_engine(connection_string)
            self.connection = self.engine.connect()
            
            logger.info("✅ Database connection established successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()
        logger.info("🔌 Database connection closed")
    
    def execute_sql_file(self, sql_file_path: str) -> bool:
        """Execute SQL from file"""
        try:
            with open(sql_file_path, 'r') as f:
                sql_content = f.read()
            
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            for stmt in statements:
                if stmt:
                    self.connection.execute(text(stmt))
            
            self.connection.commit()
            logger.info(f"✅ SQL file executed successfully: {sql_file_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error executing SQL file {sql_file_path}: {e}")
            return False
    
    def load_csv_to_database(self, csv_path: str, chunk_size: int = 10000) -> bool:
        """Load CSV data to database with ETL processing"""
        try:
            logger.info(f"🔄 Starting ETL process for {csv_path}")
            
            # First, populate dimension tables
            self._populate_dimension_tables(csv_path, chunk_size)
            
            # Then load fact data
            self._load_fact_data(csv_path, chunk_size)
            
            # Refresh materialized views
            self._refresh_materialized_views()
            
            logger.info("✅ ETL process completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ ETL process failed: {e}")
            return False
    
    def _populate_dimension_tables(self, csv_path: str, chunk_size: int):
        """Populate dimension tables from CSV data"""
        logger.info("📊 Populating dimension tables...")
        
        # Read sample to get unique values
        sample_df = pd.read_csv(csv_path, nrows=100000)
        
        # Countries
        countries_data = []
        unique_countries = sample_df['location_name'].unique()
        
        for country in unique_countries:
            region = self._get_country_region(country)
            countries_data.append({
                'country_name': country,
                'region': region
            })
        
        countries_df = pd.DataFrame(countries_data)
        countries_df.to_sql('countries', self.engine, if_exists='append', index=False, method='multi')
        
        logger.info(f"✅ Loaded {len(countries_data)} countries")
    
    def _get_country_region(self, country: str) -> str:
        """Simple region classification"""
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
    
    def _load_fact_data(self, csv_path: str, chunk_size: int):
        """Load main fact data"""
        logger.info("📈 Loading fact data...")
        
        # Get dimension table mappings
        countries_map = pd.read_sql("SELECT country_id, country_name FROM countries", self.engine)
        countries_map = dict(zip(countries_map['country_name'], countries_map['country_id']))
        
        disorders_map = pd.read_sql("SELECT disorder_id, disorder_name FROM mental_disorders", self.engine)
        disorders_map = dict(zip(disorders_map['disorder_name'], disorders_map['disorder_id']))
        
        measures_map = pd.read_sql("SELECT measure_id, measure_name FROM health_measures", self.engine)
        measures_map = dict(zip(measures_map['measure_name'], measures_map['measure_id']))
        
        age_groups_map = pd.read_sql("SELECT age_group_id, age_group_name FROM age_groups", self.engine)
        age_groups_map = dict(zip(age_groups_map['age_group_name'], age_groups_map['age_group_id']))
        
        sex_map = pd.read_sql("SELECT sex_id, sex_name FROM sex_categories", self.engine)
        sex_map = dict(zip(sex_map['sex_name'], sex_map['sex_id']))
        
        # Process CSV in chunks
        total_rows = 0
        chunk_count = 0
        
        for chunk in tqdm(pd.read_csv(csv_path, chunksize=chunk_size), desc="Processing chunks"):
            # Map foreign keys
            chunk['country_id'] = chunk['location_name'].map(countries_map)
            chunk['disorder_id'] = chunk['cause_name'].map(disorders_map)
            chunk['measure_id'] = chunk['measure_name'].map(measures_map)
            chunk['age_group_id'] = chunk['age_name'].map(age_groups_map)
            chunk['sex_id'] = chunk['sex_name'].map(sex_map)
            
            # Prepare fact data
            fact_data = chunk[['country_id', 'disorder_id', 'measure_id', 'age_group_id', 
                              'sex_id', 'year', 'val', 'upper', 'lower']].copy()
            fact_data.columns = ['country_id', 'disorder_id', 'measure_id', 'age_group_id', 
                                'sex_id', 'year', 'value', 'upper_bound', 'lower_bound']
            
            # Remove rows with missing foreign keys
            fact_data = fact_data.dropna(subset=['country_id', 'disorder_id', 'measure_id', 
                                               'age_group_id', 'sex_id'])
            
            # Load to database
            fact_data.to_sql('mental_health_data', self.engine, if_exists='append', 
                           index=False, method='multi')
            
            total_rows += len(fact_data)
            chunk_count += 1
            
            if chunk_count % 10 == 0:
                logger.info(f"Processed {chunk_count} chunks, {total_rows:,} rows loaded")
        
        logger.info(f"✅ Loaded {total_rows:,} fact records")
    
    def _refresh_materialized_views(self):
        """Refresh materialized views"""
        logger.info("🔄 Refreshing materialized views...")
        self.connection.execute(text("SELECT refresh_all_materialized_views()"))
        self.connection.commit()
        logger.info("✅ Materialized views refreshed")
    
    def execute_analysis_query(self, query: str) -> pd.DataFrame:
        """Execute analytical SQL query"""
        try:
            result_df = pd.read_sql(query, self.engine)
            logger.info(f"✅ Query executed successfully, returned {len(result_df)} rows")
            return result_df
        except Exception as e:
            logger.error(f"❌ Query execution failed: {e}")
            return pd.DataFrame()
    
    def get_data_quality_report(self) -> Dict:
        """Generate data quality report"""
        logger.info("📊 Generating data quality report...")
        
        quality_report = {}
        
        # Basic counts
        total_records = self.execute_analysis_query("SELECT COUNT(*) as count FROM mental_health_data")
        quality_report['total_records'] = total_records.iloc[0]['count'] if not total_records.empty else 0
        
        # Coverage by dimension
        countries_count = self.execute_analysis_query("SELECT COUNT(DISTINCT country_id) as count FROM mental_health_data")
        quality_report['countries_covered'] = countries_count.iloc[0]['count'] if not countries_count.empty else 0
        
        disorders_count = self.execute_analysis_query("SELECT COUNT(DISTINCT disorder_id) as count FROM mental_health_data")
        quality_report['disorders_covered'] = disorders_count.iloc[0]['count'] if not disorders_count.empty else 0
        
        # Time coverage
        time_range = self.execute_analysis_query("SELECT MIN(year) as min_year, MAX(year) as max_year FROM mental_health_data")
        if not time_range.empty:
            quality_report['time_range'] = {
                'min_year': int(time_range.iloc[0]['min_year']),
                'max_year': int(time_range.iloc[0]['max_year'])
            }
        
        # Data completeness
        completeness = self.execute_analysis_query("""
            SELECT 
                COUNT(*) as total,
                COUNT(value) as value_complete,
                COUNT(upper_bound) as upper_complete,
                COUNT(lower_bound) as lower_complete
            FROM mental_health_data
        """)
        
        if not completeness.empty:
            row = completeness.iloc[0]
            quality_report['completeness'] = {
                'value': row['value_complete'] / row['total'] * 100,
                'upper_bound': row['upper_complete'] / row['total'] * 100,
                'lower_bound': row['lower_complete'] / row['total'] * 100
            }
        
        logger.info("✅ Data quality report generated")
        return quality_report

@click.group()
def cli():
    """Mental Health Database Management CLI"""
    pass

@cli.command()
@click.option('--config', '-c', help='Configuration file path')
@click.option('--schema-file', '-s', default='src/sql/schema/create_tables.sql', help='Schema SQL file')
def setup_database(config, schema_file):
    """Set up database schema"""
    db = MentalHealthDatabase(config)
    
    if db.connect():
        success = db.execute_sql_file(schema_file)
        if success:
            click.echo("✅ Database schema created successfully")
        else:
            click.echo("❌ Failed to create database schema")
        db.disconnect()

@cli.command()
@click.option('--config', '-c', help='Configuration file path')
@click.option('--csv-path', '-f', required=True, help='Path to CSV data file')
@click.option('--chunk-size', '-s', default=10000, help='Chunk size for processing')
def load_data(config, csv_path, chunk_size):
    """Load CSV data into database"""
    db = MentalHealthDatabase(config)
    
    if db.connect():
        success = db.load_csv_to_database(csv_path, chunk_size)
        if success:
            click.echo("✅ Data loaded successfully")
        else:
            click.echo("❌ Failed to load data")
        db.disconnect()

@cli.command()
@click.option('--config', '-c', help='Configuration file path')
def quality_report(config):
    """Generate data quality report"""
    db = MentalHealthDatabase(config)
    
    if db.connect():
        report = db.get_data_quality_report()
        
        click.echo("\n📊 DATA QUALITY REPORT")
        click.echo("=" * 30)
        click.echo(f"Total records: {report.get('total_records', 0):,}")
        click.echo(f"Countries covered: {report.get('countries_covered', 0)}")
        click.echo(f"Disorders covered: {report.get('disorders_covered', 0)}")
        
        if 'time_range' in report:
            time_range = report['time_range']
            click.echo(f"Time range: {time_range['min_year']} - {time_range['max_year']}")
        
        if 'completeness' in report:
            completeness = report['completeness']
            click.echo(f"Data completeness:")
            click.echo(f"  Value: {completeness['value']:.1f}%")
            click.echo(f"  Upper bound: {completeness['upper_bound']:.1f}%")
            click.echo(f"  Lower bound: {completeness['lower_bound']:.1f}%")
        
        db.disconnect()

if __name__ == "__main__":
    cli()
