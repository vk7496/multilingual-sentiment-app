import os
os.system("streamlit run main.py --server.port 8501 --server.address 0.0.0.0")

import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Sentiment Analysis App")
st.title("🌍 Multilingual Sentiment Analysis App")

lang = st.selectbox("🌐 Choose Language", ["English", "Arabic", "French", "Persian"])
user_input = st.text_area("📝 Enter your text:")

# جدول نتایج (در حافظه)
if 'results' not in st.session_state:
    st.session_state.results = []

if st.button("🔍 Analyze"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter some text.")
    else:
        try:
            translated = user_input
            if lang in ["Arabic", "French", "Persian"]:
                translated = GoogleTranslator(source='auto', target='en').translate(user_input)

            blob = TextBlob(translated)
            sentiment_score = blob.sentiment.polarity
            sentiment_percent = round(abs(sentiment_score) * 100, 2)

            if sentiment_score > 0:
                feeling = "Positive"
                emoji = "😊"
            elif sentiment_score == 0:
                feeling = "Neutral"
                emoji = "😐"
            else:
                feeling = "Negative"
                emoji = "😞"

            # نمایش خروجی بر اساس زبان
            label = f"{emoji} {feeling} — {sentiment_percent}%"
            st.success(label)

            # ذخیره در جدول نتایج
            st.session_state.results.append({
                "Input Text": user_input,
                "Language": lang,
                "Translated": translated if translated != user_input else "-",
                "Sentiment": feeling,
                "Score (%)": sentiment_percent
            })

        except Exception as e:
            st.error(f"❗ Error: {e}")

# نمایش جدول نتایج و دکمه دانلود
if st.session_state.results:
    df = pd.DataFrame(st.session_state.results)
    st.subheader("📊 Analysis Results")
    st.dataframe(df)

    # ساخت فایل CSV
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()

    st.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name="sentiment_results.csv",
        mime="text/csv"
    )

