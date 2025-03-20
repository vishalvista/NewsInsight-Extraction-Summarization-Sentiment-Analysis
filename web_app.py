import streamlit as st
import subprocess
import json
from gtts import gTTS
import os
import time

# Custom CSS for styling
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #4A90E2;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #6C757D;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            border: 2px solid #4A90E2;
            padding: 10px;
        }
        .stButton>button {
            border-radius: 20px;
            background: linear-gradient(to right, #4A90E2, #8E44AD);
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            width: 100%;
        }
        .stAlert {
            border-radius: 10px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Function to convert text to speech in Hindi
def text_to_speech(text, filename="news_audio.mp3", lang="hi"):
    """Convert given text to speech in Hindi and return the audio file path."""
    if not text.strip():
        return None
    
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        return filename
    except Exception as e:
        st.error(f"Error in text-to-speech: {e}")
        return None

# Streamlit UI
st.markdown("<h1 class='title'>📰 NewsInsight: Extraction, Summarization & Sentiment Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Analyze recent news articles and their sentiments in an interactive way.</p>", unsafe_allow_html=True)

# User input
company_name = st.text_input("Enter Company Name:")

if st.button("🔍 Fetch & Analyze News"):
    if company_name:
        with st.spinner("Fetching latest news..."):
            try:
                process = subprocess.Popen(["python", "news_extraction.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate(input=company_name)
                
                if process.returncode == 0:
                    st.success("✅ News extraction completed!")
                else:
                    st.error("❌ Failed to fetch news.")
                    st.text(stderr)
                    st.stop()
            
            except Exception as e:
                st.error(f"Unexpected error: {e}")
                st.stop()

        with st.spinner("Analyzing sentiment..."):
            result = subprocess.run(["python", "sentiment_analysis.py"], capture_output=True, text=True)
            if result.returncode == 0:
                st.success("✅ Sentiment analysis completed!")
            else:
                st.error("❌ Sentiment analysis failed.")
                st.text(result.stderr)
                st.stop()

        if os.path.exists("processed_news.json"):
            with open("processed_news.json", "r", encoding="utf-8") as file:
                articles = json.load(file)

            if articles:
                st.subheader("📑 Processed News Articles")
                for idx, article in enumerate(articles[:10], 1):
                    with st.expander(f"🔹 {article.get('title', 'No Title')}"):
                        st.write(f"📝 **Summary:** {article.get('summary', 'No summary available.')}")
                        st.write(f"📊 **Sentiment:** {article.get('sentiment', 'Unknown')} ({article.get('sentiment_score', 0):.2f})")
                        hindi_text = f"शीर्षक: {article.get('title', 'कोई शीर्षक नहीं')}. सारांश: {article.get('summary', 'कोई सारांश नहीं')[:200]}"
                        audio_filename = f"news_audio_{idx}.mp3"
                        audio_file = text_to_speech(hindi_text, filename=audio_filename)
                        if audio_file:
                            st.audio(audio_file, format="audio/mp3", start_time=0)
            else:
                st.warning("⚠ No processed news available.")
        else:
            st.error("❌ Processed news file not found. Please run sentiment analysis again.")
    else:
        st.error("⚠ Please enter a company name before proceeding.")
