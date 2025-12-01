import streamlit as st
import google.generativeai as genai

# כותרת האפליקציה
st.title("הצ'אט שלי עם ג'מיני 🤖")

# הגדרת המפתח - מושך אותו מהכספת של סטרימליט
# אם אין מפתח, מציג הודעה
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("חסר מפתח API. נא להגדיר אותו בהגדרות של Streamlit.")
    st.stop()

# בחירת המודל
model = genai.GenerativeModel('gemini-1.5-flash')

# שמירת היסטוריית השיחה בזיכרון
if "messages" not in st.session_state:
    st.session_state.messages = []

# הצגת כל ההודעות הקודמות על המסך
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# תיבת הטקסט למטה - מחכה שהמשתמש יכתוב משהו
if prompt := st.chat_input("הקלידו הודעה כאן..."):
    # 1. מציג את ההודעה של המשתמש
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. שולח לגוגל ומקבל תשובה
    try:
        response = model.generate_content(prompt)
        bot_reply = response.text
        
        # 3. מציג את התשובה של הבוט
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        
    except Exception as e:
        st.error(f"אירעה שגיאה: {e}")
