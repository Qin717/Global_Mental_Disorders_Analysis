"""
Database Configuration for Mental Health Analysis
===============================================

Configuration settings for database connections and analysis parameters.

Author: Data Analysis Portfolio
Date: September 2024
"""

import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    """Database connection configuration"""
    host: str = "localhost"
    port: int = 5432
    dbname: str = "mental_health_db"
    user: str = "postgres"
    password: str = "postgres"
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """Create config from environment variables"""
        return cls(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 5432)),
            dbname=os.getenv('DB_NAME', 'mental_health_db'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgres')
        )
    
    @property
    def connection_string(self) -> str:
        """Get SQLAlchemy connection string"""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"

@dataclass 
class AnalysisConfig:
    """Analysis configuration parameters"""
    chunk_size: int = 10000
    sample_size: int = 500000
    min_data_points: int = 5
    confidence_level: float = 0.95
    trend_threshold: float = 0.001
    correlation_threshold: float = 0.5
    
# Default configurations
DEFAULT_DB_CONFIG = DatabaseConfig()
DEFAULT_ANALYSIS_CONFIG = AnalysisConfig()

# Configuration for different environments
CONFIGS = {
    'development': {
        'database': DatabaseConfig(),
        'analysis': AnalysisConfig(sample_size=100000)
    },
    'production': {
        'database': DatabaseConfig.from_env(),
        'analysis': AnalysisConfig()
    },
    'testing': {
        'database': DatabaseConfig(dbname='mental_health_test_db'),
        'analysis': AnalysisConfig(sample_size=10000, chunk_size=1000)
    }
}

def get_config(environment: str = 'development') -> Dict[str, Any]:
    """Get configuration for specified environment"""
    return CONFIGS.get(environment, CONFIGS['development'])
