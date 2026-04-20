from api import get_team_id
from predictor import predict_match

def main():
    print("=== Football Match Predictor ===\n")
    
    team1_name = input("Enter home team: ")
    team2_name = input("Enter away team: ")
    
    print("\nFetching team data...")
    
    team1_id = get_team_id(team1_name)
    team2_id = get_team_id(team2_name)
    
    if not team1_id:
        print(f"Could not find team: {team1_name}")
        return
    if not team2_id:
        print(f"Could not find team: {team2_name}")
        return
    
    predict_match(team1_id, team2_id, team1_name, team2_name)

if __name__ == "__main__":
    main()