def map_health_data(input_data: dict, dataset_type: str) -> dict:
    """
    Map smartwatch and manual input data into the exact feature format needed by each ML model.
    Handles missing values by applying sensible defaults.
    """
    age = input_data.get("age", 40)
    bmi = input_data.get("bmi", 25.0)
    heart_rate = input_data.get("heart_rate", 70)
    glucose = input_data.get("glucose", 90.0)
    steps = input_data.get("steps", 5000)
    sleep = input_data.get("sleep_hours", 7.0)
    gender_str = str(input_data.get("gender", "male")).lower()
    
    # Blood pressure parsing
    bp_parts = str(input_data.get("blood_pressure", "120/80")).split("/")
    ap_hi = int(bp_parts[0]) if len(bp_parts) == 2 else 120
    ap_lo = int(bp_parts[1]) if len(bp_parts) == 2 else 80
    
    # Generic mapping matching standard numerical and categorical expectations
    if dataset_type == "heart":
        return {
            "age": age,
            "sex": 1 if gender_str == "male" else 0,
            "cp": 1, # typical angina
            "trestbps": ap_hi,
            "chol": 200,
            "fbs": 1 if glucose > 120 else 0,
            "restecg": 0, # normal
            "thalch": heart_rate,
            "exang": 0,
            "oldpeak": 0.0,
            "slope": 1, # upsloping
            "ca": 0,
            "thal": 3  # normal (standard mapping is 3, 6, 7)
        }
    elif dataset_type == "diabetes":
        return {
            "Pregnancies": 0 if gender_str == "male" else 1,
            "Glucose": glucose,
            "BloodPressure": ap_lo,
            "SkinThickness": 20,
            "Insulin": 80,
            "BMI": bmi,
            "DiabetesPedigreeFunction": 0.5,
            "Age": age
        }
    elif dataset_type == "cardio":
        return {
            "age": age * 365,
            "gender": 2 if gender_str == "male" else 1,
            "height": 170,
            "weight": bmi * ((170/100)**2),
            "ap_hi": ap_hi,
            "ap_lo": ap_lo,
            "cholesterol": 1,
            "gluc": 1,
            "smoke": 0,
            "alco": 0,
            "active": 1 if steps > 5000 else 0
        }
    elif dataset_type == "health_indicators":
        return {
            "HighBP": 1 if ap_hi >= 130 else 0,
            "HighChol": 0,
            "CholCheck": 1,
            "BMI": bmi,
            "Smoker": 0,
            "Stroke": 0,
            "HeartDiseaseorAttack": 0,
            "PhysActivity": 1 if steps > 5000 else 0,
            "Fruits": 1,
            "Veggies": 1,
            "HvyAlcoholConsump": 0,
            "AnyHealthcare": 1,
            "NoDocbcCost": 0,
            "GenHlth": 3,
            "MentHlth": 0,
            "PhysHlth": 0,
            "DiffWalk": 0,
            "Sex": 1 if gender_str == "male" else 0,
            "Age": min(13, max(1, (age - 18) // 5 + 1)), # Simplified age bracket mapping
            "Education": 5,
            "Income": 6
        }
    
    return {}
