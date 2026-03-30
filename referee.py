import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
}

REFEREE_DB = {
    '김대용': {'style': '엄격', 'avg_fouls': 28, 'avg_yellows': 4.2, 'home_bias': '중립', 'note': '파울에 민감, 옐로카드 많음'},
    '고형진': {'style': '관대', 'avg_fouls': 22, 'avg_yellows': 2.8, 'home_bias': '홈팀 유리', 'note': '접촉 플레이 허용'},
    '김우성': {'style': '보통', 'avg_fouls': 25, 'avg_yellows': 3.5, 'home_bias': '중립', 'note': '표준적 판정'},
    '이동준': {'style': '엄격', 'avg_fouls': 30, 'avg_yellows': 4.8, 'home_bias': '중립', 'note': '반칙에 엄격'},
    '기본값': {'style': '보통', 'avg_fouls': 25, 'avg_yellows': 3.5, 'home_bias': '중립', 'note': '데이터 없음'},
}


def get_referee_info(home, away):
    referee_name = fetch_referee_name(home, away)
    info = REFEREE_DB.get(referee_name, REFEREE_DB['기본값'])

    return {
        'name': referee_name,
        'style': info['style'],
        'avg_fouls': info['avg_fouls'],
        'avg_yellows': info['avg_yellows'],
        'home_bias': info['home_bias'],
        'note': info['note']
    }


def fetch_referee_name(home, away):
    try:
        query = f"{home} {away} 주심 심판 2026"
        url = f"https://search.naver.com/search.naver?where=news&query={requests.utils.quote(query)}&sort=1"
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')

        articles = soup.select('.news_tit')[:3]
        for a in articles:
            text = a.get_text(strip=True)
            for name in REFEREE_DB.keys():
                if name != '기본값' and name in text:
                    return name

        return "심판 정보 없음"
    except:
        return "심판 정보 없음"
