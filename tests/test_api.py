import requests

BASE = "http://localhost:8000"

def test_deploy_function():
    with open("functions/multiply.py", 'rb') as f:
        files = {'file': f}
        data = {"name": "multiply", "language": "python", "timeout": 5}
        response = requests.post(f"{BASE}/deploy", data=data, files=files)
        assert response.status_code == 200

def test_run_function():
    response = requests.post(f"{BASE}/execute", params={"name": "multiply"})
    assert response.status_code == 200
    result = response.json().get("result")
    assert result is not None  # Adjust based on your actual output structure
