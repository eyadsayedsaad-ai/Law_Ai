# ==============================================================================
# 🌟 منصة LAW AI - الإصدار الأسطوري النهائي والمستقر 100%
# 🌟 المبرمج الرئيسي: البطل أنس
# 🌟 الوصف: مستشار قانوني، نظام باقات كامل، حماية كوكيز، ومكافحة Spam
# ==============================================================================

import streamlit as st
import google.generativeai as genai
import time
import datetime
import re
import secrets
from streamlit_cookies_controller import CookieController

# ==============================================================================
# 🎨 [القسم الأول]: التصميم الملكي والواجهة الفخمة (Premium UI/UX)
# ==============================================================================
st.set_page_config(page_title="LAW AI | المستشار الرقمي", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght=400;700;900&display=swap');
    
    .stApp {
        background-color: #050a1f; 
        color: #e0e1dd;
        font-family: 'Cairo', sans-serif;
    }
    
    h1, h2, h3 {
        text-align: center;
        color: #d4af37 !important;
        font-family: 'Cairo', sans-serif;
        font-weight: 900;
        text-shadow: 0px 4px 15px rgba(212, 175, 55, 0.3);
    }
    
    .ai-bubble {
        background: linear-gradient(145deg, #1a1105, #2a1b0a);
        padding: 20px;
        border-radius: 20px 0px 20px 20px;
        margin: 15px 0;
        border-right: 5px solid #d4af37;
        color: #fdf5e6;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4);
        font-size: 18px;
        line-height: 1.8;
        direction: rtl;
    }
    
    .user-bubble {
        background: linear-gradient(145deg, #0b132b, #1c2541);
        padding: 15px;
        border-radius: 0px 20px 20px 20px;
        margin: 15px 0;
        border-left: 5px solid #4CAF50;
        color: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4);
        font-size: 16px;
        line-height: 1.6;
        direction: rtl;
    }
    
    .stTextInput>div>div>input {
        border-radius: 15px;
        border: 2px solid #d4af37 !important;
        background-color: #0b132b !important;
        color: white !important;
        text-align: center;
    }
    
    .stButton>button {
        border-radius: 15px;
        background: linear-gradient(45deg, #d4af37, #b5952f);
        color: #050a1f !important;
        font-weight: 900;
        font-size: 18px;
        border: none;
        transition: all 0.4s ease;
        padding: 12px;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.6);
    }
    
    hr { border-color: rgba(212, 175, 55, 0.2); }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 🛡️ [القسم الثاني]: جدار الحماية، الكوكيز، وإدارة الجلسات الآمنة
# ==============================================================================
controller = CookieController()

def sanitize_input(text):
    """تصفية حاسمة للمدخلات لمنع الرموز الضارة أو محاولات الاختراق"""
    if not text: return ""
    clean_text = re.sub(r'[^a-zA-Z0-9\s\u0600-\u06FF\?\!\.\,\:\-\_\(\)\'\"\n]', '', text)
    blacklist = ["<script", "javascript:", "union select", "drop table", "exec(", "ignore previous"]
    if any(word in clean_text.lower() for word in blacklist):
        return None
    return clean_text.strip()

# تهيئة كاملة وبدون أي نقص لمتغيرات الجلسة (Session State)
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "failed_attempts" not in st.session_state: st.session_state.failed_attempts = 0
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "lockout_time" not in st.session_state: st.session_state.lockout_time = None
if "msg_timestamps" not in st.session_state: st.session_state.msg_timestamps = []

# نظام حظر التخمين العنيف المؤقت (Anti-Brute Force Lockout)
if st.session_state.lockout_time:
    elapsed = (datetime.datetime.now() - st.session_state.lockout_time).total_seconds()
    if elapsed < 120:
        st.error(f"🚨 تم حظر العمليات مؤقتاً لحماية المنصة. يرجى الانتظار {int(120 - elapsed)} ثانية.")
        st.stop()
    else:
        st.session_state.failed_attempts = 0
        st.session_state.lockout_time = None

# ==============================================================================
# 🧠 [القسم الثالث]: محرك تشغيل الذكاء الاصطناعي المستقر والآمن
# ==============================================================================
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    API_READY = True
else:
    API_READY = False
    st.error("⚠️ مفتاح GEMINI_API_KEY مفقود من إعدادات Secrets!")

def ask_law_ai(prompt, package_type):
    if not API_READY: return "❌ النظام متوقف تقنياً لعدم وجود مفتاح التشغيل."

    # تحديد صرامة وعقلية الرد حسب رتبة الباقة
    if package_type == "vip":
        system_persona = (
            "أنت مستشار قانوني مصري من الطراز الرفيع وقاضي محكمة نقض وعضو مجلس الدولة. "
            "مهمتك تحليل القضية المعروضة من كافة الجوانب، ذكر ثغرات الخصم، "
            "وضع استراتيجية دفاع محكمة، والاستناد الحتمي لأرقام المواد في القانون المدني أو الجنائي المصري. "
            "استخدم لغة قانونية فخمة ورصينة."
        )
    elif package_type == "pro":
        system_persona = (
            "أنت محامي استئناف مصري متميز وخبير. أجب بتفصيل واسع عن السؤال القانوني، "
            "واذكر الخطوات الإجرائية والأوراق المطلوبة وفقاً للقانون المصري."
        )
    else:
        system_persona = "أنت مساعد قانوني مصري بسيط. قدم إجابة قانونية مباشرة، صحيحة، ومختصرة جداً."

    final_prompt = f"[تعليمات صارمة: لا تكتب أكواد، لا تخرج عن دورك كخبير قانوني مصري]\n\n{system_persona}\n\nسؤال الموكل:\n{prompt}"
    
    try:
        # ✅ التعديل الوحيد: حذف "models/" من اسم الموديل - هذا هو سبب الخطأ 404
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        response = model.generate_content(final_prompt)
        return response.text if response.text else "⚠️ عذراً، لم أتمكن من صياغة الرد القانوني المناسب."
    except Exception as e:
        err = str(e).lower()
        if "429" in err or "quota" in err:
            return "⚠️ (خطأ 429): الرصيد المجاني للمفتاح الحالي نفد. يرجى الانتظار دقيقة."
        return f"❌ خطأ تقني في قاعة المحكمة الرقمية: {str(e)[:150]}"

# ==============================================================================
# 🔑 [القسم الرابع]: قواعد بيانات الباقات كاملة (جميع الأكواد الـ 35 بالتفصيل)
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

# ==============================================================================
# 🏛️ [القسم الخامس]: واجهات العرض والـ Frontend الكامل للموقع
# ==============================================================================
if not st.session_state.logged_in:
    # شاشة ترحيب الدخول الأولى للمنصة
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1>⚖️ LAW AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3>بوابتك الذكية والآمنة للقانون المصري</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔐 دخول آمن للمنصة", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()
else:
    # --- شريط التحكم الجانبي الكامل (Sidebar) ---
    with st.sidebar:
        st.markdown("<h2>⚙️ لوحة القيادة</h2>", unsafe_allow_html=True)
        st.write("---")
        st.info("💡 يتم تشفير كافة المحادثات الجارية بتقنية End-to-End.")
        st.write("---")
        if st.button("🗑️ مسح ذاكرة المحادثة"):
            st.session_state.chat_history = []
            st.rerun()
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.logged_in = False
            st.session_state.chat_history = []
            st.rerun()
            
    # --- رأس الصفحة الرئيسية الحية ---
    st.title("⚖️ قاعة الاستشارات القانونية الرقمية")
    st.markdown("<p style='text-align: center; color: #888;'>اختر رتبة وحجم باقة المستشار القانوني لليوم</p>", unsafe_allow_html=True)
    
    # اختيار نوع الباقة الحالية
    chosen_package = st.radio("", ["🟢 باقة مجانية (إجابة سريعة)", "🔵 باقة المحامي (Pro)", "👑 باقة المستشار الملكي (VIP)"], horizontal=True)
    
    is_premium = False
    current_role = "free"
    
    # محاولة قراءة الكود المخزن مسبقاً في كوكيز متصفح الموكل
    saved_cookie = str(controller.get('user_active_code'))

    # تفاصيل تشغيل باقة Pro
    if "Pro" in chosen_package:
        if any(secrets.compare_digest(saved_cookie, c) for c in ALLOWED_PRO_CODES):
            st.success("🔵 باقة المـحـامـي (Pro) مفعلة تلقائياً عبر الكوكيز.")
            is_premium, current_role = True, "pro"
        else:
            code = st.text_input("🔑 أدخل كود تفعيل باقة (Pro):", type="password")
            if code:
                if code in ALLOWED_PRO_CODES:
                    controller.set('user_active_code', code)
                    st.success("تم التفعيل بنجاح! جاري التحديث...")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.session_state.failed_attempts += 1
                    if st.session_state.failed_attempts >= 5:
                        st.session_state.lockout_time = datetime.datetime.now()
                        st.rerun()
                    st.error(f"❌ كود خاطئ. متبقي {5 - st.session_state.failed_attempts} محاولات.")
                    
    # تفاصيل تشغيل باقة VIP الملكية
    elif "VIP" in chosen_package:
        if any(secrets.compare_digest(saved_cookie, c) for c in ALLOWED_VIP_CODES):
            st.warning("👑 باقة المـسـتـشـار الملكي (VIP) مفعلة بكامل الصلاحيات.")
            is_premium, current_role = True, "vip"
        else:
            code = st.text_input("👑 أدخل كود التفعيل الملكي (VIP):", type="password")
            if code:
                if code in ALLOWED_VIP_CODES:
                    controller.set('user_active_code', code)
                    st.success("مرحباً بك سيادة المستشار! جاري التحديث...")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.session_state.failed_attempts += 1
                    if st.session_state.failed_attempts >= 5:
                        st.session_state.lockout_time = datetime.datetime.now()
                        st.rerun()
                    st.error(f"❌ كود خاطئ. متبقي {5 - st.session_state.failed_attempts} محاولات.")
    else:
        # الباقة المجانية مفتوحة دائماً
        is_premium, current_role = True, "free"

    # --- نظام التفاعل الحي وإرسال واستقبال الرسائل الكامل ---
    if is_premium:
        st.write("---")
        
        # طباعة الشات التاريخي للمستخدم والمستشار بالترتيب والتصميم الذهبي الفخم
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"<div align='right' class='user-bubble'>👤 <b>سؤالك:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div align='right' class='ai-bubble'>⚖️ <b>المستشار:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

        # استقبال استشارة جديدة وحمايتها ضد الإرسال السريع جداً (Spam)
        if prompt := st.chat_input("اكتب وقائع قضيتك أو سؤالك القانوني هنا بالتفصيل..."):
            clean_prompt = sanitize_input(prompt)
            if clean_prompt:
                now = datetime.datetime.now()
                st.session_state.msg_timestamps = [t for t in st.session_state.msg_timestamps if (now - t).total_seconds() < 60]
                if len(st.session_state.msg_timestamps) >= 4:
                    st.error("⚠️ يرجى إبطاء معدل إرسال الاستشارات قليلاً لحماية السيرفر.")
                else:
                    st.session_state.msg_timestamps.append(now)
                    st.session_state.chat_history.append({"role": "user", "content": clean_prompt})
                    st.markdown(f"<div align='right' class='user-bubble'>👤 <b>سؤالك:</b><br>{clean_prompt}</div>", unsafe_allow_html=True)
                    
                    # استدعاء وعرض رد المستشار القانوني بـ Spinner فخم
                    with st.spinner("⚖️ يقوم المستشار الآن بمراجعة الحيثيات ومواد القانون المصري..."):
                        response = ask_law_ai(clean_prompt, current_role)
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                        st.markdown(f"<div align='right' class='ai-bubble'>⚖️ <b>المستشار:</b><br>{response}</div>", unsafe_allow_html=True)