# Streamlit imports
import streamlit as st
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from langdetect import detect
import pandas as pd
from datetime import datetime
import os

# Check for API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.set_page_config(page_title="Neon Translator Error", page_icon="🚫")
    st.error("🚨 GROQ_API_KEY not found. Please add it in Streamlit Cloud: Manage App > Secrets.")
    st.stop()

llm = ChatGroq(
    temperature=0.2,
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-70b-8192"
)

# Language options
LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Arabic": "ar",
    "Bengali": "bn",
    "Marathi": "mr",
    "Tamil": "ta",
    "Telugu": "te",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa",
    "Odia (Oriya)": "or",
    "Urdu": "ur",
    "Assamese": "as",
    "Maithili": "mai",
    "Sanskrit": "sa",
    "Nepali": "ne",
    "Santali": "sat",
    "Konkani": "kok",
    "Tulu": "tcy",
    # Add more as needed...
}

# Neon style
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
input, textarea, select {
    background-color: #000;
    color: #39ff14;
    border: 1px solid #39ff14;
}
</style>
"""

# Main app logic
def main():
    st.set_page_config(page_title="Neon Translator by SHASHANK", page_icon="🌐")
    st.markdown(NEON_STYLE, unsafe_allow_html=True)
    st.title("🌍 Multilingual Customer Query Translator")

    st.markdown(
        """
        1. Translate query to English (if needed)  
        2. Generate AI response  
        3. Translate response to output language  
        4. Show only final output to user  
        """
    )

    input_lang_name = st.selectbox("🈯 Input Language (or Auto Detect):", list(LANGUAGES.keys()), index=0)
    output_lang_name = st.selectbox("🈳 Output Language:", [lang for lang in LANGUAGES.keys() if lang != "Auto Detect"])
    user_query = st.text_area("📝 Enter customer query:")
    submit = st.button("🌐 Translate & Respond")

    if submit and user_query.strip():
        input_lang_code = LANGUAGES[input_lang_name]
        output_lang_code = LANGUAGES[output_lang_name]

        # Auto-detect language
        if input_lang_code == "auto":
            try:
                input_lang_code = detect(user_query)
                st.info(f"🌍 Detected language code: `{input_lang_code}`")
            except:
                st.error("Language detection failed.")
                return

        # Step 1: Translate to English
        translation_prompt = f"Translate this from {input_lang_name} to English:\n\n{user_query}"
        english_text = llm.invoke([HumanMessage(content=translation_prompt)]).content.strip()

        # Step 2: Get AI response in English
        response_prompt = f"This is a customer support query: \"{english_text}\". Respond politely and helpfully in English."
        response_in_english = llm.invoke([HumanMessage(content=response_prompt)]).content.strip()

        # Step 3: Translate to target language
        final_translation_prompt = f"Translate the following from English to {output_lang_name}:\n\n{response_in_english}"
        translated_response = llm.invoke([HumanMessage(content=final_translation_prompt)]).content.strip()

        # ✅ Show only final translated response
        st.success(f"🌐 {output_lang_name} Response:")
        st.markdown(translated_response)

        # 📁 Log data
        log_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "input_lang": input_lang_name,
            "output_lang": output_lang_name,
            "user_query": user_query,
            "detected_input": english_text,
            "response_english": response_in_english,
            "response_translated": translated_response
        }
        log_df = pd.DataFrame([log_data])
        log_file = "query_log.csv"

        if os.path.exists(log_file):
            existing_df = pd.read_csv(log_file)
            log_df = pd.concat([existing_df, log_df], ignore_index=True)

        log_df.to_csv(log_file, index=False)

if __name__ == "__main__":
    main()
