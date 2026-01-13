"""
Data Processing Module
Handles data loading from various sources
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List
import logging
from pathlib import Path
import os

# Optional database imports
try:
    import pymongo
    HAS_MONGODB = True
except ImportError:
    HAS_MONGODB = False

try:
    from sqlalchemy import create_engine
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False

logger = logging.getLogger(__name__)


class DataProcessor:
    """Handles data loading from various sources"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.data = None
        
    def load_from_file(self, filepath: str) -> pd.DataFrame:
        """Load data from file (CSV, Excel)"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        extension = filepath.suffix.lower()
        
        try:
            if extension == '.csv':
                df = pd.read_csv(filepath)
            elif extension in ['.xlsx', '.xls']:
                df = pd.read_excel(filepath)
            elif extension == '.json':
                df = pd.read_json(filepath)
            else:
                raise ValueError(f"Unsupported file format: {extension}")
            
            logger.info(f"Loaded data from {filepath}: {df.shape}")
            self.data = df
            return df
            
        except Exception as e:
            logger.error(f"Error loading file: {str(e)}")
            raise
    
    def load_from_mongodb(self, 
                         connection_string: str,
                         database: str,
                         collection: str,
                         query: Optional[Dict] = None) -> pd.DataFrame:
        """Load data from MongoDB"""
        if not HAS_MONGODB:
            raise ImportError("pymongo is not installed. Install it with: pip install pymongo")
        
        try:
            client = pymongo.MongoClient(connection_string)
            db = client[database]
            collection_obj = db[collection]
            
            # Execute query
            if query:
                cursor = collection_obj.find(query)
            else:
                cursor = collection_obj.find()
            
            # Convert to DataFrame
            df = pd.DataFrame(list(cursor))
            
            # Remove MongoDB _id if present
            if '_id' in df.columns:
                df = df.drop('_id', axis=1)
            
            logger.info(f"Loaded data from MongoDB: {df.shape}")
            self.data = df
            return df
            
        except Exception as e:
            logger.error(f"Error loading from MongoDB: {str(e)}")
            raise
    
    def load_from_postgresql(self,
                            connection_string: str,
                            table: str,
                            query: Optional[str] = None) -> pd.DataFrame:
        """Load data from PostgreSQL (NeonDB)"""
        if not HAS_SQLALCHEMY:
            raise ImportError("sqlalchemy is not installed. Install it with: pip install sqlalchemy psycopg2-binary")
        
        try:
            engine = create_engine(connection_string)
            
            if query:
                sql_query = query
            else:
                sql_query = f"SELECT * FROM {table}"
            
            df = pd.read_sql(sql_query, engine)
            
            logger.info(f"Loaded data from PostgreSQL: {df.shape}")
            self.data = df
            return df
            
        except Exception as e:
            logger.error(f"Error loading from PostgreSQL: {str(e)}")
            raise
    
    def select_columns(self, X_columns: List[str], y_column: str) -> tuple:
        """Select X and y columns from data"""
        if self.data is None:
            raise ValueError("No data loaded. Load data first.")
        
        # Validate columns exist
        all_columns = list(self.data.columns)
        missing_x = [col for col in X_columns if col not in all_columns]
        if missing_x:
            raise ValueError(f"X columns not found: {missing_x}")
        
        if y_column not in all_columns:
            raise ValueError(f"Y column not found: {y_column}")
        
        # Select columns
        X = self.data[X_columns].copy()
        y = self.data[y_column].copy()
        
        logger.info(f"Selected {len(X_columns)} X columns and 1 y column")
        return X, y
    
    def get_data_info(self) -> Dict[str, Any]:
        """Get information about the loaded data"""
        if self.data is None:
            return {}
        
        info = {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'dtypes': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'memory_usage': self.data.memory_usage(deep=True).sum()
        }
        
        return info
        

