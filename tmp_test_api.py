import requests
import json

url = "http://127.0.0.1:8000/api/predict/all"
data = {
    "age": 42,
    "bmi": 26.5,
    "heart_rate": 72,
    "glucose": 95,
    "steps": 6500,
    "sleep_hours": 7.5
}
try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
