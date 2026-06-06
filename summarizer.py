import requests
from config import GEMINI_API_KEY

_GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY
)


def _translate(titles: list[str]) -> list[str]:
    prompt = (
        "다음 영어 뉴스 제목들을 자연스러운 한국어로 번역해줘. "
        "번호와 번역문만 출력하고 다른 설명은 쓰지 마.\n"
        + "\n".join(f"{i+1}. {t}" for i, t in enumerate(titles))
    )
    try:
        resp = requests.post(
            _GEMINI_URL,
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=15,
        )
        resp.raise_for_status()
        text = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        translated = []
        for line in lines:
            # "1. 제목" 형식에서 제목 부분만 추출
            if ". " in line:
                translated.append(line.split(". ", 1)[1])
            else:
                translated.append(line)
        if len(translated) == len(titles):
            return translated
    except Exception:
        pass
    return titles  # 실패 시 원문 반환


def summarize_stock(stock_info):
    ticker = stock_info["ticker"]
    change_pct = float(stock_info["change_pct"])
    direction = "상승" if change_pct > 0 else "하락"

    raw_titles = []
    for article in stock_info["news"][:3]:
        try:
            raw_titles.append(article["content"]["title"])
        except Exception:
            continue

    translated = _translate(raw_titles) if raw_titles else []

    summary = f"📌 {ticker}\n- 전일 대비 {abs(change_pct):.2f}% {direction}\n\n📰 주요 뉴스:\n"
    for title in translated:
        summary += f"- {title}\n"

    return summary
