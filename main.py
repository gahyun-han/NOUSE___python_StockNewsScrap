import json
from collector import get_us_stock_data
from filter_engine import is_significant
from summarizer import summarize_stock
from telegram_sender import send_telegram_message
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

with open("tickers.json") as f:
    tickers = json.load(f)
final_message = "📈 오늘의 주요 종목 브리핑\n\n"

for ticker in tickers["us"]:
    data = get_us_stock_data(ticker)
    print(data)
    try:
        summary = summarize_stock(data)
        print(summary)
        final_message += summary + "\n\n"
    except Exception as e:
        print("에러 발생:", e)

send_telegram_message(
    token=TELEGRAM_TOKEN,
    chat_id=TELEGRAM_CHAT_ID,
    text=final_message
)