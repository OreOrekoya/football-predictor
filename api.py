import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

def get_team_id(team_name, league_id=39, season=2024):
    """Search for a team and return its ID"""
    response = requests.get(
        f"{BASE_URL}/teams",
        headers=HEADERS,
        params={"name": team_name, "league": league_id, "season": season}
    )
    data = response.json()
    teams = data.get("response", [])
    if not teams:
        return None
    return teams[0]["team"]["id"]

def get_team_form(team_id, league_id=39, season=2024):
    """Get match results for a team this season"""
    response = requests.get(
        f"{BASE_URL}/fixtures",
        headers=HEADERS,
        params={
            "team": team_id,
            "league": league_id,
            "season": season,
            "status": "FT"
        }
    )
    fixtures = response.json().get("response", [])
    # Return last 5 manually
    return fixtures[-5:] if len(fixtures) >= 5 else fixtures

def get_head_to_head(team1_id, team2_id, season=2024):
    """Get head to head record between two teams"""
    response = requests.get(
        f"{BASE_URL}/fixtures/headtohead",
        headers=HEADERS,
        params={
            "h2h": f"{team1_id}-{team2_id}",
            "season": season,
            "status": "FT"
        }
    )
    fixtures = response.json().get("response", [])
    return fixtures[-5:] if len(fixtures) >= 5 else fixtures