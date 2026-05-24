IMPORTANT_KEYWORDS = [
    "earnings",
    "guidance",
    "AI",
    "SEC",
    "실적",
    "공급계약",
    "반도체",
    "급등",
    "테슬라",
    "엔비디아"
]


def is_significant(stock_data):
    if abs(stock_data["change_pct"]) >= 3:
        return True

    for article in stock_data["news"]:
        title = article.get("title", "")

        for keyword in IMPORTANT_KEYWORDS:
            if keyword.lower() in title.lower():
                return True

    return False