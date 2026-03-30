import requests
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
}

def get_form_and_h2h(home, away):
    try:
        home_form = get_team_form(home)
        time.sleep(0.3)
        away_form = get_team_form(away)
        time.sleep(0.3)
        h2h = get_h2h(home, away)

        return {
            'home_form': home_form,
            'away_form': away_form,
            'h2h': h2h
        }
    except Exception as e:
        return {
            'home_form': '데이터 없음',
            'away_form': '데이터 없음',
            'h2h': '데이터 없음'
        }


def get_team_form(team):
    try:
        query = f"{team} 축구 최근경기 결과"
        url = f"https://search.naver.com/search.naver?where=news&query={requests.utils.quote(query)}&sort=1"
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')

        results = []
        articles = soup.select('.news_tit')[:3]
        for a in articles:
            text = a.get_text(strip=True)
            if text:
                results.append(text)

        return ' | '.join(results) if results else f"{team} 최근 폼 데이터 없음"
    except:
        return "폼 데이터 없음"


def get_h2h(home, away):
    try:
        query = f"{home} {away} 상대전적 역대전적"
        url = f"https://search.naver.com/search.naver?where=news&query={requests.utils.quote(query)}&sort=1"
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')

        results = []
        articles = soup.select('.news_tit')[:3]
        for a in articles:
            text = a.get_text(strip=True)
            if text:
                results.append(text)

        return ' | '.join(results) if results else "상대전적 데이터 없음"
    except:
        return "상대전적 데이터 없음"
