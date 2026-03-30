import requests
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
}


def get_injury_report(home, away):
    home_injuries = search_injuries(home)
    away_injuries = search_injuries(away)
    return {
        'home_injuries': home_injuries,
        'away_injuries': away_injuries
    }


def search_injuries(team):
    """네이버 웹 스크래핑으로 부상 정보 검색"""
    try:
        query = f"{team} 부상 결장 출전불가 2026"
        url = f"https://search.naver.com/search.naver?where=news&query={requests.utils.quote(query)}&sort=1"
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')

        results = []
        articles = soup.select('.news_tit')[:3]
        for a in articles:
            text = a.get_text(strip=True)
            if text:
                results.append(text)

        time.sleep(0.3)
        return '\n'.join(results) if results else f"{team} 부상자 정보 없음"
    except Exception as e:
        return f"부상 정보 수집 실패: {e}"