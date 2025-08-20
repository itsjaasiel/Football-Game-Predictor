from flask import Flask, request, jsonify
import requests, os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://v3.football.api-sports.io"
headers = {"x-apisports-key": API_KEY}

app = Flask(__name__)

@app.route("/fixtures")
def get_fixtures():
    date = request.args.get("date")
    if not date:
        return jsonify({"error": "Missing date"}), 400

    url = f"{BASE_URL}/fixtures"
    params = {"date": date, "league": 39, "season": 2025}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        return jsonify({"error": "API call failed", "details": response.text}), 500
    
    return jsonify(response.json())
