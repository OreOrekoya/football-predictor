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

def predict_match(team1_id, team2_id, team1_name, team2_name):
    """Predict match outcome based on form and h2h"""
    print(f"\nAnalysing: {team1_name} vs {team2_name}...\n")

    team1_form = get_team_form(team1_id)
    team2_form = get_team_form(team2_id)
    h2h = get_head_to_head(team1_id, team2_id)

    team1_score = calculate_form_score(team1_form, team1_id)
    team2_score = calculate_form_score(team2_form, team2_id)

    team1_h2h_score = calculate_form_score(h2h, team1_id)
    team2_h2h_score = calculate_form_score(h2h, team2_id)

    team1_avg_scored, team1_avg_conceded = calculate_avg_goals(team1_form, team1_id)
    team2_avg_scored, team2_avg_conceded = calculate_avg_goals(team2_form, team2_id)

    team1_total = team1_score + team1_h2h_score
    team2_total = team2_score + team2_h2h_score

    print(f"--- Form (last 5) ---")
    print(f"{team1_name}: {team1_score}/15 pts")
    print(f"{team2_name}: {team2_score}/15 pts")

    print(f"\n--- Head to Head (last 5) ---")
    print(f"{team1_name}: {team1_h2h_score} pts")
    print(f"{team2_name}: {team2_h2h_score} pts")

    print(f"\n--- Avg Goals Scored ---")
    print(f"{team1_name}: {team1_avg_scored:.1f} | Conceded: {team1_avg_conceded:.1f}")
    print(f"{team2_name}: {team2_avg_scored:.1f} | Conceded: {team2_avg_conceded:.1f}")

    print(f"\n--- Prediction ---")
    if team1_total > team2_total:
        print(f"Winner: {team1_name}")
    elif team2_total > team1_total:
        print(f"Winner: {team2_name}")
    else:
        print("Too close to call — likely a draw")