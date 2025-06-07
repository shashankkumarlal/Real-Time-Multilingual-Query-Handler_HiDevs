# 1. Imports and setup
import streamlit as st
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from langdetect import detect
import pandas as pd
from datetime import datetime
import os

# 2. Initialize LLaMA 3 client
GROQ_API_KEY = os.getenv("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")
llm = ChatGroq(
    temperature=0.2,
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-70b-8192"
)

# Supported language codes and names (partial example, extend as needed)
LANGUAGES = {
    "Auto Detect": "auto",
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chichewa": "ny",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Filipino": "tl",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jw",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Kinyarwanda": "rw",
    "Korean": "ko",
    "Kurdish (Kurmanji)": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Nyanja": "ny",
    "Odia (Oriya)": "or",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala (Sinhalese)": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu",

    # Additional Indian languages / dialects (some without official ISO 639-1 but used here):
    "Assamese": "as",
    "Bodo": "brx",
    "Dogri": "doi",
    "Konkani": "kok",
    "Maithili": "mai",
    "Manipuri (Meitei)": "mni",
    "Santhali": "sat",
    "Sindhi": "sd",
    "Tulu": "tcy",
    "Kashmiri": "ks",
    "Nepali (India)": "ne-IN",
    "Bhili/Bhilodi": "bhb",
    "Chhattisgarhi": "hne",
    "Garhwali": "gbm",
    "Haryanvi": "bgc",
    "Khandeshi": "khn",
    "Magahi": "mag",
    "Marwari": "mwr",
    "Mundari": "unr",
    "Angika": "anp",
    "Santali": "sat",
    "Bishnupriya Manipuri": "bpy",

    # Add more dialects or regional Indian languages as needed...
}


# 3. Neon CSS styling
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

# 4. Streamlit App UI and Logic
def main():
    st.set_page_config(page_title="Neon Translator by SHASHANK", page_icon="🌐")
    st.markdown(NEON_STYLE, unsafe_allow_html=True)
    st.title("🌍 Multilingual Customer Query Translator")

    st.markdown(
        """
        Type your customer query in any language. This AI will:
        1. Detect language (if Auto Detect selected)
        2. Translate from input language to output language
        3. Respond in the output language
        4. Log interaction with time
        """
    )

    # Language selection dropdowns with search support
    input_lang_name = st.selectbox(
        "🈯 Select input language (or Auto Detect):",
        options=list(LANGUAGES.keys()),
        index=0,
        help="If Auto Detect is selected, language will be detected automatically."
    )
    output_lang_name = st.selectbox(
        "🈳 Select output language:",
        options=[lang for lang in LANGUAGES.keys() if lang != "Auto Detect"],
        index=0,
        help="Select the language you want to translate and respond in."
    )

    user_query = st.text_area("💬 Enter your customer query:", height=150)

    if user_query.strip():
        # Detect language if Auto Detect selected, else use chosen language
        if input_lang_name == "Auto Detect":
            detected_lang_code = detect(user_query)
            st.write(f"🈶 Detected Input Language: `{detected_lang_code}`")
            input_lang_code = detected_lang_code
        else:
            input_lang_code = LANGUAGES[input_lang_name]
            st.write(f"🈶 Selected Input Language: `{input_lang_code}`")

        output_lang_code = LANGUAGES[output_lang_name]

        with st.spinner("Translating and responding..."):
            try:
                # Translate input query to output language if input != output
                if input_lang_code != output_lang_code:
                    translation_prompt = [
                        SystemMessage(content=f"Translate the following text from {input_lang_name} to {output_lang_name}:"),
                        HumanMessage(content=user_query)
                    ]
                    translated_text = llm.invoke(translation_prompt).content.strip()
                else:
                    # If input and output languages are same, no translation needed
                    translated_text = user_query

                # Generate friendly support reply in output language
                reply_prompt = [
                    SystemMessage(content=f"You're a friendly support AI. Reply to this message in {output_lang_name}."),
                    HumanMessage(content=translated_text)
                ]
                reply_text = llm.invoke(reply_prompt).content.strip()

            except Exception as e:
                st.error(f"Error: {e}")
                return

        st.subheader(f"🔤 Translated Message ({output_lang_name}):")
        st.success(translated_text)

        st.subheader(f"🤖 Support Reply ({output_lang_name}):")
        st.info(reply_text)

        st.markdown("---")
        rating = st.slider("⭐ Rate the translation and reply quality:", 1, 5, 3)
        if rating >= 4:
            st.balloons()
            st.success("Thanks for the great rating! 🚀")

        # Log the query and response
        if "log" not in st.session_state:
            st.session_state.log = []
        st.session_state.log.append({
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Original": user_query,
            "InputLang": input_lang_code,
            "OutputLang": output_lang_code,
            "Translated": translated_text,
            "Reply": reply_text,
            "Rating": rating
        })

        if st.button("📥 Download Log CSV"):
            df = pd.DataFrame(st.session_state.log)
            df.to_csv("translation_log.csv", index=False)
            st.success("Saved as translation_log.csv ✅")

    else:
        st.info("Enter a message to begin translation and support.")

# 5. Run app
if __name__ == "__main__":
    main()
