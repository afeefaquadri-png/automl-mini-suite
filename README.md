# ML AutoML Suite - Comprehensive Machine Learning Platform


A full-stack machine learning platform that automates the entire ML pipeline from data ingestion to model deployment.

## Features

- **Multi-Source Data Ingestion**: SQL, NoSQL (MongoDB), CSV, Excel
- **Intelligent Preprocessing**: Automatic handling of missing values, scaling, encoding
- **Auto Model Selection**: Automatically selects appropriate models based on problem type
- **Hyperparameter Tuning**: Grid search and random search for optimal parameters
- **Model Comparison**: Comprehensive comparison with visual reports
- **Model Persistence**: Save and reuse trained models
- **Real-time Predictions**: Fast inference API
- **Dual Frontend**: Streamlit (quick) and React/Next.js (production)

## Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: Streamlit, React/Next.js
- **Database**: MongoDB, NeonDB (PostgreSQL)
- **ML Libraries**: scikit-learn, pandas, numpy

## Project Structure

```
.
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core business logic
│   │   ├── models/         # Database models
│   │   └── utils/          # Utilities
│   ├── ml_pipeline/        # ML pipeline module
│   └── main.py            # FastAPI app entry
├── frontend_streamlit/     # Streamlit frontend
├── frontend_nextjs/        # Next.js frontend
├── config/                 # Configuration files
├── logs/                   # Log files
├── models/                 # Saved ML models
└── requirements.txt        # Python dependencies
```

## Quick Start - Web Access

### Easiest Way (One Click):
```bash
start_all.bat
```
This starts both backend and frontend, then opens your browser automatically!

### Manual Start:
1. **Install dependencies:**
   ```bash
   setup.bat
   ```

2. **Start backend:**
   ```bash
   start_backend.bat
   ```

3. **Start Streamlit frontend (in new terminal):**
   ```bash
   start_streamlit.bat
   ```

4. **Open browser:** `http://localhost:8501`

### Check Services:
```bash
check_services.bat
```

📖 **For detailed web access guide, see [WEB_ACCESS_GUIDE.md](WEB_ACCESS_GUIDE.md)**  
📖 **For installation details, see [INSTALLATION.md](INSTALLATION.md)**  
📖 **For quick examples, see [QUICK_START.md](QUICK_START.md)**

## Usage

1. Upload data or connect to database
2. Select X and Y columns
3. System automatically detects problem type
4. Preprocessing is applied automatically
5. Models are trained and compared
6. Best model is selected and saved
7. Use saved model for predictions

## API Endpoints

- `POST /api/data/upload` - Upload data file
- `POST /api/data/database` - Fetch from database
- `POST /api/train` - Train models
- `POST /api/predict` - Get predictions
- `GET /api/models` - List saved models
- `GET /api/models/{model_id}` - Get model details
- `GET /api/health` - Health check
- `GET /api/metrics` - Prometheus metrics

## Documentation

- [Installation Guide](INSTALLATION.md)
- [Quick Start Guide](QUICK_START.md)
- [Product Requirements](PRD.md)
- [Design Document](DESIGN.md)
- [Project Structure](PROJECT_STRUCTURE.md)

## Features in Detail

### Supported ML Models
- **Regression:** Linear Regression, SVR, Decision Tree
- **Classification:** Logistic Regression, SVC, Decision Tree

### Data Sources
- CSV, Excel, JSON files
- MongoDB (NoSQL)
- PostgreSQL/NeonDB (SQL)

### Preprocessing
- Automatic missing value imputation
- Feature scaling (StandardScaler)
- Encoding (OneHot, Label)
- Categorical/Numerical detection

### Model Training
- Automatic problem type detection
- Hyperparameter tuning (Grid Search)
- Cross-validation (5-fold)
- Model comparison and selection
