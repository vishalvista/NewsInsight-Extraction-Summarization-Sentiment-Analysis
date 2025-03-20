import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Replace this with your actual API key
NEWS_API_KEY = "b1928b003f9a48e79fa264b933e7def2"

def fetch_news(company):
    """Fetch latest 10 news articles for a given company."""
    url = f"https://newsapi.org/v2/everything?q={company}&pageSize=10&apiKey={NEWS_API_KEY}"
    response = requests.get(url, timeout=10)
    data = response.json()

    if data.get("status") == "ok":
        articles = data.get("articles", [])[:10]  # Ensure only 10 articles
        with open("extracted_news.json", "w", encoding="utf-8") as file:
            json.dump(articles, file, indent=4, ensure_ascii=False)
        print(f"✅ News extraction completed! {len(articles)} articles saved.")
        return articles
    else:
        print(f"❌ Error: {data.get('message', 'Unknown error')}")
        return []

if __name__ == "__main__":
    company = input("Enter Company Name: ")
    articles = fetch_news(company)
    if not articles:
        print("⚠️ Failed to fetch news. Please check your API key or try another company.")
