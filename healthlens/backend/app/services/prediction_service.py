import joblib
import os
import pandas as pd
import numpy as np
from .mapping_service import map_health_data

# Use explicit absolute or package-relative paths
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))

models = {
    "heart": None,
    "diabetes": None,
    "cardio": None,
    "health_indicators": None
}

def load_models():
    """Load the trained models and their scalers into memory"""
    import logging
    logger = logging.getLogger("uvicorn")
    logger.info(f"Loading models from {MODEL_DIR}...")
    try:
        models["heart"] = joblib.load(os.path.normpath(os.path.join(MODEL_DIR, "heart_model.pkl")))
        models["diabetes"] = joblib.load(os.path.normpath(os.path.join(MODEL_DIR, "diabetes_model.pkl")))
        models["cardio"] = joblib.load(os.path.normpath(os.path.join(MODEL_DIR, "cardio_model.pkl")))
        
        hi_path = os.path.normpath(os.path.join(MODEL_DIR, "health_indicators_model.pkl"))
        if os.path.exists(hi_path):
            models["health_indicators"] = joblib.load(hi_path)
            logger.info("Successfully loaded health_indicators model")
        logger.info("Models loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model artifacts: {e}", exc_info=True)

def get_risk_level(risk_percentage: float) -> str:
    if risk_percentage < 30:
        return "Low"
    elif risk_percentage < 70:
        return "Medium"
    else:
        return "High"

def predict_all_risks(user_data: dict) -> dict:
    # Ensure models are loaded
    if models["heart"] is None:
        load_models()
        
    risks = {}
    levels = {}
    
    # We predict core 3: heart, diabetes, hypertension(cardio)
    core_datasets = {
        "heart": "heart_risk",
        "diabetes": "diabetes_risk",
        "cardio": "hypertension_risk"
    }
    
    for model_key, out_key in core_datasets.items():
        artifact = models.get(model_key)
        if not artifact:
            risks[out_key] = 0.0
            levels[model_key] = "Unknown"
            continue
            
        try:
            print(f"Processing prediction for {model_key}...")
            # Detect if it's a dict or the model directly
            if isinstance(artifact, dict) and 'model' in artifact:
                model = artifact['model']
                scaler = artifact['scaler']
            else:
                print(f"Warning: {model_key} artifact is not a dictionary with 'model' key. It is a {type(artifact)}")
                # Support fallthrough if the model was saved directly in a previous run
                model = artifact
                scaler = None
            
            mapped_data = map_health_data(user_data, model_key)
            print(f"Mapped {model_key} data: {mapped_data}")
            df = pd.DataFrame([mapped_data])
            
            if scaler:
                scaled_features = scaler.transform(df)
            else:
                scaled_features = df.values
                
            probas = model.predict_proba(scaled_features)
            
            if probas.shape[1] > 1:
                risk_prob = probas[0][1]
            else:
                risk_prob = probas[0][0]
                
            risk_pct = round(float(risk_prob * 100), 1)
            risks[out_key] = risk_pct
            levels[model_key] = get_risk_level(risk_pct)
            print(f"Success: {model_key} risk is {risk_pct}%")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error predicting {model_key}: {e}")
            risks[out_key] = 0.0
            levels[model_key] = "Error"
            
    return {
        **risks,
        "risk_level": levels
    }
