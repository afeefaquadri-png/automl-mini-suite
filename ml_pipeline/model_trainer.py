"""
Model Training Module
Handles model training, hyperparameter tuning, and evaluation
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_val_score, train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    r2_score, mean_squared_error, mean_absolute_error
)
from typing import Dict, List, Any, Tuple
import joblib
import logging
from pathlib import Path

from .model_selector import ModelSelector
from .preprocessor import Preprocessor

logger = logging.getLogger(__name__)


class ModelTrainer:
    """Trains and evaluates multiple models"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.model_selector = ModelSelector(self.config)
        self.preprocessor = Preprocessor(self.config.get('preprocessing', {}) if self.config else {})
        self.trained_models = {}
        self.model_results = {}
        self.best_model = None
        self.best_model_name = None
        self.problem_type = None
        
    def prepare_data(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2):
        """Prepare and preprocess data"""
        # Detect problem type
        self.problem_type = self.model_selector.detect_problem_type(y)
        logger.info(f"Detected problem type: {self.problem_type}")
        
        # Preprocess X
        X_processed = self.preprocessor.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y, test_size=test_size, random_state=42
        )
        
        return X_train, X_test, y_train, y_test
    
    def train_models(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        """Train all selected models"""
        # Prepare data
        X_train, X_test, y_train, y_test = self.prepare_data(X, y)
        
        # Get models and grids
        models = self.model_selector.get_models(self.problem_type)
        grids = self.model_selector.get_hyperparameter_grids(self.problem_type)
        
        # Training config
        cv_folds = self.config.get('hyperparameter_tuning', {}).get('cv_folds', 5)
        scoring = self.config.get('hyperparameter_tuning', {}).get('scoring', {}).get(
            self.problem_type, 'r2' if self.problem_type == 'regression' else 'accuracy'
        )
        tuning_method = self.config.get('hyperparameter_tuning', {}).get('method', 'grid_search')
        
        results = {}
        
        for model_name, model_class in models.items():
            logger.info(f"Training {model_name}...")
            
            try:
                # Get hyperparameter grid
                param_grid = grids.get(model_name, {})
                
                # Create base model
                base_model = model_class()
                
                # Hyperparameter tuning
                if param_grid and tuning_method == 'grid_search':
                    search = GridSearchCV(
                        base_model,
                        param_grid,
                        cv=cv_folds,
                        scoring=scoring,
                        n_jobs=-1,
                        verbose=0
                    )
                elif param_grid and tuning_method == 'random_search':
                    search = RandomizedSearchCV(
                        base_model,
                        param_grid,
                        cv=cv_folds,
                        scoring=scoring,
                        n_jobs=-1,
                        verbose=0,
                        n_iter=20
                    )
                else:
                    search = base_model
                
                # Train
                search.fit(X_train, y_train)
                
                # Get best model
                if hasattr(search, 'best_estimator_'):
                    best_model = search.best_estimator_
                    best_params = search.best_params_
                else:
                    best_model = search
                    best_params = {}
                
                # Evaluate
                train_pred = best_model.predict(X_train)
                test_pred = best_model.predict(X_test)
                
                metrics = self._calculate_metrics(y_train, train_pred, y_test, test_pred)
                
                # Cross-validation score
                cv_scores = cross_val_score(best_model, X_train, y_train, cv=cv_folds, scoring=scoring)
                
                results[model_name] = {
                    'model': best_model,
                    'params': best_params,
                    'metrics': metrics,
                    'cv_mean': cv_scores.mean(),
                    'cv_std': cv_scores.std(),
                    'train_predictions': train_pred,
                    'test_predictions': test_pred
                }
                
                self.trained_models[model_name] = best_model
                
                logger.info(f"{model_name} - CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
                
            except Exception as e:
                logger.error(f"Error training {model_name}: {str(e)}")
                continue
        
        self.model_results = results
        self._select_best_model()
        
        return results
    
    def _calculate_metrics(self, y_train, train_pred, y_test, test_pred) -> Dict[str, float]:
        """Calculate evaluation metrics"""
        metrics = {}
        
        if self.problem_type == 'regression':
            metrics['train_r2'] = r2_score(y_train, train_pred)
            metrics['test_r2'] = r2_score(y_test, test_pred)
            metrics['train_rmse'] = np.sqrt(mean_squared_error(y_train, train_pred))
            metrics['test_rmse'] = np.sqrt(mean_squared_error(y_test, test_pred))
            metrics['train_mae'] = mean_absolute_error(y_train, train_pred)
            metrics['test_mae'] = mean_absolute_error(y_test, test_pred)
        else:  # classification
            metrics['train_accuracy'] = accuracy_score(y_train, train_pred)
            metrics['test_accuracy'] = accuracy_score(y_test, test_pred)
            metrics['train_precision'] = precision_score(y_train, train_pred, average='weighted', zero_division=0)
            metrics['test_precision'] = precision_score(y_test, test_pred, average='weighted', zero_division=0)
            metrics['train_recall'] = recall_score(y_train, train_pred, average='weighted', zero_division=0)
            metrics['test_recall'] = recall_score(y_test, test_pred, average='weighted', zero_division=0)
            metrics['train_f1'] = f1_score(y_train, train_pred, average='weighted', zero_division=0)
            metrics['test_f1'] = f1_score(y_test, test_pred, average='weighted', zero_division=0)
        
        return metrics
    
    def _select_best_model(self):
        """Select the best model based on CV score"""
        if not self.model_results:
            return
        
        # Select based on CV mean score
        best_score = float('-inf')
        best_name = None
        
        for name, result in self.model_results.items():
            score = result['cv_mean']
            if score > best_score:
                best_score = score
                best_name = name
        
        self.best_model_name = best_name
        self.best_model = self.trained_models[best_name]
        
        logger.info(f"Best model: {best_name} with CV score: {best_score:.4f}")
    
    def save_model(self, model_name: str, filepath: str):
        """Save a trained model"""
        if model_name not in self.trained_models:
            raise ValueError(f"Model {model_name} not found")
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Save model and preprocessor together
        model_data = {
            'model': self.trained_models[model_name],
            'preprocessor': self.preprocessor,
            'problem_type': self.problem_type,
            'model_name': model_name,
            'metrics': self.model_results[model_name]['metrics']
        }
        
        joblib.dump(model_data, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load a saved model"""
        model_data = joblib.load(filepath)
        self.best_model = model_data['model']
        self.preprocessor = model_data['preprocessor']
        self.problem_type = model_data['problem_type']
        return model_data
    
    def predict(self, X: pd.DataFrame, model_name: str = None) -> np.ndarray:
        """Make predictions using a trained model"""
        if model_name:
            if model_name not in self.trained_models:
                raise ValueError(f"Model {model_name} not found")
            model = self.trained_models[model_name]
        else:
            if self.best_model is None:
                raise ValueError("No model available for prediction")
            model = self.best_model
        
        # Preprocess
        X_processed = self.preprocessor.transform(X)
        
        # Predict
        predictions = model.predict(X_processed)
        return predictions
