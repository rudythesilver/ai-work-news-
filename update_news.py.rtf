import feedparser
import json
import datetime
import os

RSS_URL = "https://news.google.com/rss/search?q=AI+업무+활용+언어:ko&hl=ko&gl=KR&ceid=KR:ko"

def fetch_ai_news():
    try:
        print("뉴스 수집 시작...")
        feed = feedparser.parse(RSS_URL)
        news_list = []

        for entry in feed.entries[:10]:
            news_list.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", "내용 없음")[:100] + "...",
                "date": datetime.datetime.now().strftime("%Y-%m-%d")
            })
        
        # 파일 저장
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=4)
        print(f"성공: {len(news_list)}개의 뉴스를 저장했습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")
        # 오류가 나도 빈 리스트라도 저장해서 에러 방지
        if not os.path.exists('data.json'):
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump([], f)

if __name__ == "__main__":
    fetch_ai_news()
