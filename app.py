# ==============================================================================
# 🌟 منصة LAW AI - النسخة الذهبية (النهائية والمستقرة 100%)
# 🌟 المبرمج الرئيسي: البطل أنس
# 🌟 الوصف: مستشار قانوني كامل، نظام باقات بأكواد، حماية Spam، تصميم فخم
# ==============================================================================

import streamlit as st
import google.generativeai as genai
import datetime
import re

# ==============================================================================
# 1. إعدادات الصفحة والتصميم الملكي
# ==============================================================================
st.set_page_config(page_title="LAW AI | المستشار الرقمي", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .stApp { background-color: #050a1f; color: #e0e1dd; font-family: 'Cairo', sans-serif; }
    h1, h2, h3 { text-align: center; color: #d4af37 !important; font-weight: 900; text-shadow: 0px 4px 15px rgba(212, 175, 55, 0.3); }
    .ai-bubble { background: linear-gradient(145deg, #1a1105, #2a1b0a); padding: 20px; border-radius: 20px 0px 20px 20px; border-right: 5px solid #d4af37; margin: 15px 0; color: #fdf5e6; box-shadow: 0 5px 15px rgba(0,0,0,0.4); }
    .user-bubble { background: linear-gradient(145deg, #0b132b, #1c2541); padding: 15px; border-radius: 0px 20px 20px 20px; border-left: 5px solid #4CAF50; margin: 15px 0; color: white; box-shadow: 0 5px 15px rgba(0,0,0,0.4); }
    .stButton>button { background: linear-gradient(45deg, #d4af37, #b5952f); color: #050a1f; font-weight: 900; border-radius: 15px; border: none; padding: 10px 25px; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. قواعد البيانات والحماية
# ==============================================================================
ALLOWED_PRO_CODES = [
    "M5_PRO_AHMED_01", "M5_PRO_MOHAMED_02", "M5_PRO_MAHMOUD_03", "M5_PRO_MOSTAFA_04", "M5_PRO_ALI_05",
    "M5_PRO_OMAR_06", "M5_PRO_AMR_07", "M5_PRO_KHALED_08", "M5_PRO_YOUSSEF_09", "M5_PRO_TARIQ_10",
    "M5_PRO_HASSAN_11", "M5_PRO_HUSSEIN_12", "M5_PRO_IBRAHIM_13", "M5_PRO_SAYED_14", "M5_PRO_HANY_15",
    "M5_PRO_SHERIF_16", "M5_PRO_TAHER_17", "M5_PRO_KARIM_18", "M5_PRO_WAEL_19", "M5_PRO_MAGDY_20"
]

ALLOWED_VIP_CODES = [
    "M5_VIP_KING_01", "M5_VIP_BOSS_02", "M5_VIP_ROYAL_03", "M5_VIP_ELITE_04", "M5_VIP_GOLD_05",
    "M5_VIP_PRIME_06", "M5_VIP_EXPERT_07", "M5_VIP_CHIEF_08", "M5_VIP_MASTER_09", "M5_VIP_LEADER_10",
    "M5_VIP_JUDGE_11", "M5_VIP_COURT_12", "M5_VIP_LAWYER_13", "M5_VIP_ALPHA_14", "M5_VIP_OMEGA_15"
]

def sanitize_input(text):
    if not text: return ""
    clean = re.sub(r'[^a-zA-Z0-9\s\u0600-\u06FF\?\!\.\,\:\-\_\(\)\'\"\n]', '', text)
    blacklist = ["<script", "union select", "drop table", "exec(", "ignore"]
    return None if any(word in clean.lower() for word in blacklist) else clean.strip()

# ==============================================================================
# 3. إعدادات الذكاء الاصطناعي (من Streamlit Secrets)
# ==============================================================================
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    API_READY = True
except Exception:
    API_READY = False
    st.error("⚠️ يرجى ضبط GEMINI_API_KEY في إعدادات Secrets.")

# ==============================================================================
# 4. الحالة العامة (State Management)
# ==============================================================================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "role" not in st.session_state: st.session_state.role = "free"
if "msg_timestamps" not in st.session_state: st.session_state.msg_timestamps = []

# ==============================================================================
# 5. محرك المستشار
# ==============================================================================
def ask_law_ai(prompt, role):
    if not API_READY: return "❌ النظام متوقف."
    model = genai.GenerativeModel('gemini-1.5-flash')
    persona = "أنت قاضٍ ومحامٍ مصري خبير." if role == "vip" else ("أنت محامٍ استئناف مصري." if role == "pro" else "أنت مساعد قانوني.")
    try:
        response = model.generate_content(f"{persona}\n\nسؤال المستخدم: {prompt}")
        return response.text
    except Exception as e: return f"خطأ تقني: {str(e)[:50]}"

# ==============================================================================
# 6. الواجهة الرئيسية
# ==============================================================================
if not st.session_state.logged_in:
    st.markdown("<br><br><h1>⚖️ LAW AI</h1><h3>بوابتك الذكية للقانون المصري</h3>", unsafe_allow_html=True)
    if st.button("🔐 دخول آمن للمنصة", use_container_width=True):
        st.session_state.logged_in = True
        st.rerun()
else:
    with st.sidebar:
        st.header("⚙️ لوحة القيادة")
        if st.button("🗑️ مسح المحادثة"): st.session_state.chat_history = []; st.rerun()
        if st.button("🚪 خروج"): st.session_state.logged_in = False; st.rerun()

    st.title("⚖️ قاعة الاستشارات القانونية")
    package = st.radio("اختر باقة المستشار:", ["🟢 مجانية", "🔵 Pro", "👑 VIP"], horizontal=True)
    
    # إدارة الأكواد
    if "Pro" in package:
        code = st.text_input("🔑 كود تفعيل Pro:", type="password")
        if code in ALLOWED_PRO_CODES: st.session_state.role = "pro"
    elif "VIP" in package:
        code = st.text_input("👑 كود تفعيل VIP:", type="password")
        if code in ALLOWED_VIP_CODES: st.session_state.role = "vip"
    else: st.session_state.role = "free"

    # المحادثة
    for msg in st.session_state.chat_history:
        style = "user-bubble" if msg["role"] == "user" else "ai-bubble"
        st.markdown(f"<div class='{style}'>{msg['content']}</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("اكتب قضيتك هنا..."):
        clean = sanitize_input(prompt)
        if clean:
            # حماية Spam
            now = datetime.datetime.now()
            st.session_state.msg_timestamps = [t for t in st.session_state.msg_timestamps if (now - t).total_seconds() < 60]
            if len(st.session_state.msg_timestamps) < 5:
                st.session_state.msg_timestamps.append(now)
                st.session_state.chat_history.append({"role": "user", "content": clean})
                with st.spinner("⚖️ المستشار يراجع النصوص القانونية..."):
                    resp = ask_law_ai(clean, st.session_state.role)
                    st.session_state.chat_history.append({"role": "assistant", "content": resp})
                st.rerun()
            else: st.error("⚠️ يرجى التمهل قليلاً لحماية السيرفر.")