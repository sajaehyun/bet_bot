from flask import Flask, jsonify
from crawler import get_betman_games
from news_search import get_news_for_game
import time

app = Flask(__name__)

@app.route('/')
def index():
    return "Betman Analyzer API 작동 중 ✅"

@app.route('/collect')
def collect():
    games = get_betman_games()
    result = []
    for game in games:
        home = game['home']
        away = game['away']
        news = get_news_for_game(home, away)
        time.sleep(0.3)
        result.append({
            'home': home,
            'away': away,
            'odd_home': game.get('odd_home'),
            'odd_draw': game.get('odd_draw'),
            'odd_away': game.get('odd_away'),
            'signal': game.get('signal'),
            'news': news
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
