"""
Model Selection Module
Automatically selects appropriate models based on problem type
"""

from typing import Dict, List, Any
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR, SVC
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
import logging

logger = logging.getLogger(__name__)


class ModelSelector:
    """Selects appropriate models based on problem type"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.regression_models = {
            'linear_regression': LinearRegression,
            'svr': SVR,
            'decision_tree': DecisionTreeRegressor
        }
        self.classification_models = {
            'logistic_regression': LogisticRegression,
            'svc': SVC,
            'decision_tree': DecisionTreeClassifier
        }
    
    def detect_problem_type(self, y: Any) -> str:
        """Detect if problem is regression or classification"""
        import pandas as pd
        import numpy as np
        
        if isinstance(y, pd.Series):
            y_values = y.values
        else:
            y_values = y
        
        # Check if target is continuous or discrete
        unique_values = len(np.unique(y_values))
        total_values = len(y_values)
        
        # If unique values are less than 20% of total, likely classification
        if unique_values < total_values * 0.2 and unique_values <= 20:
            return 'classification'
        else:
            # Check data type
            if pd.api.types.is_numeric_dtype(y_values):
                return 'regression'
            else:
                return 'classification'
    
    def get_models(self, problem_type: str) -> Dict[str, Any]:
        """Get models for the problem type"""
        if problem_type == 'regression':
            models = self.regression_models
        else:
            models = self.classification_models
        
        # Filter based on config
        if 'models' in self.config and problem_type in self.config['models']:
            allowed_models = self.config['models'][problem_type]
            models = {k: v for k, v in models.items() if k in allowed_models}
        
        logger.info(f"Selected {len(models)} models for {problem_type}")
        return models
    
    def get_hyperparameter_grids(self, problem_type: str) -> Dict[str, Dict]:
        """Get hyperparameter grids for each model"""
        
        if problem_type == 'regression':
            grids = {
                'linear_regression': {
                    'fit_intercept': [True, False],
                    'normalize': [False]
                },
                'svr': {
                    'C': [0.1, 1, 10, 100],
                    'gamma': ['scale', 'auto', 0.001, 0.01, 0.1],
                    'kernel': ['rbf', 'linear', 'poly']
                },
                'decision_tree': {
                    'max_depth': [3, 5, 7, 10, None],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                }
            }
        else:  # classification
            grids = {
                'logistic_regression': {
                    'C': [0.1, 1, 10, 100],
                    'penalty': ['l1', 'l2'],
                    'solver': ['liblinear', 'lbfgs']
                },
                'svc': {
                    'C': [0.1, 1, 10, 100],
                    'gamma': ['scale', 'auto', 0.001, 0.01, 0.1],
                    'kernel': ['rbf', 'linear', 'poly']
                },
                'decision_tree': {
                    'max_depth': [3, 5, 7, 10, None],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4],
                    'criterion': ['gini', 'entropy']
                }
            }
        
        return grids
