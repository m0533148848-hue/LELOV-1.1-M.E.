import streamlit as st
import google.generativeai as genai

# כותרת חגיגית
st.title("הצ'אט שלי עם ג'מיני 3.0 🚀")

# הגדרת המפתח
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("חסר מפתח API. נא להגדיר אותו בהגדרות של Streamlit.")
    st.stop()

# --- כאן השינוי הגדול: שימוש במודל שמצאנו ברשימה ---
model = genai.GenerativeModel('gemini-3-pro-preview')

# שמירת היסטוריית השיחה
if "messages" not in st.session_state:
    st.session_state.messages = []

# הצגת הודעות קודמות
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# תיבת קלט
if prompt := st.chat_input("כתוב משהו למודל החדש..."):
    # הצגת הודעת המשתמש
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # שליחה לגוגל
    try:
        response = model.generate_content(prompt)
        text_response = response.text
        
        # הצגת תשובת הבוט
        with st.chat_message("assistant"):
            st.markdown(text_response)
        st.session_state.messages.append({"role": "assistant", "content": text_response})
    except Exception as e:
        st.error(f"שגיאה: {e}")
