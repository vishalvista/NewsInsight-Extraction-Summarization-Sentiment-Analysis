import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Ensure VADER lexicon is downloaded
nltk.download("vader_lexicon")

def analyze_sentiment(text):
    """Analyze sentiment using VADER."""
    if not text:
        return 0  # Neutral sentiment if no text is available
    
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)["compound"]
    return sentiment_score  # Returns a value between -1 (negative) and 1 (positive)

def process_news():
    """Load news from extracted_news.json, analyze sentiment, and save results."""
    try:
        with open("extracted_news.json", "r", encoding="utf-8") as file:
            articles = json.load(file)

        if not articles:
            print("[INFO] No articles found in 'extracted_news.json'.")
            return

        processed_articles = []
        for article in articles:
            title = article.get("title", "No Title")
            description = article.get("description", "")
            content = article.get("content", "")

            # Combine available text for sentiment analysis
            full_text = " ".join(filter(None, [title, description, content]))  # Remove None values
            sentiment_score = analyze_sentiment(full_text[:1000])  # Limit analysis to 1000 characters

            processed_articles.append({
                "title": title,
                "sentiment_score": sentiment_score,
                "sentiment": "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral",
                "summary": full_text[:200]  # Shortened summary (first 200 chars)
            })

        with open("processed_news.json", "w", encoding="utf-8") as file:
            json.dump(processed_articles, file, indent=4, ensure_ascii=False)

        print("[SUCCESS] Sentiment analysis completed!")
        print(f"[INFO] {len(processed_articles)} articles saved in 'processed_news.json'.")

    except FileNotFoundError:
        print("[ERROR] 'extracted_news.json' not found. Please run 'news_extraction.py' first.")
    except json.JSONDecodeError:
        print("[ERROR] 'extracted_news.json' contains invalid JSON. Check the file format.")
    except Exception as e:
        print(f"[ERROR] Error processing news: {e}")

if __name__ == "__main__":
    process_news()
