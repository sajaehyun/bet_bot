import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
}

# 홈팀 → 도시 매핑
TEAM_CITY_MAP = {
    '수원삼성': '수원', '수원FC': '수원', '용인FC': '용인',
    '포항': '포항', '강원FC': '강릉', '전북': '전주',
    'FC서울': '서울', '서울이랜드': '서울', '울산': '울산',
    '인천': '인천', '광주FC': '광주', '대구FC': '대구',
    '부산': '부산', '충북청주': '청주', '성남': '성남',
    '김포': '김포', '천안': '천안', '전남': '광양',
    '안산': '안산', '경남': '창원', '파주': '파주',
    '화성': '화성', '충남아산': '아산', '제주': '제주',
    '한국': '서울', '헝가리': '부다페스트', '일본': '도쿄',
    '노르웨이': '오슬로', '스위스': '베른', '오스트리아': '빈',
    '잉글랜드': '런던', '브라질': '올랜도', '멕시코': '멕시코시티',
    '미국': '뉴욕', '캐나다': '토론토', '모로코': '카사블랑카',
}


def get_weather(home_team):
    """네이버 날씨 스크래핑"""
    city = TEAM_CITY_MAP.get(home_team, '서울')

    try:
        url = f"https://search.naver.com/search.naver?query={requests.utils.quote(city+'날씨')}"
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')

        # 현재 기온
        temp_el = soup.select_one('.temperature_text, .current_temp, .temp')
        temp = temp_el.get_text(strip=True) if temp_el else '-'

        # 날씨 상태
        desc_el = soup.select_one('.weather_main, .sky_condition, .desc')
        description = desc_el.get_text(strip=True) if desc_el else '-'

        # 습도
        humidity_el = soup.select_one('.humidity, .item_humidity')
        humidity = humidity_el.get_text(strip=True) if humidity_el else '-'

        # 바람
        wind_el = soup.select_one('.wind_speed, .item_wind')
        wind = wind_el.get_text(strip=True) if wind_el else '-'

        impact = analyze_weather_impact(description, temp)

        return {
            'city': city,
            'description': description,
            'temp': temp,
            'humidity': humidity,
            'wind': wind,
            'impact': impact
        }

    except Exception as e:
        return {
            'city': city,
            'description': f'날씨 수집 실패: {e}',
            'temp': '-', 'humidity': '-', 'wind': '-',
            'impact': '날씨 정보 없음'
        }


def analyze_weather_impact(description, temp):
    """날씨 영향 분석"""
    impacts = []

    if any(k in description for k in ['비', '소나기', '우천']):
        impacts.append("🌧️ 강우 - 미끄러운 그라운드, 수비적 경기 예상")
    if any(k in description for k in ['눈', '폭설']):
        impacts.append("❄️ 눈 - 경기력 저하, 득점 감소 가능")
    if any(k in description for k in ['강풍', '바람']):
        impacts.append("💨 강풍 - 롱볼·코너킥 영향")

    try:
        t = float(temp.replace('°', '').replace('C', '').replace(' ', '').replace('현재온도', '').strip())
        if t < 0:
            impacts.append(f"🥶 영하({t}°C) - 선수 체력 소모 증가")
        elif t > 30:
            impacts.append(f"🔥 고온({t}°C) - 후반 체력 저하 주의")
        else:
            impacts.append(f"☀️ 적정 온도({t}°C) - 정상 컨디션 예상")
    except:
        impacts.append("🌤️ 날씨 양호 예상")

    return ' | '.join(impacts)
