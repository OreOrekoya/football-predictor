from api import get_team_form, get_head_to_head

def calculate_form_score(fixtures, team_id):
    """Calculate a form score based on last N results (W=3, D=1, L=0)"""
    score = 0
    for fixture in fixtures:
        home_id = fixture["teams"]["home"]["id"]
        away_id = fixture["teams"]["away"]["id"]
        home_goals = fixture["goals"]["home"]
        away_goals = fixture["goals"]["away"]

        if home_goals is None or away_goals is None:
            continue

        if team_id == home_id:
            if home_goals > away_goals:
                score += 3
            elif home_goals == away_goals:
                score += 1
        else:
            if away_goals > home_goals:
                score += 3
            elif home_goals == away_goals:
                score += 1
    return score

def calculate_avg_goals(fixtures, team_id):
    """Calculate average goals scored and conceded"""
    scored, conceded = [], []
    for fixture in fixtures:
        home_id = fixture["teams"]["home"]["id"]
        home_goals = fixture["goals"]["home"]
        away_goals = fixture["goals"]["away"]

        if home_goals is None or away_goals is None:
            continue

        if team_id == home_id:
            scored.append(home_goals)
            conceded.append(away_goals)
        else:
            scored.append(away_goals)
            conceded.append(home_goals)

    avg_scored = sum(scored) / len(scored) if scored else 0
    avg_conceded = sum(conceded) / len(conceded) if conceded else 0
    return avg_scored, avg_conceded

def predict_match_data(team1_id, team2_id, team1_name, team2_name):
    """Return prediction data as a dict for the web UI"""
    team1_form = get_team_form(team1_id)
    team2_form = get_team_form(team2_id)
    h2h = get_head_to_head(team1_id, team2_id)

    team1_score = calculate_form_score(team1_form, team1_id)
    team2_score = calculate_form_score(team2_form, team2_id)

    team1_h2h = calculate_form_score(h2h, team1_id)
    team2_h2h = calculate_form_score(h2h, team2_id)

    team1_avg_scored, team1_avg_conceded = calculate_avg_goals(team1_form, team1_id)
    team2_avg_scored, team2_avg_conceded = calculate_avg_goals(team2_form, team2_id)

    team1_total = team1_score + team1_h2h
    team2_total = team2_score + team2_h2h

    if team1_total > team2_total:
        winner = team1_name.title()
    elif team2_total > team1_total:
        winner = team2_name.title()
    else:
        winner = "Draw"

    return {
        "team1": team1_name.title(),
        "team2": team2_name.title(),
        "team1_form": team1_score,
        "team2_form": team2_score,
        "team1_h2h": team1_h2h,
        "team2_h2h": team2_h2h,
        "team1_avg_scored": round(team1_avg_scored, 1),
        "team2_avg_scored": round(team2_avg_scored, 1),
        "team1_avg_conceded": round(team1_avg_conceded, 1),
        "team2_avg_conceded": round(team2_avg_conceded, 1),
        "winner": winner
    }