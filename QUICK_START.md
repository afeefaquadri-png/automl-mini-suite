# Quick Start Guide
## ML AutoML Suite

### 🚀 Get Started in 5 Minutes

#### Step 1: Install Dependencies
```bash
# Run setup script
setup.bat

# Or manually
pip install -r requirements.txt
cd frontend_streamlit && pip install -r requirements.txt && cd ..
```

#### Step 2: Start Backend
```bash
start_backend.bat
```
Backend runs at: `http://localhost:8000`

#### Step 3: Start Streamlit (Easiest)
```bash
start_streamlit.bat
```
Open: `http://localhost:8501`

#### Step 4: Test with Sample Data

1. **Upload Data:**
   - Go to "Data Upload" tab
   - Click "Choose a file"
   - Select `Exam_Score_Prediction.csv`
   - Click "Upload"

2. **Train Models:**
   - Go to "Model Training" tab
   - Select X columns (all except `exam_score`)
   - Select Y column (`exam_score`)
   - Click "Train Models"
   - Wait for training (1-2 minutes)

3. **View Results:**
   - See model comparison table
   - Best model is highlighted
   - Check metrics (R², RMSE, MAE)

4. **Make Predictions:**
   - Go to "Predictions" tab
   - Upload a CSV with same features
   - Get predictions instantly!

### 📊 Using Next.js Frontend (Optional)

```bash
cd frontend_nextjs
npm install
npm run dev
```
Open: `http://localhost:3000`

### 🔌 API Usage

#### Upload Data
```bash
curl -X POST "http://localhost:8000/api/data/upload" \
  -F "file=@Exam_Score_Prediction.csv"
```

#### Train Models
```bash
curl -X POST "http://localhost:8000/api/train" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "job_0",
    "X_columns": ["age", "study_hours", "class_attendance"],
    "y_column": "exam_score"
  }'
```

#### Make Predictions
```bash
curl -X POST "http://localhost:8000/api/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "model_0",
    "data": [{"age": 20, "study_hours": 5.0, "class_attendance": 80}]
  }'
```

### 📖 Full Documentation

- **Installation:** See `INSTALLATION.md`
- **API Docs:** `http://localhost:8000/docs`
- **PRD:** See `PRD.md`
- **Design:** See `DESIGN.md`

### 🎯 Key Features

✅ **6 ML Models:** Linear Regression, Logistic Regression, SVM, SVR, SVC, Decision Tree  
✅ **Auto Preprocessing:** Missing values, scaling, encoding  
✅ **Hyperparameter Tuning:** Grid search with cross-validation  
✅ **Model Comparison:** Side-by-side metrics  
✅ **Multiple Data Sources:** Files, MongoDB, PostgreSQL  
✅ **Dual Frontend:** Streamlit (quick) + Next.js (production)  
✅ **Model Persistence:** Save and reuse models  
✅ **Visual Reports:** Charts and HTML reports  

### 🐛 Troubleshooting

**Backend won't start:**
- Check if port 8000 is available
- Verify Python dependencies installed

**Streamlit won't connect:**
- Ensure backend is running
- Check API URL in sidebar (default: http://localhost:8000)

**Training fails:**
- Check data format
- Ensure X and Y columns are valid
- Check logs in `logs/app.log`

### 💡 Tips

1. **Start Small:** Test with small datasets first
2. **Check Data:** Review data info before training
3. **Save Models:** Model IDs are returned after training
4. **Use API:** For automation and integrations
5. **Monitor Logs:** Check `logs/app.log` for details

### 🎓 Example Workflow

```
1. Upload CSV → Get job_id
2. Select columns → Train models → Get model_id
3. Upload new data → Get predictions
4. Compare models → Select best one
5. Save model → Use for future predictions
```

Happy ML Modeling! 🚀
