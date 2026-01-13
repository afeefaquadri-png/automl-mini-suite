"""
Custom Exceptions
"""


class MLSuiteException(Exception):
    """Base exception for ML Suite"""
    pass


class DataLoadError(MLSuiteException):
    """Error loading data"""
    pass


class ModelTrainingError(MLSuiteException):
    """Error during model training"""
    pass


class PredictionError(MLSuiteException):
    """Error during prediction"""
    pass


class ModelNotFoundError(MLSuiteException):
    """Model not found"""
    pass
