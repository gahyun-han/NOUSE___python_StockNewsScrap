import requests
from config import GEMINI_API_KEY

_GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent?key=" + GEMINI_API_KEY
)


def _translate(titles: list[str]) -> list[str]:
    if not titles:
        return titles
    prompt = (
        "다음 영어 뉴스 제목들을 자연스러운 한국어로 번역해줘. "
        "반드시 번호와 번역문만 출력하고 설명, 원문, 주석은 절대 쓰지 마.\n"
        "예시:\n1. 번역된 제목\n2. 번역된 제목\n\n"
        + "\n".join(f"{i+1}. {t}" for i, t in enumerate(titles))
    )
    try:
        resp = requests.post(
            _GEMINI_URL,
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=30,
        )
        resp.raise_for_status()
        text = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        print(f"[번역 응답]\n{text}\n")
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        translated = []
        for line in lines:
            if ". " in line:
                translated.append(line.split(". ", 1)[1])
            else:
                translated.append(line)
        print(f"[번역 결과] 기대={len(titles)}개, 수신={len(translated)}개")
        if len(translated) == len(titles):
            return translated
        # 개수 불일치 → 최대한 맞춰서 사용 (부족하면 원문으로 채움)
        result = list(titles)
        for i, t in enumerate(translated[:len(titles)]):
            result[i] = t
        return result
    except Exception as e:
        print(f"[번역 오류] {e}")
    return titles


def build_messages(stocks_data: list[dict]) -> str:
    """모든 종목 제목을 한 번에 번역 후 메시지 생성."""
    # 종목별 제목 수집
    per_stock = []
    for stock_info in stocks_data:
        raw_titles = []
        for article in stock_info.get("news", [])[:3]:
            try:
                raw_titles.append(article["content"]["title"])
            except Exception:
                continue
        per_stock.append((stock_info, raw_titles))

    # 전체 제목을 한 번에 번역
    all_titles = [t for _, titles in per_stock for t in titles]
    all_translated = _translate(all_titles)

    # 번역 결과를 종목별로 재분배
    idx = 0
    message = ""
    for stock_info, raw_titles in per_stock:
        n = len(raw_titles)
        translated = all_translated[idx:idx + n]
        idx += n

        ticker = stock_info["ticker"]
        raw_pct = stock_info.get("change_pct")
        if raw_pct is None:
            pct_str = "전일 데이터 없음"
        else:
            change_pct = float(raw_pct)
            direction = "상승" if change_pct > 0 else "하락"
            pct_str = f"전일 대비 {abs(change_pct):.2f}% {direction}"

        message += f"📌 {ticker}\n- {pct_str}\n\n📰 주요 뉴스:\n"
        for title in translated:
            message += f"- {title}\n"
        message += "\n"

    return message


# 단일 종목용 (하위 호환)
def summarize_stock(stock_info: dict) -> str:
    return build_messages([stock_info])
