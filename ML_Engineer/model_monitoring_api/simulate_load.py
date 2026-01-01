import requests
import time
import random

def simulate_load(n_requests=100):
    url = "http://127.0.0.1:8000/predict"
    print(f"🚀 Simulating {n_requests} requests to {url}...")
    
    for i in range(n_requests):
        payload = {"features": [random.random() for _ in range(5)]}
        try:
            res = requests.post(url, json=payload)
            if i % 10 == 0:
                print(f"Request {i}: Status {res.status_code}")
        except Exception as e:
            print(f"Connection failed: {e}")
            break
        time.sleep(0.1)
    
    print("\n✅ Simulation complete. Visit http://127.0.0.1:8000/metrics to see the stats!")

if __name__ == "__main__":
    simulate_load()
