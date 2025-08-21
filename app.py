from flask import Flask, render_template, request, jsonify
import requests, os
from dotenv import load_dotenv
from datetime import date

load_dotenv()
API_KEY = os.getenv("ODDS_API_KEY")
if not API_KEY:
    raise RuntimeError("ODDS_API_KEY not found in environment")

BASE_URL = "https://api.the-odds-api.com/v4/sports"

app = Flask(__name__)

LEAGUES = {
    "soccer_epl": "Premier League",
    "soccer_spain_la_liga": "La Liga",
    "soccer_italy_serie_a": "Serie A",
    "soccer_germany_bundesliga": "Bundesliga",
    "soccer_france_ligue_one": "Ligue 1"
}


@app.route("/")
def index():
    return render_template("index.html", leagues=LEAGUES)


@app.route("/api/odds")
def api_odds():
    selected_date = request.args.get("date", date.today().isoformat())
    selected_leagues = request.args.get("leagues", "").split(",")
    if not selected_leagues or selected_leagues == [""]:
        selected_leagues = list(LEAGUES.keys())

    fixtures_by_league = {}

    for league_id in selected_leagues:
        league_name = LEAGUES.get(league_id, league_id)
        url = f"{BASE_URL}/{league_id}/odds"
        params = {
            "apiKey": API_KEY,
            "regions": "eu",
            "markets": "h2h",
            "oddsFormat": "decimal",
            "dateFormat": "iso",
            "commenceTimeFrom": selected_date + "T00:00:00Z",
            "commenceTimeTo": selected_date + "T23:59:59Z"
        }
        try:
            r = requests.get(url, params=params)
            r.raise_for_status()
            data = r.json()

            bookmakers_set = set()
            matches = []

            for match in data:
                odds_by_bookmaker = {}
                for book in match.get("bookmakers", []):
                    bm_name = book["title"]
                    bookmakers_set.add(bm_name)
                    # Get h2h market
                    h2h_market = next((m for m in book["markets"] if m["key"] == "h2h"), None)
                    if h2h_market:
                        for outcome in h2h_market["outcomes"]:
                            if outcome["name"] == match["home_team"]:
                                odds_by_bookmaker[bm_name] = outcome["price"]

                matches.append({
                    "home_team": match["home_team"],
                    "away_team": match["away_team"],
                    "odds": odds_by_bookmaker
                })

            fixtures_by_league[league_name] = {
                "bookmakers": sorted(bookmakers_set),
                "matches": matches
            }

        except Exception as e:
            print(f"Error fetching {league_name}: {e}")

    return jsonify({"success": True, "fixtures_by_league": fixtures_by_league})


if __name__ == "__main__":
    app.run(debug=True)