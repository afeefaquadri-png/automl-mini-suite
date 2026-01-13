# Installation Guide
## ML AutoML Suite

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher (for Next.js frontend)
- MongoDB (optional, for MongoDB data source)
- PostgreSQL (optional, for NeonDB/PostgreSQL data source)

### Step 1: Clone/Download Project

Navigate to the project directory:
```bash
cd "C:\AI ML COURSE\ai ml project cursor"
```

### Step 2: Install Python Dependencies

```bash
# Install main dependencies
pip install -r requirements.txt

# Install Streamlit dependencies
cd frontend_streamlit
pip install -r requirements.txt
cd ..
```

### Step 3: Create Required Directories

```bash
mkdir models
mkdir data
mkdir logs
mkdir reports
```

Or use the setup script:
```bash
# Windows
setup.bat

# Linux/Mac
chmod +x setup.sh
./setup.sh
```

### Step 4: Configure Environment

Create a `.env` file in the root directory (optional):
```env
MONGODB_URI=mongodb://localhost:27017
POSTGRES_URI=postgresql://user:password@localhost:5432/dbname
API_BASE_URL=http://localhost:8000
```

Or edit `config/config.yaml` directly.

### Step 5: Start Backend API

```bash
# Windows
start_backend.bat

# Or manually
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### Step 6: Start Streamlit Frontend

```bash
# Windows
start_streamlit.bat

# Or manually
cd frontend_streamlit
streamlit run app.py --server.port 8501
```

The Streamlit app will be available at: `http://localhost:8501`

### Step 7: Start Next.js Frontend (Optional)

```bash
cd frontend_nextjs
npm install
npm run dev
```

The Next.js app will be available at: `http://localhost:3000`

### Step 8: Verify Installation

1. Open `http://localhost:8000/docs` - Should see FastAPI documentation
2. Open `http://localhost:8501` - Should see Streamlit interface
3. Test API health: `http://localhost:8000/api/health`

### Troubleshooting

#### Port Already in Use
- Change ports in configuration files
- Or stop the process using the port

#### Module Not Found
- Ensure you're in the correct directory
- Check Python path
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

#### Database Connection Issues
- Verify database is running
- Check connection strings
- Ensure network access

#### Frontend Not Connecting to API
- Check API_BASE_URL in frontend config
- Verify CORS settings in backend
- Check API is running

### Development Setup

For development, use:
```bash
# Backend with auto-reload
cd backend
uvicorn main:app --reload

# Streamlit with auto-reload (default)
streamlit run app.py

# Next.js with hot reload (default)
npm run dev
```

### Production Deployment

See `DEPLOYMENT.md` for production deployment instructions.

### Quick Start Test

1. Start backend: `start_backend.bat`
2. Start Streamlit: `start_streamlit.bat`
3. Upload `Exam_Score_Prediction.csv`
4. Select columns (all except `exam_score` as X, `exam_score` as Y)
5. Click "Train Models"
6. View results!
