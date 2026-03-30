import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
}

def get_betman_games():
    try:
        res = requests.get('https://www.zentoto.com/toto/soccer', headers=headers, timeout=15)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        games = []
        rows = soup.select('table tr')

        for row in rows:
            tds = row.select('td')
            if len(tds) < 5:
                continue

            no_text = tds[0].get_text(strip=True)
            if not re.match(r'^\d+$', no_text):
                continue
            no = int(no_text)

            row_text = row.get_text(separator='\n')
            pcts = re.findall(r'(\d+\.\d+)\s*%', row_text)

            team_names = []
            skip_words = ['경기분석', '투표', '순위', '보기', '승점', '선택', 'VS', 'vs']
            for td in tds:
                for img in td.select('img'):
                    alt = img.get('alt', '').strip()
                    if alt and 2 <= len(alt) <= 8 and re.search(r'[가-힣]', alt):
                        if alt not in team_names:
                            team_names.append(alt)
                txt = td.get_text(strip=True)
                if txt and 2 <= len(txt) <= 7 and re.search(r'[가-힣]', txt):
                    if '%' not in txt and txt not in team_names:
                        if not any(w in txt for w in skip_words):
                            team_names.append(txt)

            if len(team_names) < 2:
                continue

            home = team_names[0]
            away = team_names[1]
            pct_h = pcts[0] if len(pcts) > 0 else '0'
            pct_d = pcts[1] if len(pcts) > 1 else '0'
            pct_a = pcts[2] if len(pcts) > 2 else '0'

            games.append({
                'no': no,
                'time': '-',
                'league': '남축INTL',
                'home': home,
                'away': away,
                'odd_home': f'{pct_h}%',
                'odd_draw': f'{pct_d}%',
                'odd_away': f'{pct_a}%',
                'signal': calc_signal_pct(pct_h, pct_a)
            })

        if games:
            print(f"✅ 젠토토 {len(games)}경기 수집 완료!")
            return games

        print("⚠️ 파싱 실패 → 더미 사용")
        return get_dummy_games()

    except Exception as e:
        print(f"❌ 오류: {e}")
        return get_dummy_games()


def calc_signal_pct(pct_h, pct_a):
    try:
        h = float(str(pct_h).replace('%', ''))
        a = float(str(pct_a).replace('%', ''))
        if h >= 70:
            return f"홈팀 압도적 우세 {h}% ⚠️"
        elif a >= 70:
            return f"원정팀 압도적 우세 {a}% ⚠️"
        elif h > a:
            return f"홈팀 우세 ({h}% vs {a}%)"
        elif a > h:
            return f"원정팀 우세 ({a}% vs {h}%)"
        else:
            return "균형 경기"
    except:
        return ""


def get_dummy_games():
    return [
        {'no': 1, 'time': '-', 'league': '남축INTL', 'home': '노르웨이', 'away': '스위스',
         'odd_home': '49.91%', 'odd_draw': '29.18%', 'odd_away': '20.91%', 'signal': '홈팀 우세'},
        {'no': 2, 'time': '-', 'league': '남축INTL', 'home': '아이티', 'away': '아이슬란',
         'odd_home': '11.03%', 'odd_draw': '15.53%', 'odd_away': '73.44%', 'signal': '원정팀 압도적 우세 73.44% ⚠️'},
        {'no': 3, 'time': '-', 'league': '남축INTL', 'home': '헝가리', 'away': '그리스',
         'odd_home': '59.69%', 'odd_draw': '26.29%', 'odd_away': '14.02%', 'signal': '홈팀 우세'},
    ]
