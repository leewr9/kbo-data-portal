from flask import Flask, render_template, request, jsonify
from fetcher import fetch_game_list, fetch_match_info, fetch_rank_info

APP = Flask(__name__)

team = {
    "LG": {"full": "LG 트윈스", "color": "#C30452"},
    "OB": {"full": "두산 베어스", "color": "#0E1C34"},
    "SK": {"full": "SSG 랜더스", "color": "#E60012"},
    "WO": {"full": "키움 히어로즈", "color": "#76232F"},
    "KT": {"full": "KT 위즈", "color": "#000000"},
    "NC": {"full": "NC 다이노스", "color": "#012E67"},
    "HT": {"full": "KIA 타이거즈", "color": "#D6001C"},
    "SS": {"full": "삼성 라이온즈", "color": "#0072CE"},
    "LT": {"full": "롯데 자이언츠", "color": "#13294B"},
    "HH": {"full": "한화 이글스", "color": "#F26722"},
}

@APP.route("/get_match", methods=["POST"])
def get_match():
    data = request.get_json()
    game_id = data.get("game_id")

    match = fetch_match_info(game_id)
    rank = fetch_rank_info(match.SEASON_ID)
    
    home = [row for row in rank if row.TEAM_NM == match.HOME_NM][0]
    away = [row for row in rank if row.TEAM_NM == match.AWAY_NM][0]

    return jsonify({
        "SEASON_ID": match.SEASON_ID,
        "S_NM": match.S_NM,
        "G_DT_TXT": match.G_DT_TXT,
        "TV_IF": match.TV_IF,
        "HOME_ID": match.HOME_ID,
        "HOME_NM": team[match.HOME_ID]["full"],
        "HOME_SCORE": f"{home.W_CN}승 {home.D_CN}무 {home.L_CN}패 ( {home.RANK}위 )",
        "HOME_COLOR": team[match.HOME_ID]["color"],
        "AWAY_ID": match.AWAY_ID,
        "AWAY_NM": team[match.AWAY_ID]["full"],
        "AWAY_SCORE": f"{away.W_CN}승 {away.D_CN}무 {away.L_CN}패 ( {away.RANK}위 )",
        "AWAY_COLOR": team[match.AWAY_ID]["color"],
        "matches": [],
    })

@APP.route("/")
def index():
    return render_template("index.html", games=fetch_game_list(), home_color="#000000", away_color="#0072CE") 

if __name__ == "__main__":
    APP.run(debug=True)
