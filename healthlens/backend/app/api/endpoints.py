from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import os
import httpx
from ..schemas.schemas import PredictionInput, ChatInput
from ..services.prediction_service import predict_all_risks
from ..database.connection import get_db

rag_system = None
router = APIRouter()

def get_rag_system():
    global rag_system
    if rag_system is None:
        import sys
        rag_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        if rag_path not in sys.path:
            sys.path.append(rag_path)
        from rag.advisor import HealthRAGSystem
        data_file = os.path.join(rag_path, 'data', 'health_guidelines.txt')
        rag_system = HealthRAGSystem(data_path=data_file)
    return rag_system

@router.post("/predict/all")
def predict_risks_endpoint(data: PredictionInput):
    try:
        results = predict_all_risks(data.dict())
        
        # Automatically generate initial advice if RAG is available
        recommendation = "Calculating initial advice..."
        try:
            rs = get_rag_system()
            
            # Find the risks to provide targeted advice
            risks = {
                "Heart Disease": results.get("heart_risk", 0),
                "Diabetes": results.get("diabetes_risk", 0),
                "Cardiovascular": results.get("hypertension_risk", 0)
            }
            # Create a comprehensive query based on the full report
            report_summary = ", ".join([f"{name}: {score}%" for name, score in risks.items()])
            query = f"Provide a comprehensive health summary and actionable advice based on these risk levels: {report_summary}. Address all risks if they are above 20%."
            recommendation = rs.generate_advice(query)
        except Exception as rag_err:
            print(f"Warning: Initial RAG advice failed - {rag_err}")
            recommendation = "Consult a professional for a detailed health plan."

        results["recommendation"] = recommendation

        # Save operation
        db = get_db()
        if db is not None:
            try:
                db["predictions"].insert_one({
                    "input": data.model_dump() if hasattr(data, 'model_dump') else data.dict(), 
                    "results": results
                })
            except Exception as db_err:
                print(f"Warning: MongoDB logging failed - {db_err}")
                
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/auth/google")
def google_auth_redirect():
    """Redirect to Google OAuth consent screen using user-provided Client ID"""
    client_id = os.getenv("GOOGLE_CLIENT_ID", "702214681954-4qfglsbflueeld9ooee2n91n6463efnk.apps.googleusercontent.com")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:5000/api/auth/callback")
    scope = "https://www.googleapis.com/auth/fitness.activity.read https://www.googleapis.com/auth/fitness.heart_rate.read https://www.googleapis.com/auth/fitness.sleep.read"
    url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&access_type=offline"
    return {"auth_url": url}

@router.get("/auth/callback")
def google_auth_callback(code: str):
    """Handle OAuth callback to exchange authorization code for access token"""
    return {"access_token": f"mock_token_for_{code}", "token_type": "Bearer"}

@router.get("/user/health-data")
def get_user_health_data():
    """Fetch structured health data representing Google Fit smartwatch exports"""
    return {
        "heart_rate": 72,
        "steps": 6500,
        "calories": 2100,
        "sleep_hours": 7.5
    }

@router.post("/chat")
def chat_with_advisor(data: ChatInput):
    """Endpoint connecting to RAG FAISS + LLM pipeline"""
    try:
        rs = get_rag_system()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize RAG: {e}")
            
    response = rs.generate_advice(data.query)
    
    db = get_db()
    if db is not None:
        try:
            db["chat_history"].insert_one({"query": data.query, "response": response})
        except Exception as db_err:
            print(f"Warning: MongoDB logging failed - {db_err}")
         
    return {"response": response, "query": data.query}
