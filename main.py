#@title 🚀 Neon Multilingual AI Translator by SHASHANK

# 1. Install dependencies
#!pip install --quiet streamlit langchain langchain_groq langdetect

# 2. Imports and setup
import streamlit as st
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from langdetect import detect
import pandas as pd
from datetime import datetime

# 3. Initialize LLaMA 3 client
import os
GROQ_API_KEY = os.getenv("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")
llm = ChatGroq(
    temperature=0.2,
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-70b-8192"
)

# 4. Neon CSS styling
NEON_STYLE = """
<style>
body {
    background-color: #0f0f0f;
    color: #39ff14;
    font-family: 'Courier New', monospace;
}
section.main > div {
    background-color: #111;
    border: 2px solid #39ff14;
    border-radius: 10px;
    padding: 20px;
}
input, textarea {
    background-color: #000;
    color: #39ff14;
    border: 1px solid #39ff14;
}
</style>
"""

# 5. Streamlit App UI and Logic
def main():
    st.set_page_config(page_title="Neon Translator by SHASHANK", page_icon="🌐")
    st.markdown(NEON_STYLE, unsafe_allow_html=True)
    st.title("🌍 Multilingual Customer Query Translator")
    st.markdown(
        """
        Type your customer query in any language. This AI will:
        1. Detect language
        2. Translate to English
        3. Respond in original language
        4. Log interaction with time
        """
    )

    user_query = st.text_area("💬 Enter your customer query (any language):", height=150)

    if user_query.strip():
        detected_lang = detect(user_query)
        st.write(f"🈶 Detected Language: `{detected_lang}`")

        with st.spinner("Translating and responding..."):
            try:
                # English translation
                translation_prompt = [
                    SystemMessage(content="Translate the following into clear English only."),
                    HumanMessage(content=user_query)
                ]
                english_response = llm.invoke(translation_prompt).content.strip()

                # Friendly AI reply (English)
                reply_prompt = [
                    SystemMessage(content="You're a friendly support AI. Reply to this message in English."),
                    HumanMessage(content=english_response)
                ]
                english_reply = llm.invoke(reply_prompt).content.strip()

                # Translate back to original language
                back_translation_prompt = [
                    SystemMessage(content=f"Translate this English reply back to {detected_lang} as naturally as possible:"),
                    HumanMessage(content=english_reply)
                ]
                translated_reply = llm.invoke(back_translation_prompt).content.strip()

            except Exception as e:
                st.error(f"Error: {e}")
                return

        st.subheader("🔤 Translated Message (English):")
        st.success(english_response)

        st.subheader("🤖 Support Reply (original language):")
        st.info(translated_reply)

        st.markdown("---")
        rating = st.slider("⭐ Rate the translation accuracy:", 1, 5, 3)
        if rating >= 4:
            st.balloons()
            st.success("Thanks for the great rating! 🚀")

        # Log the query
        if "log" not in st.session_state:
            st.session_state.log = []
        st.session_state.log.append({
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Original": user_query,
            "DetectedLang": detected_lang,
            "Translated": english_response,
            "Reply": translated_reply,
            "Rating": rating
        })

        if st.button("📥 Download Log CSV"):
            df = pd.DataFrame(st.session_state.log)
            df.to_csv("translation_log.csv", index=False)
            st.success("Saved as translation_log.csv ✅")

    else:
        st.info("Enter a message to begin translation and support.")

# 6. Run app
if __name__ == "__main__":
    main()
#!pip install streamlit langchain langchain_groq
#!npm install -g localtunnel
#!curl https://loca.lt/mytunnelpassword
#!streamlit run app.py & npx localtunnel --port 8501
