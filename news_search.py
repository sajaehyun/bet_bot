import requests
from bs4 import BeautifulSoup
import time
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
}

def get_news_for_game(home, away):
    results = []

    queries = [
        f"{home} {away} 축구 평가전",
        f"{home} 축구 국가대표 부상 컨디션",
        f"{away} 축구 국가대표 부상 컨디션",
    ]

    for query in queries:
        news = search_google_news(query)
        for n in news:
            if n not in results:
                results.append(n)
        if len(results) >= 5:
            break
        time.sleep(0.5)

    return results[:5] if results else ['관련 뉴스 없음']


def search_google_news(query):
    try:
        url = f"https://news.google.com/search?q={requests.utils.quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        results = []
        # 구글 뉴스 기사 제목 태그
        for tag in soup.select('a.JtKRv, a.gPFEn, h3, h4'):
            title = tag.get_text(strip=True)
            if title and 10 < len(title) < 120:
                # 광고/불필요한 텍스트 제외
                skip = ['Google', '뉴스', '더보기', '전체', '최신']
                if not any(s == title for s in skip):
                    results.append(title)
            if len(results) >= 3:
                break

        return results
    except Exception as e:
        print(f"뉴스 오류: {e}")
        return []
