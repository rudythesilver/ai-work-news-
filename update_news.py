import feedparser
import json
import datetime
import os
import re

# 뉴스 검색 키워드: AI 업무 활용
RSS_URL = "https://news.google.com/rss/search?q=AI+업무+활용+언어:ko&hl=ko&gl=KR&ceid=KR:ko"

def clean_html(raw_html):
    """HTML 태그를 제거하고 순수 텍스트만 남깁니다."""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def fetch_ai_news():
    try:
        print("뉴스 수집 시작...")
        feed = feedparser.parse(RSS_URL)
        news_list = []

        for entry in feed.entries[:10]:
            # 요약 내용에서 HTML 태그 제거
            summary_clean = clean_html(entry.summary)
            # 너무 길면 자르기
            summary_short = summary_clean[:120] + "..." if len(summary_clean) > 120 else summary_clean

            news_list.append({
                "title": entry.title,
                "link": entry.link,
                "summary": summary_short,
                "date": datetime.datetime.now().strftime("%Y-%m-%d")
            })
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=4)
        print(f"성공: {len(news_list)}개의 뉴스를 저장했습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")
        if not os.path.exists('data.json'):
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump([], f)

if __name__ == "__main__":
    fetch_ai_news()
