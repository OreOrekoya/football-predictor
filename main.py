from flask import Flask, render_template, request, jsonify
from api import get_team_id
from predictor import predict_match_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    team1_name = data.get('team1')
    team2_name = data.get('team2')

    team1_id = get_team_id(team1_name)
    team2_id = get_team_id(team2_name)

    if not team1_id:
        return jsonify({'error': f'Could not find team: {team1_name}'})
    if not team2_id:
        return jsonify({'error': f'Could not find team: {team2_name}'})

    result = predict_match_data(team1_id, team2_id, team1_name, team2_name)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)