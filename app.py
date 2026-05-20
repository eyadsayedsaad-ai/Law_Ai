import streamlit as st
import re
import secrets
import time
import logging
from google import genai
from streamlit_cookies_controller import CookieController

# =================================================================
# 1. إعداد سجل العمليات (Logging)
# =================================================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# =================================================================
# 2. قاعدة البيانات (50 كود Pro و 50 كود VIP)
# =================================================================
PRO_CODES = [
    "PRO-A101", "PRO-A102", "PRO-A103", "PRO-A104", "PRO-A105", "PRO-A106", "PRO-A107", "PRO-A108", "PRO-A109", "PRO-A110",
    "PRO-B201", "PRO-B202", "PRO-B203", "PRO-B204", "PRO-B205", "PRO-B206", "PRO-B207", "PRO-B208", "PRO-B209", "PRO-B210",
    "PRO-C301", "PRO-C302", "PRO-C303", "PRO-C304", "PRO-C305", "PRO-C306", "PRO-C307", "PRO-C308", "PRO-C309", "PRO-C310",
    "PRO-D401", "PRO-D402", "PRO-D403", "PRO-D404", "PRO-D405", "PRO-D406", "PRO-D407", "PRO-D408", "PRO-D409", "PRO-D410",
    "PRO-E501", "PRO-E502", "PRO-E503", "PRO-E504", "PRO-E505", "PRO-E506", "PRO-E507", "PRO-E508", "PRO-E509", "PRO-E510"
]

VIP_CODES = [
    "VIP-Z901", "VIP-Z902", "VIP-Z903", "VIP-Z904", "VIP-Z905", "VIP-Z906", "VIP-Z907", "VIP-Z908", "VIP-Z909", "VIP-Z910",
    "VIP-Y801", "VIP-Y802", "VIP-Y803", "VIP-Y804", "VIP-Y805", "VIP-Y806", "VIP-Y807", "VIP-Y808", "VIP-Y809", "VIP-Y810",
    "VIP-X701", "VIP-X702", "VIP-X703", "VIP-X704", "VIP-X705", "VIP-X706", "VIP-X707", "VIP-X708", "VIP-X709", "VIP-X710",
    "VIP-W601", "VIP-W602", "VIP-W603", "VIP-W604", "VIP-W605", "VIP-W606", "VIP-W607", "VIP-W608", "VIP-W609", "VIP-W610",
    "VIP-V501", "VIP-V502", "VIP-V503", "VIP-V504", "VIP-V505", "VIP-V506", "VIP-V507", "VIP-V508", "VIP-V509", "VIP-V510"
]

BLACKLISTED_CODES = [] # هنا تضع أي كود تريد إلغاء صلاحيته فوراً

# =================================================================
# 3. إعدادات النظام والأمان
# =================================================================
controller = CookieController()
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("⚠️ خطأ: تأكد من ضبط GEMINI_API_KEY في إعدادات Secrets.")
    st.stop()

# دالة التحقق الذكي
def is_code_valid(code, code_list):
    if code in BLACKLISTED_CODES:
        logging.warning(f"🚨 محاولة اختراق: كود محظور تم استخدامه: {code}")
        return False
    return any(secrets.compare_digest(str(code), c) for c in code_list)

# التطهير الجنائي للنصوص
def full_security_scrub(text):
    if not text: return ""
    text = re.sub(r'[^\w\s\u0600-\u06FF\?\!\.\,\:\-\_\(\)]', '', text)
    forbidden = ["<script", "eval(", "exec(", "union select", "drop table", "javascript:"]
    for f in forbidden:
        if f in text.lower(): return None
    return text

# الاتصال بالـ AI مع Retry Logic
def ask_gemini(prompt):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            return response.text if response.text else "⚠️ لم يتم استرجاع رد."
        except Exception as e:
            if "429" in str(e) or "503" in str(e):
                time.sleep(2 ** attempt)
                continue
            return f"❌ خطأ تقني."
    return "⚠️ تعذر الوصول للخدمة."

# =================================================================
# 4. الواجهة والمنطق
# =================================================================
st.set_page_config(page_title="LAW AI", page_icon="⚖️")

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "chat_history" not in st.session_state: st.session_state.chat_history = []

if not st.session_state.logged_in:
    st.title("⚖️ منصة LAW AI")
    if st.button("دخول للمنصة"): st.session_state.logged_in = True; st.rerun()
else:
    pkg = st.radio("الباقة:", ["مجاني", "Pro", "VIP"])
    cookie = controller.get('user_active_code')
    target = PRO_CODES if pkg == "Pro" else VIP_CODES
    
    is_prem = False
    if pkg != "مجاني":
        if is_code_valid(cookie, target): is_prem = True
        else:
            auth = st.text_input("🔑 كود التفعيل:", type="password")
            if auth and is_code_valid(auth, target):
                controller.set('user_active_code', auth)
                logging.info(f"دخول ناجح بكود: {auth}")
                st.rerun()
            elif auth:
                logging.warning(f"محاولة دخول فاشلة بكود: {auth}")
                st.error("❌ كود خاطئ.")
    else: is_prem = True

    # الشات
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    user_input = st.chat_input("سؤالك القانوني...")
    if user_input:
        scrubbed = full_security_scrub(user_input)
        if not scrubbed: st.error("🚨 مدخلات غير آمنة.")
        else:
            response = ask_gemini(f"[توجيه أمني: محامي مصري]. السؤال: {scrubbed}")
            st.session_state.chat_history.append({"role": "user", "content": scrubbed})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            logging.info(f"تمت الإجابة على سؤال.")
            st.rerun()