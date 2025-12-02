import streamlit as st
import google.generativeai as genai

# כותרת האפליקציה
st.title("הצ'אט שלי עם ג'מיני ⚡")

# הגדרת המפתח - מושך אותו מהכספת של סטרימליט
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("חסר מפתח API. נא להגדיר אותו בהגדרות של Streamlit.")
    st.stop()

# --- הגדרת המודל: שימוש במודל היציב והחינמי ביותר ---
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"שגיאה בטעינת המודל: {e}")
    st.stop()

# שמירת היסטוריית השיחה בזיכרון
if "messages" not in st.session_state:
    st.session_state.messages = []

# הצגת כל ההודעות הקודמות על המסך
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# תיבת הטקסט למטה
if prompt := st.chat_input("הקלידו הודעה כאן..."):
    # 1. הצגת הודעת המשתמש
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. שליחה לגוגל
    try:
        response = model.generate_content(prompt)
        bot_reply = response.text
        
        # 3. הצגת תשובת הבוט
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        
    except Exception as e:
        # הצגת שגיאה ברורה אם משהו משתבש
        st.error(f"אירעה תקלה: {e}")
