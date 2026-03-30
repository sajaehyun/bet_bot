import requests
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
}

def get_news_for_game(home, away):
    results = []
    queries = [
        f"{home} {away} 축구",
        f"{home} 국가대표",
        f"{away} 국가대표",
    ]
    for query in queries:
        news = search_google_rss(query)
        for n in news:
            if n not in results:
                results.append(n)
        if len(results) >= 5:
            break
        time.sleep(0.3)
    return results[:5] if results else ['관련 뉴스 없음']


def search_google_rss(query):
    try:
        url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'xml')

        results = []
        for item in soup.find_all('item'):
            title = item.find('title')
            if title:
                txt = title.get_text(strip=True)
                if txt and 10 < len(txt) < 100:
                    results.append(txt)
            if len(results) >= 3:
                break
        return results
    except Exception as e:
        print(f"뉴스 오류: {e}")
        return []
