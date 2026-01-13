# Project Structure
## ML AutoML Suite

```
.
├── README.md                      # Main documentation
├── PRD.md                         # Product Requirements Document
├── DESIGN.md                      # UX/UI Design Document
├── INSTALLATION.md                # Installation guide
├── QUICK_START.md                 # Quick start guide
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
│
├── config/                        # Configuration files
│   └── config.yaml               # Main configuration
│
├── ml_pipeline/                   # ML Pipeline Module
│   ├── __init__.py
│   ├── data_processor.py         # Data loading from various sources
│   ├── preprocessor.py           # Data preprocessing
│   ├── model_selector.py         # Model selection logic
│   ├── model_trainer.py          # Model training and evaluation
│   └── visualization.py           # Charts and reports
│
├── backend/                       # FastAPI Backend
│   ├── main.py                   # FastAPI app entry point
│   └── app/
│       ├── __init__.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── routes.py         # Main API routes
│       │   └── metrics.py        # Prometheus metrics
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py         # Configuration management
│       │   ├── logger.py         # Logging setup
│       │   └── exceptions.py     # Custom exceptions
│       └── utils/
│           ├── __init__.py
│           ├── response.py       # API response utilities
│           └── monitoring.py     # Monitoring utilities
│
├── frontend_streamlit/            # Streamlit Frontend
│   ├── app.py                    # Main Streamlit app
│   └── requirements.txt         # Streamlit dependencies
│
├── frontend_nextjs/               # Next.js Frontend
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── app/
│       ├── layout.tsx            # Root layout
│       ├── page.tsx              # Main page
│       ├── globals.css           # Global styles
│       └── components/
│           ├── DataUpload.tsx
│           ├── ModelTraining.tsx
│           ├── Predictions.tsx
│           ├── ModelComparison.tsx
│           └── Reports.tsx
│
├── models/                        # Saved ML models (generated)
├── data/                          # Uploaded data files (generated)
├── logs/                          # Log files (generated)
├── reports/                       # Generated reports (generated)
│
└── Scripts/                       # Startup scripts
    ├── setup.bat                 # Setup script
    ├── start_backend.bat         # Start backend
    └── start_streamlit.bat       # Start Streamlit
```

## Key Components

### ML Pipeline (`ml_pipeline/`)
- **DataProcessor:** Handles data loading from files, MongoDB, PostgreSQL
- **Preprocessor:** Automatic preprocessing (missing values, scaling, encoding)
- **ModelSelector:** Detects problem type and selects appropriate models
- **ModelTrainer:** Trains models, hyperparameter tuning, evaluation
- **Visualization:** Creates charts and reports

### Backend (`backend/`)
- **FastAPI:** RESTful API for all operations
- **Routes:** Data upload, training, predictions, model management
- **Config:** YAML-based configuration with env overrides
- **Logging:** Structured logging with Loguru
- **Monitoring:** Prometheus metrics endpoint

### Frontends
- **Streamlit:** Quick prototyping, Python-based
- **Next.js:** Production-ready React application with TypeScript

## Data Flow

```
User Input → Frontend → FastAPI → ML Pipeline → Model Storage
                ↓
         Database/File
                ↓
         Preprocessing → Training → Evaluation → Comparison
                ↓
         Best Model → Persistence → Predictions
```

## Configuration

- **config/config.yaml:** Main configuration file
- **Environment Variables:** Override config values
- **API Settings:** Host, port, CORS origins
- **ML Settings:** Models, hyperparameters, preprocessing

## Storage

- **models/:** Saved model files (.pkl)
- **data/:** Uploaded data files
- **logs/:** Application logs
- **reports/:** Generated HTML reports and charts

## API Endpoints

- `POST /api/data/upload` - Upload data file
- `POST /api/data/database` - Load from database
- `POST /api/train` - Train models
- `POST /api/predict` - Make predictions
- `GET /api/models` - List all models
- `GET /api/models/{id}` - Get model details
- `GET /api/health` - Health check
- `GET /api/metrics` - Prometheus metrics
