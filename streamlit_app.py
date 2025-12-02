import streamlit as st
import google.generativeai as genai

# כותרת המערכת
st.title("מערכת ניהול הנתונים שלי 📊")

# חיבור למפתח
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("חסר מפתח API")
    st.stop()

# --- כאן הקסם: הגדרת המוח של המערכת ---
# העתיקו לפה את ההוראות המדויקות שכתבתם ב-AI Studio
system_instruction = """
אתה מנהל מערכת נתונים מומחה.
התפקיד שלך הוא: [כאן תדביקו את ההוראות שלכם]
הנתונים שיש לך הם: [כאן תדביקו את הנתונים או החוקים]
אסור לך לחרוג מההוראות האלו.
"""

# הגדרת המודל עם ההוראות המיוחדות
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=system_instruction
)

# ממשק המשתמש
if "messages" not in st.session_state:
    st.session_state.messages = []

# הצגת היסטוריה
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# קלט
if prompt := st.chat_input("הכנס נתונים או בקשה..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # שליחה למודל (שעכשיו יודע את ההוראות שלכם)
        response = model.generate_content(prompt)
        st.chat_message("assistant").markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"שגיאה: {e}")
