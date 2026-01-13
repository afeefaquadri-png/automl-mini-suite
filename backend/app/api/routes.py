"""
API Routes
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from ml_pipeline import DataProcessor, ModelTrainer
from app.core.exceptions import DataLoadError, ModelTrainingError, PredictionError, ModelNotFoundError
from app.utils.response import success_response, error_response
from app.core.config import Config

router = APIRouter()
config = Config()

# Global storage (in production, use database)
data_storage = {}
model_storage = {}
training_jobs = {}


@router.post("/data/upload")
async def upload_data(file: UploadFile = File(...)):
    """Upload data file"""
    try:
        # Save uploaded file
        file_path = f"data/{file.filename}"
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Load data
        processor = DataProcessor(config.get('ml', {}))
        df = processor.load_from_file(file_path)
        
        # Store processor
        job_id = f"job_{len(data_storage)}"
        data_storage[job_id] = {
            'processor': processor,
            'file_path': file_path,
            'data_info': processor.get_data_info()
        }
        
        return success_response({
            'job_id': job_id,
            'data_info': processor.get_data_info()
        }, "Data uploaded successfully")
        
    except Exception as e:
        return error_response(f"Error uploading data: {str(e)}")


@router.post("/data/database")
async def load_from_database(request: Dict[str, Any]):
    """Load data from database"""
    try:
        db_type = request.get('type')  # 'mongodb' or 'postgresql'
        processor = DataProcessor(config.get('ml', {}))
        
        if db_type == 'mongodb':
            df = processor.load_from_mongodb(
                connection_string=request.get('connection_string'),
                database=request.get('database'),
                collection=request.get('collection'),
                query=request.get('query')
            )
        elif db_type == 'postgresql':
            df = processor.load_from_postgresql(
                connection_string=request.get('connection_string'),
                table=request.get('table'),
                query=request.get('query')
            )
        else:
            return error_response("Invalid database type")
        
        job_id = f"job_{len(data_storage)}"
        data_storage[job_id] = {
            'processor': processor,
            'data_info': processor.get_data_info()
        }
        
        return success_response({
            'job_id': job_id,
            'data_info': processor.get_data_info()
        }, "Data loaded successfully")
        
    except Exception as e:
        return error_response(f"Error loading from database: {str(e)}")


@router.post("/train")
async def train_models(request: Dict[str, Any]):
    """Train models"""
    try:
        job_id = request.get('job_id')
        X_columns = request.get('X_columns', [])
        y_column = request.get('y_column')
        
        if job_id not in data_storage:
            return error_response("Job ID not found")
        
        processor = data_storage[job_id]['processor']
        
        # Select columns
        X, y = processor.select_columns(X_columns, y_column)
        
        # Train models
        trainer = ModelTrainer(config.get('ml', {}))
        results = trainer.train_models(X, y)
        
        # Save best model
        model_id = f"model_{len(model_storage)}"
        model_path = f"models/{model_id}.pkl"
        trainer.save_model(trainer.best_model_name, model_path)
        
        # Store trainer
        model_storage[model_id] = {
            'trainer': trainer,
            'model_path': model_path,
            'results': results,
            'best_model': trainer.best_model_name,
            'problem_type': trainer.problem_type
        }
        
        return success_response({
            'model_id': model_id,
            'best_model': trainer.best_model_name,
            'results': {
                name: {
                    'metrics': result['metrics'],
                    'cv_mean': result['cv_mean'],
                    'cv_std': result['cv_std']
                }
                for name, result in results.items()
            }
        }, "Models trained successfully")
        
    except Exception as e:
        return error_response(f"Error training models: {str(e)}")


@router.post("/predict")
async def predict(request: Dict[str, Any]):
    """Make predictions"""
    try:
        model_id = request.get('model_id')
        data = request.get('data')  # List of dicts or dict
        
        if model_id not in model_storage:
            return error_response("Model ID not found")
        
        trainer = model_storage[model_id]['trainer']
        
        # Convert data to DataFrame
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = pd.DataFrame(data)
        
        # Make predictions
        predictions = trainer.predict(df)
        
        return success_response({
            'predictions': predictions.tolist()
        }, "Predictions generated successfully")
        
    except Exception as e:
        return error_response(f"Error making predictions: {str(e)}")


@router.get("/models")
async def list_models():
    """List all saved models"""
    models = [
        {
            'model_id': model_id,
            'best_model': info['best_model'],
            'problem_type': info['problem_type'],
            'metrics': info['results'].get(info['best_model'], {}).get('metrics', {})
        }
        for model_id, info in model_storage.items()
    ]
    
    return success_response(models, "Models retrieved successfully")


@router.get("/models/{model_id}")
async def get_model(model_id: str):
    """Get model details"""
    if model_id not in model_storage:
        return error_response("Model not found")
    
    info = model_storage[model_id]
    return success_response({
        'model_id': model_id,
        'best_model': info['best_model'],
        'problem_type': info['problem_type'],
        'all_results': {
            name: {
                'metrics': result['metrics'],
                'cv_mean': result['cv_mean'],
                'cv_std': result['cv_std']
            }
            for name, result in info['results'].items()
        }
    }, "Model details retrieved successfully")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return success_response({"status": "healthy"}, "Service is running")
