from crawler import get_betman_games
from news_search import get_news_for_game
import time

def collect_all():
    print("betman 경기 목록 수집 중...")
    games = get_betman_games()
    
    if not games:
        print("경기 목록을 가져오지 못했습니다.")
        return
    
    print(f"총 {len(games)}경기 발견\n")
    
    output = []
    output.append(f"=== 총 {len(games)}경기 ===\n")
    
    for i, game in enumerate(games):
        home = game['home']
        away = game['away']
        time_str = game.get('time', '')
        
        print(f"[{i+1}/{len(games)}] {home} vs {away} 뉴스 수집 중...")
        
        news = get_news_for_game(home, away)
        
        output.append(f"""
{'='*50}
경기 {i+1}: {home} vs {away} ({time_str})
{'='*50}
{news}
""")
        time.sleep(0.3)
    
    # 파일로 저장
    result_text = "\n".join(output)
    
    with open("games_news.txt", "w", encoding="utf-8") as f:
        f.write(result_text)
    
    print("\n✅ 저장 완료: games_news.txt")
    print("이 파일 내용을 Claude 채팅창에 붙여넣으세요!")
    
    return result_text

if __name__ == "__main__":
    collect_all()