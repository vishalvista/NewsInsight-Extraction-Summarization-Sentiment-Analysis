import json
from gtts import gTTS
import os

def text_to_speech(text, filename="news_audio.mp3"):
    """Convert text to speech in Hindi and save as an audio file."""
    if not text.strip():
        print("⚠️ No text provided for speech conversion.")
        return
    
    try:
        tts = gTTS(text, lang="hi")
        tts.save(filename)
        print(f"✅ Speech saved as '{filename}'")
    except Exception as e:
        print(f"❌ Error generating speech: {e}")

def generate_speech_from_news():
    """Load processed news and generate Hindi speech."""
    try:
        with open("processed_news.json", "r", encoding="utf-8") as f:
            articles = json.load(f)

        if not articles:
            print("⚠️ No articles found in 'processed_news.json'.")
            return

        # Combine news summaries for speech
        speech_text = "\n\n".join([
            f"समाचार: {article.get('title', 'कोई शीर्षक नहीं')} - {article.get('summary', 'कोई सारांश नहीं')}"
            for article in articles
        ])

        # Ensure text is not too long for TTS
        max_length = 4000  # Limit based on gTTS processing constraints
        if len(speech_text) > max_length:
            speech_text = speech_text[:max_length]  # Truncate long text

        text_to_speech(speech_text, "news_audio.mp3")

    except FileNotFoundError:
        print("❌ Error: 'processed_news.json' not found. Please run sentiment analysis first.")
    except json.JSONDecodeError:
        print("❌ Error: 'processed_news.json' contains invalid JSON.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    generate_speech_from_news()
