import requests
import json

def test_api():
    url = "http://127.0.0.1:8000/classify"
    payload = {
        "ticket_text": "I can't log into my account and I need to reset my password immediately. It says my email is not recognized."
    }
    
    print(f"Testing API at: {url}")
    print(f"Payload: {payload}")
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("\n✅ Classification Result:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        print("\nNote: Make sure the FastAPI server is running with 'uvicorn main:app --reload'")

if __name__ == "__main__":
    test_api()
