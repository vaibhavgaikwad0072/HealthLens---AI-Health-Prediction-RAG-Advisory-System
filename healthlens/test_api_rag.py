import httpx
import json

def test_api():
    print("Testing HealthLens API...")
    
    # Test Predict All (should include recommendation)
    predict_url = "http://localhost:8000/api/predict/all"
    payload = {
        "age": 45,
        "bmi": 28.5,
        "heart_rate": 78,
        "glucose": 110.0,
        "steps": 4000,
        "sleep_hours": 6.0,
        "gender": "male",
        "blood_pressure": "130/85"
    }
    
    try:
        print("\nSending prediction request...")
        with httpx.Client(timeout=60.0) as client:
            res = client.post(predict_url, json=payload)
            print(f"Status: {res.status_code}")
            data = res.json()
            print(f"Heart Risk: {data.get('heart_risk')}%")
            print(f"Diabetes Risk: {data.get('diabetes_risk')}%")
            print(f"Cardio Risk: {data.get('hypertension_risk')}%")
            print(f"Recommendation: {data.get('recommendation')}")
    except Exception as e:
        print(f"Error testing prediction: {e}")

    # Test Chat
    chat_url = "http://localhost:8000/api/chat"
    try:
        print("\nSending chat query: 'How to lower my heart risk?'")
        with httpx.Client(timeout=60.0) as client:
            res = client.post(chat_url, json={"query": "How to lower my heart risk?"})
            print(f"Status: {res.status_code}")
            print(f"AI Response: {res.json().get('response')}")
    except Exception as e:
        print(f"Error testing chat: {e}")

if __name__ == "__main__":
    test_api()
