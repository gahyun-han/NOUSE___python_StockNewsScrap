import json
from pathlib import Path
from collector import get_us_stock_data
from summarizer import build_messages
from telegram_sender import send_telegram_message
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

BASE_DIR = Path(__file__).resolve().parent

# /list 관심종목과 항상 동기화 — UserCustomStockinfo_agent의 watchlist를 우선 사용
_WATCHLIST_PATH = BASE_DIR.parent / "UserCustomStockinfo_agent" / "user_watchlist.json"
_TICKERS_PATH = BASE_DIR / "tickers.json"

if _WATCHLIST_PATH.exists():
    with open(_WATCHLIST_PATH, encoding="utf-8") as f:
        watchlist_data = json.load(f)
    # watchlist는 {chat_id: [ticker, ...]} 구조 — 전체 종목 합집합 사용
    us_tickers = []
    for tickers_list in watchlist_data.values():
        for t in tickers_list:
            if t not in us_tickers:
                us_tickers.append(t)
else:
    with open(_TICKERS_PATH, encoding="utf-8") as f:
        us_tickers = json.load(f).get("us", [])

# 모든 종목 데이터 수집
stocks_data = []
for ticker in us_tickers:
    data = get_us_stock_data(ticker)
    print(data)
    stocks_data.append(data)

# 전체 제목을 Gemini 1회 호출로 번역 후 메시지 생성
final_message = "📈 오늘의 주요 종목 브리핑\n\n"
try:
    final_message += build_messages(stocks_data)
except Exception as e:
    print("요약 오류:", e)
    final_message += f"⚠️ 요약 생성 중 오류 발생: {e}"

send_telegram_message(
    token=TELEGRAM_TOKEN,
    chat_id=TELEGRAM_CHAT_ID,
    text=final_message,
)
