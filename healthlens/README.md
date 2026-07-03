# HealthLens - AI Health Prediction & RAG Advisory System

HealthLens is a comprehensive, AI-powered healthcare platform that predicts disease risks (Heart Disease, Diabetes, Hypertension) and provides personalized lifestyle advice via an integrated FAISS + HuggingFace FLAN-T5 RAG system. It also integrates manual health tracking and smartwatch data forms (Google Fit mock integrations).

## Project Structure
- `backend/` - FastAPI application connecting machine learning inferences, MongoDB tracking, and the RAG advisor logic.
- `frontend/` - React + TailwindCSS + Vite dashboard for health monitoring, graphs, and chat UI.
- `ml/` - Sklearn/XGBoost pipelines utilizing SMOTE and GridSearch to output serialized artifacts model weights.
- `rag/` - FAISS retrieval and generative pipelines utilizing `sentence-transformers` for embedding generation.
- `data/` - Target repository for incoming batch CSV files.

---

## 🛠 Setup Instructions

### 1. Database (MongoDB)
Add a `.env` file in `healthlens/backend/` and populate:
```
MONGO_URI=mongodb+srv://healthlens:<your_password>@cluster0...
GOOGLE_CLIENT_ID=your_provided_client_id
GOOGLE_REDIRECT_URI=http://localhost:5000/api/auth/callback
```

### 2. Generate ML Models
```bash
cd healthlens/ml
pip install -r ../backend/requirements.txt
pip install imbalanced-learn
python train_models.py
```
*(This places the `.pkl` models required by FastAPI into `healthlens/backend/app/models/`)*

### 3. Start Backend
```bash
cd healthlens/backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be available at: `http://localhost:8000/docs`

### 4. Start Frontend
```bash
cd healthlens/frontend
npm install
npm run dev
```

---

## ⚡ Sample API Requests

### 1. Predict All Health Risks (POST)
**Endpoint:** `http://localhost:8000/api/predict/all`  
```json
{
  "age": 45,
  "bmi": 28.5,
  "heart_rate": 78,
  "glucose": 110.0,
  "steps": 4000,
  "sleep_hours": 6.0,
  "gender": "male",
  "blood_pressure": "130/85"
}
```
**Expected Response:**
```json
{
  "heart_risk": 64.2,
  "diabetes_risk": 55.1,
  "hypertension_risk": 71.8,
  "risk_level": {
    "heart": "Medium",
    "diabetes": "Medium",
    "hypertension": "High"
  }
}
```

### 2. Connect Smartwatch (Google Fit Proxy) (GET)
**Endpoint:** `http://localhost:8000/api/user/health-data`
**Expected Response:**
```json
{
  "heart_rate": 72,
  "steps": 6500,
  "calories": 2100,
  "sleep_hours": 7.5
}
```

### 3. RAG Health Advisor Chatbot (POST)
**Endpoint:** `http://localhost:8000/api/chat`
```json
{
  "query": "How to lower my high blood pressure and hypertension risk?"
}
```
**Expected Response:**
```json
{
  "response": "Hypertension (high blood pressure) can be controlled by a low-salt diet like the DASH diet, reducing daily stress, and avoiding excessive alcohol consumption.",
  "query": "How to lower my high blood pressure and hypertension risk?"
}
```

---

## Deployment (Production Guide)
- **Frontend**: Connect the `healthlens/frontend` folder to **Vercel** or **Netlify**. Ensure environment variables for the API URLs are updated to the backend host.
- **Backend/RAG/ML**: Deploy `healthlens/backend` via Docker on **Render**, **AWS ECS**, or **Google Cloud Run**. Ensure the saved models inside `/app/models` are bundled into the container deployment.
