import yfinance as yf
import feedparser
#from pykrx import stock
from datetime import datetime, timedelta

def get_us_stock_data(ticker):
    stock = yf.Ticker(ticker)

    hist = stock.history(period="2d")

    if len(hist) < 2:
        return None

    prev_close = hist.iloc[-2]["Close"]
    last_close = hist.iloc[-1]["Close"]

    change_pct = ((last_close - prev_close) / prev_close) * 100

    news = stock.news

    return {
        "ticker": ticker,
        "change_pct": round(change_pct, 2),
        "news": news[:5]
    }


#def get_kr_stock_data(ticker):
#    today = datetime.today()
#    yesterday = today - timedelta(days=1)
#    df = stock.get_market_ohlcv_by_date(
#        yesterday.strftime("%Y%m%d"),
#        today.strftime("%Y%m%d"),
#        ticker
#    )
#    return df




def fetch_news(keyword):
    url = f"https://news.google.com/rss/search?q={keyword}"

    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries[:5]:
        articles.append({
            "title": entry.title,
            "link": entry.link
        })

    return articles