from flask import Flask, jsonify
import requests, os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://v3.football.api-sports.io"

headers = {"x-apisports-key": API_KEY}

app = Flask(__name__)

@app.route("/fixtures/<league_id>")
def get_fixtures(league_id):
    url = f"{BASE_URL}/fixtures?league={league_id}&season=2024&next=5"
    response = requests.get(url, headers=headers)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
