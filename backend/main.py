"""
FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.api.routes import router
from app.api.metrics import router as metrics_router
from app.core.config import Config
from app.core.logger import setup_logging

# Initialize config
config = Config()

# Setup logging
logger = setup_logging(config.config)

# Create FastAPI app
app = FastAPI(
    title=config.get('app.name', 'ML AutoML Suite'),
    version=config.get('app.version', '1.0.0'),
    description="Comprehensive Machine Learning Platform"
)

# CORS middleware
cors_origins = config.get('api.cors_origins', ['*'])
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api", tags=["ML Operations"])
app.include_router(metrics_router, prefix="/api", tags=["Monitoring"])


@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("Starting ML AutoML Suite API")
    # Create necessary directories
    Path("models").mkdir(exist_ok=True)
    Path("data").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("Shutting down ML AutoML Suite API")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ML AutoML Suite API",
        "version": config.get('app.version', '1.0.0'),
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    
    host = config.get('api.host', '0.0.0.0')
    port = config.get('api.port', 8000)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=config.get('app.debug', True)
    )
