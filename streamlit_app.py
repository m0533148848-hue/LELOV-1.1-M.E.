import streamlit as st
import google.generativeai as genai

st.title("בדיקת מודלים זמינים 🕵️‍♂️")

# התחברות
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    st.write("הנה המודלים שגוגל נותן לנו להשתמש בהם כרגע:")
    
    try:
        # לולאה שעוברת על כל המודלים ומדפיסה את השמות שלהם
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                st.code(m.name)
    except Exception as e:
        st.error(f"שגיאה בשליפת המודלים: {e}")
else:
    st.error("חסר מפתח API")
