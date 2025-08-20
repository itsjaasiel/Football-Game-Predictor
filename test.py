import requests, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("FOOTBALL_API_KEY")

print("Key is:", API_KEY)

url = "https://v3.football.api-sports.io/status"
headers = {"x-apisports-key": API_KEY}
res = requests.get(url, headers=headers)
print(res.json())
