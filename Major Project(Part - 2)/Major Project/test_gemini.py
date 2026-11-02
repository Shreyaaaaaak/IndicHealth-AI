import os
import httpx
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY", "").strip().strip('"').strip("'")
print(f"Testing key: {api_key[:8]}... (Length: {len(api_key)})")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={api_key}"

with httpx.Client(timeout=30.0) as client:
    try:
        res = client.post(url, json={"contents": [{"parts": [{"text": "Hello in 3 words"}]}]})
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            print("Response:", res.json()["candidates"][0]["content"]["parts"][0]["text"])
        else:
            print("Error:", res.text)
    except Exception as e:
        print("Exception:", e)
