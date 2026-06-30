import feedparser
import json
import datetime
import os
import re
from urllib.parse import quote

# 검색 키워드를 안전하게 인코딩합니다 (AI 업무 활용)
query = quote("AI 업무 활용")
RSS_URL = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"

def clean_html(raw_html):
    if not raw_html: return ""
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html)

def fetch_ai_news():
    try:
        print(f"뉴스 수집 시작: {RSS_URL}")
        feed = feedparser.parse(RSS_URL)
        
        # 피드가 비어있거나 오류가 있는 경우 체크
        if not feed.entries or feed.entries[0].title == "사용할 수 없는 피드입니다.":
            print("구글 뉴스에서 피드를 가져올 수 없습니다. 키워드를 변경하여 재시도합니다.")
            # 플랜 B: 키워드 단순화
            fallback_query = quote("AI 기술")
            feed = feedparser.parse(f"https://news.google.com/rss/search?q={fallback_query}&hl=ko&gl=KR&ceid=KR:ko")

        news_list = []
        for entry in feed.entries[:12]:
            # 기사 제목에서 언론사 이름 분리 (제목 - 언론사 형태가 많음)
            title = entry.title
            
            summary_clean = clean_html(entry.get("summary", ""))
            summary_short = summary_clean[:100] + "..." if len(summary_clean) > 100 else summary_clean

            news_list.append({
                "title": title,
                "link": entry.link,
                "summary": summary_short,
                "date": datetime.datetime.now().strftime("%Y-%m-%d")
            })
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=4)
        print(f"성공: {len(news_list)}개의 뉴스를 저장했습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump([], f)

if __name__ == "__main__":
    fetch_ai_news()
