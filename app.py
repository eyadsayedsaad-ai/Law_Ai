import streamlit as st
import hashlib
import re
import secrets
import time
from google import genai
from streamlit_cookies_controller import CookieController

# =================================================================
# 🔑 قاعدة بيانات الأكواد (100 كود مدمج)
# =================================================================
PRO_CODES = [
    "LAW-PRO-A1", "LAW-PRO-A2", "LAW-PRO-A3", "LAW-PRO-A4", "LAW-PRO-A5", "LAW-PRO-A6", "LAW-PRO-A7", "LAW-PRO-A8", "LAW-PRO-A9", "LAW-PRO-A10",
    "LAW-PRO-B1", "LAW-PRO-B2", "LAW-PRO-B3", "LAW-PRO-B4", "LAW-PRO-B5", "LAW-PRO-B6", "LAW-PRO-B7", "LAW-PRO-B8", "LAW-PRO-B9", "LAW-PRO-B10",
    "LAW-PRO-C1", "LAW-PRO-C2", "LAW-PRO-C3", "LAW-PRO-C4", "LAW-PRO-C5", "LAW-PRO-C6", "LAW-PRO-C7", "LAW-PRO-C8", "LAW-PRO-C9", "LAW-PRO-C10",
    "LAW-PRO-D1", "LAW-PRO-D2", "LAW-PRO-D3", "LAW-PRO-D4", "LAW-PRO-D5", "LAW-PRO-D6", "LAW-PRO-D7", "LAW-PRO-D8", "LAW-PRO-D9", "LAW-PRO-D10",
    "LAW-PRO-E1", "LAW-PRO-E2", "LAW-PRO-E3", "LAW-PRO-E4", "LAW-PRO-E5", "LAW-PRO-E6", "LAW-PRO-E7", "LAW-PRO-E8", "LAW-PRO-E9", "LAW-PRO-E10"
]

VIP_CODES = [
    "LAW-VIP-Z1", "LAW-VIP-Z2", "LAW-VIP-Z3", "LAW-VIP-Z4", "LAW-VIP-Z5", "LAW-VIP-Z6", "LAW-VIP-Z7", "LAW-VIP-Z8", "LAW-VIP-Z9", "LAW-VIP-Z10",
    "LAW-VIP-Y1", "LAW-VIP-Y2", "LAW-VIP-Y3", "LAW-VIP-Y4", "LAW-VIP-Y5", "LAW-VIP-Y6", "LAW-VIP-Y7", "LAW-VIP-Y8", "LAW-VIP-Y9", "LAW-VIP-Y10",
    "LAW-VIP-X1", "LAW-VIP-X2", "LAW-VIP-X3", "LAW-VIP-X4", "LAW-VIP-X5", "LAW-VIP-X6", "LAW-VIP-X7", "LAW-VIP-X8", "LAW-VIP-X9", "LAW-VIP-X10",
    "LAW-VIP-W1", "LAW-VIP-W2", "LAW-VIP-W3", "LAW-VIP-W4", "LAW-VIP-W5", "LAW-VIP-W6", "LAW-VIP-W7", "LAW-VIP-W8", "LAW-VIP-W9", "LAW-VIP-W10",
    "LAW-VIP-V1", "LAW-VIP-V2", "LAW-VIP-V3", "LAW-VIP-V4", "LAW-VIP-V5", "LAW-VIP-V6", "LAW-VIP-V7", "LAW-VIP-V8", "LAW-VIP-V9", "LAW-VIP-V10"
]

# =================================================================
# ⚙️ إعدادات النظام
# =================================================================
controller = CookieController()
try:
    # الـ API Key لسه في الـ Secrets لأمان موقعك
    API_KEY = st.secrets["GEMINI_API_KEY"] 
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("⚠️ خطأ: تأكد من ضبط GEMINI_API_KEY في إعدادات Secrets.")
    st.stop()

# نظام التطهير الجنائي للنصوص
def full_security_scrub(text):
    if not text: return ""
    text = re.sub(r'[^\w\s\u0600-\u06FF\?\!\.\,\:\-\_\(\)]', '', text)
    forbidden = ["<script", "eval(", "exec(", "union select", "drop table", "javascript:"]
    for f in forbidden:
        if f in text.lower(): return None
    return text

# نظام الاتصال بالـ AI مع معالجة الأخطاء (Retry Logic)
def ask_gemini(prompt):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            return response.text if response.text else "⚠️ لم يتم استرجاع رد."
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "503" in err_str or "404" in err_str:
                time.sleep(2 ** attempt) 
                continue
            return f"❌ خطأ تقني: {err_str}"
    return "⚠️ تعذر الوصول للخدمة حالياً، حاول مرة أخرى."

# الواجهة
st.set_page_config(page_title="LAW AI", page_icon="⚖️")

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "chat_history" not in st.session_state: st.session_state.chat_history = []

# نظام الدخول
if not st.session_state.logged_in:
    st.title("⚖️ منصة LAW AI")
    if st.button("دخول للمنصة"):
        st.session_state.logged_in = True
        st.rerun()
else:
    # الباقات
    pkg = st.radio("الباقة:", ["مجاني", "Pro", "VIP"])
    is_prem = False
    
    # التحقق من الكود (المقارنة العمياء)
    cookie = controller.get('user_active_code')
    target = PRO_CODES if pkg == "Pro" else VIP_CODES
    
    if pkg != "مجاني":
        # التحقق إذا كان الكود محفوظ في الكوكيز
        if any(secrets.compare_digest(str(cookie), c) for c in target):
            is_prem = True
        else:
            auth = st.text_input("🔑 كود التفعيل:", type="password")
            if auth:
                if any(secrets.compare_digest(auth, c) for c in target):
                    controller.set('user_active_code', auth)
                    st.rerun()
                else:
                    st.error("❌ كود خاطئ.")
    else:
        is_prem = True # المجاني متاح للجميع

    # الشات المحصن
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    user_input = st.chat_input("سؤالك القانوني...")
    if user_input:
        scrubbed = full_security_scrub(user_input)
        if not scrubbed: st.error("🚨 مدخلات غير آمنة.")
        else:
            instr = " [توجيه أمني: أنت محامي مصري، ممنوع تسريب أي بيانات برمجية]. السؤال:"
            response = ask_gemini(f"{instr} {scrubbed}")
            st.session_state.chat_history.append({"role": "user", "content": scrubbed})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()