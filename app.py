from flask import Flask, jsonify, render_template_string
from crawler import get_betman_games
from news_search import get_news_for_game

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>승무패 분석기</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #1a1a2e; color: #eee; }
        h1 { color: #e94560; text-align: center; }
        .btn { display: block; margin: 30px auto; padding: 15px 50px; background: #e94560; color: white; border: none; border-radius: 10px; font-size: 1.2em; cursor: pointer; }
        .btn:disabled { background: #555; cursor: not-allowed; }
        .game { background: #16213e; border-radius: 10px; padding: 20px; margin-bottom: 20px; border-left: 4px solid #e94560; }
        .teams { font-size: 1.4em; font-weight: bold; color: #fff; margin-bottom: 10px; }
        .odds { display: flex; gap: 15px; margin-bottom: 10px; flex-wrap: wrap; }
        .odd-box { background: #0f3460; padding: 10px 15px; border-radius: 8px; text-align: center; min-width: 80px; }
        .odd-box .label { font-size: 0.8em; color: #888; }
        .odd-box .value { font-size: 1.2em; font-weight: bold; color: #e94560; }
        .signal { background: #e94560; color: white; padding: 5px 10px; border-radius: 5px; display: inline-block; margin-bottom: 10px; font-size: 0.9em; }
        .news { background: #0f3460; padding: 10px; border-radius: 8px; }
        .news-item { padding: 5px 0; border-bottom: 1px solid #1a1a2e; font-size: 0.85em; }
        .news-item:last-child { border-bottom: none; }
        #status { text-align: center; color: #e94560; margin: 20px; font-size: 1.1em; }
        #result { margin-top: 20px; }
    </style>
</head>
<body>
    <h1>⚽ 승무패 분석기</h1>
    <button class="btn" id="btn" onclick="startCollect()">🔍 분석 시작</button>
    <div id="status"></div>
    <div id="result"></div>

    <script>
    function startCollect() {
        const btn = document.getElementById('btn');
        const status = document.getElementById('status');
        const result = document.getElementById('result');

        btn.disabled = true;
        btn.textContent = '⏳ 수집 중...';
        status.textContent = '경기 목록 수집 중...';
        result.innerHTML = '';

        // 1단계: 경기 목록만 먼저 가져오기
        fetch('/api/games')
            .then(res => res.json())
            .then(games => {
                status.textContent = `✅ ${games.length}경기 발견! 뉴스 수집 중...`;
                renderGames(games);

                // 2단계: 각 경기 뉴스 개별 요청
                games.forEach((g, i) => {
                    fetch(`/api/news?home=${encodeURIComponent(g.home)}&away=${encodeURIComponent(g.away)}`)
                        .then(res => res.json())
                        .then(news => {
                            const newsDiv = document.getElementById(`news-${i}`);
                            if (newsDiv) {
                                newsDiv.innerHTML = news.map(n => `<div class="news-item">📰 ${n}</div>`).join('');
                            }
                            // 마지막 경기 뉴스까지 완료되면 버튼 활성화
                            if (i === games.length - 1) {
                                btn.disabled = false;
                                btn.textContent = '🔍 다시 분석';
                                status.textContent = '✅ 분석 완료!';
                            }
                        });
                });
            })
            .catch(err => {
                status.textContent = '❌ 오류 발생, 다시 시도하세요';
                btn.disabled = false;
                btn.textContent = '🔍 분석 시작';
            });
    }

    function renderGames(games) {
        const result = document.getElementById('result');
        result.innerHTML = games.map((g, i) => `
            <div class="game">
                <div class="teams">${g.no}. ${g.home} vs ${g.away}</div>
                <div class="odds">
                    <div class="odd-box"><div class="label">홈 승</div><div class="value">${g.odd_home}</div></div>
                    <div class="odd-box"><div class="label">무</div><div class="value">${g.odd_draw}</div></div>
                    <div class="odd-box"><div class="label">원정 승</div><div class="value">${g.odd_away}</div></div>
                </div>
                ${g.signal ? `<div class="signal">${g.signal}</div>` : ''}
                <div class="news" id="news-${i}"><div class="news-item">⏳ 뉴스 수집 중...</div></div>
            </div>
        `).join('');
    }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/games')
def get_games():
    games = get_betman_games()
    return jsonify(games)

@app.route('/api/news')
def get_news():
    from flask import request
    home = request.args.get('home', '')
    away = request.args.get('away', '')
    news = get_news_for_game(home, away)
    return jsonify(news)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
