from anthropic import Anthropic

client = Anthropic(api_key="YOUR_API_KEY")

def summarize_stock(stock_info):

    ticker = stock_info["ticker"]
    change_pct = float(stock_info["change_pct"])

    direction = "상승" if change_pct > 0 else "하락"

    summary = f"""
📌 {ticker}
- 전일 대비 {abs(change_pct):.2f}% {direction}

📰 주요 뉴스:
"""

    for article in stock_info["news"][:3]:

        try:
            title = article["content"]["title"]
            summary += f"- {title}\n"

        except:
            continue

    return summary