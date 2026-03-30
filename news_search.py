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
        news = search_naver_rss(query)
        for n in news:
            if n not in results:
                results.append(n)
        if len(results) >= 5:
            break
        time.sleep(0.3)

    return results[:5] if results else ['관련 뉴스 없음']


def search_naver_rss(query):
    try:
        url = f"https://news.naver.com/search/results.naver?query={requests.utils.quote(query)}&section=0&ie=utf8"
        res = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(res.text, 'html.parser')

        results = []
        for item in soup.select('a.news_tit, dl dt a, .title a'):
            title = item.get_text(strip=True)
            if title and 10 < len(title) < 100:
                results.append(title)
            if len(results) >= 3:
                break

        # RSS 방식으로 시도
        if not results:
            rss_url = f"https://news.naver.com/search/news.naver?query={requests.utils.quote(query)}&type=1&office_type=0"
            res2 = requests.get(rss_url, headers=headers, timeout=8)
            soup2 = BeautifulSoup(res2.text, 'html.parser')
            for item in soup2.find_all('title')[1:4]:
                title = item.get_text(strip=True)
                if title and 10 < len(title) < 100:
                    results.append(title)

        return results
    except Exception as e:
        print(f"뉴스 오류: {e}")
        return []
