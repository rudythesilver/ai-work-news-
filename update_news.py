import feedparser
import json
import datetime
import os
import re

# 훨씬 안정적인 AI 전문지(AI 타임스)의 RSS 주소를 사용합니다.
RSS_URL = "http://www.aitimes.com/rss/all.xml"

def clean_html(raw_html):
    if not raw_html: return ""
    # HTML 태그 및 특수문자 제거
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def fetch_ai_news():
    try:
        print(f"AI 전문 뉴스 수집 시작: {RSS_URL}")
        # 구글과 달리 차단이 적은 일반 RSS 피드를 읽어옵니다.
        feed = feedparser.parse(RSS_URL)
        
        news_list = []
        
        # 최신 뉴스 12개 추출
        for entry in feed.entries[:12]:
            title = entry.title
            link = entry.link
            
            # 요약 내용 깔끔하게 정리
            summary = clean_html(entry.get("description", entry.get("summary", "")))
            summary = summary[:110] + "..." if len(summary) > 110 else summary

            news_list.append({
                "title": title,
                "link": link,
                "summary": summary,
                "date": datetime.datetime.now().strftime("%Y-%m-%d")
            })
        
        # 데이터 저장
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=4)
            
        print(f"성공: {len(news_list)}개의 기사를 저장했습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")
        if not os.path.exists('data.json'):
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump([], f)

if __name__ == "__main__":
    fetch_ai_news()
