import json
from pathlib import Path
from collector import get_us_stock_data
from summarizer import build_messages
from telegram_sender import send_telegram_message
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "tickers.json", encoding="utf-8") as f:
    tickers = json.load(f)

# 모든 종목 데이터 수집
stocks_data = []
for ticker in tickers["us"]:
    data = get_us_stock_data(ticker)
    print(data)
    stocks_data.append(data)

# 전체 제목을 Gemini 1회 호출로 번역 후 메시지 생성
final_message = "📈 오늘의 주요 종목 브리핑\n\n"
try:
    final_message += build_messages(stocks_data)
except Exception as e:
    print("요약 오류:", e)

send_telegram_message(
    token=TELEGRAM_TOKEN,
    chat_id=TELEGRAM_CHAT_ID,
    text=final_message,
)
