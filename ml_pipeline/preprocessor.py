"""
Data Preprocessing Module
Handles missing values, scaling, encoding for both categorical and numerical data
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class Preprocessor:
    """Handles all data preprocessing tasks"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.preprocessor = None
        self.feature_names = None
        self.categorical_features = []
        self.numerical_features = []
        
    def identify_features(self, df: pd.DataFrame) -> Tuple[List[str], List[str]]:
        """Identify categorical and numerical features"""
        categorical = []
        numerical = []
        
        for col in df.columns:
            if df[col].dtype == 'object' or df[col].dtype == 'category':
                categorical.append(col)
            else:
                numerical.append(col)
        
        self.categorical_features = categorical
        self.numerical_features = numerical
        
        logger.info(f"Identified {len(categorical)} categorical and {len(numerical)} numerical features")
        return categorical, numerical
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = 'auto') -> pd.DataFrame:
        """Handle missing values in the dataset"""
        df_processed = df.copy()
        
        for col in df_processed.columns:
            if df_processed[col].isnull().sum() > 0:
                if df_processed[col].dtype in ['int64', 'float64']:
                    if strategy == 'auto' or strategy == 'mean':
                        df_processed[col].fillna(df_processed[col].mean(), inplace=True)
                    elif strategy == 'median':
                        df_processed[col].fillna(df_processed[col].median(), inplace=True)
                    elif strategy == 'mode':
                        df_processed[col].fillna(df_processed[col].mode()[0], inplace=True)
                else:
                    # For categorical, use mode
                    df_processed[col].fillna(df_processed[col].mode()[0] if len(df_processed[col].mode()) > 0 else 'unknown', inplace=True)
        
        logger.info("Missing values handled")
        return df_processed
    
    def create_preprocessing_pipeline(self, 
                                     categorical_features: List[str],
                                     numerical_features: List[str],
                                     scaling: bool = True,
                                     encoding: str = 'auto') -> ColumnTransformer:
        """Create preprocessing pipeline"""
        
        # Numerical preprocessing
        if scaling:
            numerical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler())
            ])
        else:
            numerical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='mean'))
            ])
        
        # Categorical preprocessing
        if encoding == 'auto' or encoding == 'onehot':
            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
            ])
        else:  # label encoding
            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('label', LabelEncoder())
            ])
        
        # Combine transformers
        transformers = []
        if numerical_features:
            transformers.append(('num', numerical_transformer, numerical_features))
        if categorical_features:
            transformers.append(('cat', categorical_transformer, categorical_features))
        
        if not transformers:
            raise ValueError("No features to transform")
        
        preprocessor = ColumnTransformer(
            transformers=transformers,
            remainder='passthrough'
        )
        
        self.preprocessor = preprocessor
        return preprocessor
    
    def fit_transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> np.ndarray:
        """Fit and transform the data"""
        if self.preprocessor is None:
            categorical, numerical = self.identify_features(X)
            self.create_preprocessing_pipeline(
                categorical,
                numerical,
                scaling=self.config.get('scaling', True),
                encoding=self.config.get('encoding', 'auto')
            )
        
        # Handle missing values first
        X_processed = self.handle_missing_values(
            X, 
            strategy=self.config.get('missing_value_strategy', 'auto')
        )
        
        # Fit and transform
        X_transformed = self.preprocessor.fit_transform(X_processed)
        
        # Get feature names
        try:
            if hasattr(self.preprocessor, 'get_feature_names_out'):
                self.feature_names = self.preprocessor.get_feature_names_out()
            else:
                self.feature_names = list(X_processed.columns)
        except:
            self.feature_names = list(X_processed.columns)
        
        logger.info(f"Data transformed: {X_transformed.shape}")
        return X_transformed
    
    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """Transform new data using fitted preprocessor"""
        if self.preprocessor is None:
            raise ValueError("Preprocessor must be fitted first")
        
        X_processed = self.handle_missing_values(
            X,
            strategy=self.config.get('missing_value_strategy', 'auto')
        )
        
        X_transformed = self.preprocessor.transform(X_processed)
        return X_transformed
