# Web Access Guide - ML AutoML Suite
## How to Access and Use the ML Suite Through Web Browser

### 🚀 Quick Start (3 Steps)

#### Step 1: Start the Backend API
Open a **Command Prompt** or **PowerShell** window and run:
```bash
start_backend.bat
```

Or manually:
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Wait for:** You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

✅ **Backend is running at:** `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

---

#### Step 2: Start the Web Frontend

**Option A: Streamlit (Easiest - Recommended)**
Open a **NEW** Command Prompt/PowerShell window and run:
```bash
start_streamlit.bat
```

Or manually:
```bash
cd frontend_streamlit
streamlit run app.py --server.port 8501
```

**Wait for:** You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

✅ **Web Interface:** `http://localhost:8501`

**Option B: Next.js (Production-Ready)**
```bash
cd frontend_nextjs
npm install  # First time only
npm run dev
```

✅ **Web Interface:** `http://localhost:3000`

---

#### Step 3: Open in Browser
Open your web browser and go to:
- **Streamlit:** http://localhost:8501
- **Next.js:** http://localhost:3000

---

## 📋 Complete Workflow

### 1. Upload Your Data

**In the Web Interface:**

1. **Navigate to "Data Upload" tab/page**
2. **Choose upload method:**
   - **File Upload:** Click "Choose a file" and select your CSV/Excel file
   - **MongoDB:** Enter connection details
   - **PostgreSQL:** Enter connection details
3. **Click "Upload" or "Load"**
4. **Wait for confirmation** - You'll see data information (rows, columns, types)

**Example:** Upload `Exam_Score_Prediction.csv`

---

### 2. Train Models

1. **Navigate to "Model Training" tab/page**
2. **Select Columns:**
   - **X Columns (Features):** Select multiple columns (checkboxes)
     - Example: `age`, `study_hours`, `class_attendance`, etc.
   - **Y Column (Target):** Select one column (dropdown)
     - Example: `exam_score`
3. **Click "Train Models"**
4. **Wait for training** (1-5 minutes depending on data size)
5. **View Results:**
   - See all model performances
   - Best model is highlighted
   - Metrics displayed (R², RMSE, MAE for regression OR Accuracy, Precision, Recall for classification)

---

### 3. Compare Models

1. **Navigate to "Model Comparison" tab/page**
2. **Select models** to compare (checkboxes)
3. **Click "Compare Models"**
4. **View comparison charts** showing metrics side-by-side

---

### 4. Make Predictions

1. **Navigate to "Predictions" tab/page**
2. **Upload new data file** (CSV with same feature columns)
3. **Click "Make Predictions"**
4. **View predictions** in a table
5. **Download results** as CSV

---

### 5. View Reports

1. **Navigate to "Reports" tab/page**
2. **Select a model** from dropdown
3. **View detailed report:**
   - All metrics
   - Model parameters
   - Cross-validation scores

---

## 🖥️ Using Streamlit Interface

### Interface Layout:
```
┌─────────────────────────────────────────┐
│  Sidebar          │  Main Content       │
│  - Navigation     │  - Current Page     │
│  - API URL        │  - Forms            │
│                   │  - Results          │
└─────────────────────────────────────────┘
```

### Navigation:
- **Sidebar:** Click on page names to navigate
- **API URL:** Default is `http://localhost:8000` (change if needed)

### Pages:
1. **Data Upload** - Upload or connect to data
2. **Model Training** - Train ML models
3. **Predictions** - Make predictions with trained models
4. **Model Comparison** - Compare multiple models
5. **Reports** - View detailed model reports

---

## 🌐 Using Next.js Interface

### Interface Layout:
```
┌─────────────────────────────────────────┐
│  Header: ML AutoML Suite                │
├─────────────────────────────────────────┤
│  [Upload] [Training] [Predict] [Compare]│
├─────────────────────────────────────────┤
│  Main Content Area                      │
│  - Forms                                │
│  - Results                              │
└─────────────────────────────────────────┘
```

### Navigation:
- **Tabs:** Click tabs at the top to switch pages
- **Responsive:** Works on desktop, tablet, and mobile

---

## 🔧 Troubleshooting

### Backend Won't Start

**Error:** `ModuleNotFoundError` or `ImportError`
```bash
# Install dependencies
pip install -r requirements.txt
```

**Error:** `Port 8000 already in use`
```bash
# Option 1: Stop the process using port 8000
# Option 2: Change port in backend/main.py or config/config.yaml
```

**Error:** `Cannot find module 'ml_pipeline'`
```bash
# Make sure you're in the project root
cd "C:\AI ML COURSE\ai ml project cursor"
# Then start backend
cd backend
python -m uvicorn main:app --reload
```

---

### Frontend Won't Connect

**Error:** `Connection refused` or `Failed to fetch`

1. **Check backend is running:**
   - Open: http://localhost:8000/api/health
   - Should return: `{"success": true, "message": "Service is running"}`

2. **Check API URL in frontend:**
   - Streamlit: Check sidebar "API URL" field
   - Next.js: Check `.env` file or `next.config.js`

3. **Check CORS settings:**
   - Backend allows all origins by default
   - If issues, check `config/config.yaml`

---

### Streamlit Won't Start

**Error:** `ModuleNotFoundError: No module named 'streamlit'`
```bash
cd frontend_streamlit
pip install -r requirements.txt
```

**Error:** `Port 8501 already in use`
```bash
# Use different port
streamlit run app.py --server.port 8502
```

---

### Next.js Won't Start

**Error:** `npm: command not found`
- Install Node.js from https://nodejs.org/

**Error:** `Module not found`
```bash
cd frontend_nextjs
npm install
```

---

## 📱 Accessing from Other Devices

### On Same Network:

1. **Find your computer's IP address:**
   ```bash
   ipconfig  # Windows
   # Look for IPv4 Address (e.g., 192.168.1.100)
   ```

2. **Update backend to allow external access:**
   - Backend already runs on `0.0.0.0` (all interfaces)
   - Or change in `backend/main.py`:
     ```python
     uvicorn.run("main:app", host="0.0.0.0", port=8000)
     ```

3. **Update Streamlit:**
   ```bash
   streamlit run app.py --server.address 0.0.0.0 --server.port 8501
   ```

4. **Access from other device:**
   - Streamlit: `http://YOUR_IP:8501`
   - API: `http://YOUR_IP:8000`
   - Update API URL in Streamlit sidebar to match

---

## 🎯 Example: Complete Workflow

### Scenario: Predict Exam Scores

1. **Start Services:**
   ```bash
   # Terminal 1
   start_backend.bat
   
   # Terminal 2
   start_streamlit.bat
   ```

2. **Open Browser:** http://localhost:8501

3. **Upload Data:**
   - Go to "Data Upload"
   - Upload `Exam_Score_Prediction.csv`
   - See: 20000 rows, 13 columns

4. **Train Models:**
   - Go to "Model Training"
   - Select X: `age`, `study_hours`, `class_attendance`, `sleep_hours`, etc.
   - Select Y: `exam_score`
   - Click "Train Models"
   - Wait 2-3 minutes
   - See results: Best model is "linear_regression" with R² = 0.85

5. **Make Predictions:**
   - Go to "Predictions"
   - Upload new CSV with same columns
   - Get predictions instantly!

---

## 🔗 URLs Reference

| Service | URL | Description |
|---------|-----|-------------|
| Streamlit | http://localhost:8501 | Main web interface |
| Next.js | http://localhost:3000 | Alternative interface |
| API | http://localhost:8000 | Backend API |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Health | http://localhost:8000/api/health | Health check |
| Metrics | http://localhost:8000/api/metrics | Prometheus metrics |

---

## 💡 Tips

1. **Keep both terminals open** - Backend and Frontend need to run simultaneously
2. **Check backend first** - If frontend doesn't work, verify backend is running
3. **Use API docs** - Visit http://localhost:8000/docs to test API directly
4. **Check logs** - Backend logs in `logs/app.log`
5. **Save model IDs** - After training, note the model_id for future predictions

---

## 🎓 Next Steps

- Read [QUICK_START.md](QUICK_START.md) for quick examples
- Read [INSTALLATION.md](INSTALLATION.md) for detailed setup
- Check [README.md](README.md) for overview

Happy ML Modeling! 🚀
