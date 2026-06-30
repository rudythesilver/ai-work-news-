import feedparser
import json
import datetime
import os
import re
from urllib.parse import quote

# 1. 검색어 설정 (더 안정적인 검색을 위해 키워드를 조합합니다)
query = quote("AI 업무 활용 OR 인공지능 실무")
RSS_URL = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"

def clean_html(raw_html):
    if not raw_html: return ""
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html)

def fetch_ai_news():
    try:
        print(f"뉴스 수집 시작: {RSS_URL}")
        feed = feedparser.parse(RSS_URL)
        
        news_list = []
        
        for entry in feed.entries:
            # 2. 에러 링크 필터링 (중요!)
            # 제목이나 링크에 '에러' 혹은 '사용할 수 없는' 문구가 있으면 버립니다.
            if "사용할 수 없는" in entry.title or "unfepa" in entry.link:
                continue
                
            title = entry.title
            # 제목 뒤에 붙는 언론사 이름 정리 (예: 제목 - 지디넷코리아 -> 제목)
            title = title.split(" - ")[0]

            summary_clean = clean_html(entry.get("summary", ""))
            summary_short = summary_clean[:100] + "..." if len(summary_clean) > 100 else summary_clean

            news_list.append({
                "title": title,
                "link": entry.link,
                "summary": summary_short,
                "date": datetime.datetime.now().strftime("%Y-%m-%d")
            })
            
            # 최대 12개까지만 수집
            if len(news_list) >= 12:
                break
        
        # 3. 데이터 저장
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=4)
            
        if not news_list:
            print("수집된 뉴스가 없습니다. 키워드를 확인하세요.")
        else:
            print(f"성공: {len(news_list)}개의 실제 기사를 저장했습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")
        if not os.path.exists('data.json'):
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump([], f)

if __name__ == "__main__":
    fetch_ai_news()
