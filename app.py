import streamlit as st
from google import genai
import time
from streamlit_cookies_controller import CookieController

# استدعاء أداة التحكم في الكوكيز لمنع مشاركة الأكواد بين الأجهزة
controller = CookieController()

# =================================================================
# ⚙️ إعدادات الذكاء الاصطناعي (أمان كامل عبر Streamlit Secrets)
# =================================================================
try:
    GENAI_API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=GENAI_API_KEY)
except Exception as e:
    st.error("⚠️ عذراً، مفتاح الـ API غير مضبوط في إعدادات السيرفر المخفية (Secrets).")

def ask_gemini_latest(prompt):
    max_retries = 3
    backoff_time = 2
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            if response.text:
                return response.text
            else:
                return "⚠️ تم الاتصال بنجاح ولكن لم يتم إرجاع نص."
        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1:
                time.sleep(backoff_time)
                backoff_time *= 1.5
                continue
            return f"❌ خطأ في الاتصال بالخادم: {str(e)}"

# =================================================================
# 🎨 واجهة منصة LAW AI - المستشار القانوني الرقمي الشيك
# =================================================================
st.set_page_config(page_title="LAW AI - منصة المستشار الرقمية", page_icon="⚖️", layout="centered")

# --- [ 🔑 قائمة أكواد باقة الـ Pro - شهر مايو ] ---
# الأكواد مقسمة بأسماء وأرقام واضحة جداً عشان تفتكر اديت إيه لمين ومستحيل تتلخبط
ALLOWED_PRO_CODES = [
    "M5_PRO_AHMED_01",
    "M5_PRO_MOHAMED_02",
    "M5_PRO_MAHMOUD_03",
    "M5_PRO_MOSTAFA_04",
    "M5_PRO_ALI_05",
    "M5_PRO_OMAR_06",
    "M5_PRO_AMR_07",
    "M5_PRO_KHALED_08",
    "M5_PRO_YOUSSEF_09",
    "M5_PRO_TARIQ_10",
    "M5_PRO_HASSAN_11",
    "M5_PRO_HUSSEIN_12",
    "M5_PRO_IBRAHIM_13",
    "M5_PRO_SAYED_14",
    "M5_PRO_HANY_15",
    "M5_PRO_SHERIF_16",
    "M5_PRO_TAHER_17",
    "M5_PRO_KARIM_18",
    "M5_PRO_WAEL_19",
    "M5_PRO_MAGDY_20",
    "M5_PRO_SAMEH_21",
    "M5_PRO_RAMY_22",
    "M5_PRO_HAITHAM_23",
    "M5_PRO_EZZ_24",
    "M5_PRO_ANWAR_25",
    "M5_PRO_ADEL_26",
    "M5_PRO_EMAD_27",
    "M5_PRO_MEDHAT_28",
    "M5_PRO_SAEED_29",
    "M5_PRO_FAROUK_30"
]

# --- [ 👑 قائمة أكواد باقة الـ VIP - شهر مايو ] ---
ALLOWED_VIP_CODES = [
    "M5_VIP_KING_01",
    "M5_VIP_BOSS_02",
    "M5_VIP_ROYAL_03",
    "M5_VIP_ELITE_04",
    "M5_VIP_GOLD_05",
    "M5_VIP_PRIME_06",
    "M5_VIP_EXPERT_07",
    "M5_VIP_CHIEF_08",
    "M5_VIP_MASTER_09",
    "M5_VIP_LEADER_10",
    "M5_VIP_JUDGE_11",
    "M5_VIP_COURT_12",
    "M5_VIP_LAWYER_13",
    "M5_VIP_ALPHA_14",
    "M5_VIP_OMEGA_15",
    "M5_VIP_SMART_16",
    "M5_VIP_TOP_17",
    "M5_VIP_MAX_18",
    "M5_VIP_HERO_19",
    "M5_VIP_SHIELD_20"
]

CASH_MESSAGE = "❌ عذراً، هذا الكود غير صحيح، أو تم تفعيله مسبقاً على جهاز آخر!"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- [الشاشة الأولى: تسجيل الدخول] ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>⚖️ LAW AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555;'>مرحباً بك في منصة المستشار القانوني الذكي</h3>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        google_btn = st.button("🌐 تسجيل الدخول للمنصة", use_container_width=True)
        if google_btn:
            st.session_state.logged_in = True
            st.rerun()

# --- [الشاشة الثانية: المنصة الرئيسية] ---
else:
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.title("⚖️ منصة LAW AI الرقمية")
    with col_logout:
        if st.button("تسجيل الخروج", type="primary"):
            st.session_state.logged_in = False
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("### 👑 اختر باقة الاشتراك الخاصة بك:")
    chosen_package = st.radio(
        "الباقات المتاحة:", 
        ["الخط السريع (المجاني) 🟢", "المفكر (Pro) - 100 جنيهاً شهرياً 🔵", "المستشار الملكي (VIP) - 200 جنيهاً شهرياً 👑"],
        index=0
    )

    is_premium = False
    current_role = "free"

    # قراءة الكود المسجل في متصفح المستخدم حالياً
    saved_cookie_code = controller.get('user_active_code')

    if "Pro" in chosen_package:
        if saved_cookie_code in ALLOWED_PRO_CODES:
            st.success("🎉 مرحباً بك مجدداً! تم التفعيل التلقائي لجهازك في باقة Pro.")
            is_premium = True
            current_role = "pro"
        else:
            auth_code = st.text_input("🔑 باقة Pro مقفولة. أدخل كود التفعيل الخاص بك:", type="password")
            if auth_code in ALLOWED_PRO_CODES:
                controller.set('user_active_code', auth_code)
                st.success("🎉 ممتاز! تم تفعيل الباقة وقفل الكود على جهازك الحالي بنجاح.")
                is_premium = True
                current_role = "pro"
                st.rerun()
            elif auth_code:
                st.error(CASH_MESSAGE)

    elif "VIP" in chosen_package:
        if saved_cookie_code in ALLOWED_VIP_CODES:
            st.success("👑 مرحباً بك يا ملك! تم تفعيل باقة VIP تلقائياً على جهازك.")
            is_premium = True
            current_role = "vip"
        else:
            auth_code = st.text_input("🔑 باقة VIP مقفولة. أدخل كود التفعيل الملكي:", type="password")
            if auth_code in ALLOWED_VIP_CODES:
                controller.set('user_active_code', auth_code)
                st.success("👑 أهلاً بك! تم التفعيل وقفل الكود الملكي على جهازك بنجاح.")
                is_premium = True
                current_role = "vip"
                st.rerun()
            elif auth_code:
                st.error(CASH_MESSAGE)
    
    else:
        is_premium = True
        current_role = "free"

    if is_premium:
        st.write("---")
        
        if current_role == "free":
            st.info("💡 **النسخة المجانية:** (إجابات مختصرة وسريعة للمعلومات العامة).")
        elif current_role == "pro":
            st.success("🚀 **باقة Pro النشطة:** (إجابات تفصيلية مدعمة بمواد القانون المصري).")
        elif current_role == "vip":
            st.warning("👑 **باقة VIP الملكية:** (تحليل قضايا كاملة، استراتيجيات، وتوقع قرارات القاضي).")

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        user_input = st.chat_input("اكتب سؤالك أو تفاصيل قضيتك هنا...")

        if user_input:
            with st.chat_message("user"):
                st.write(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            with st.chat_message("assistant"):
                with st.spinner("⚖️ جاري صياغة الرد القانوني..."):
                    prompt_modifier = ""
                    if current_role == "free":
                        prompt_modifier = "أنت مساعد قانوني مصري. أجب باختصار شديد وبشكل مباشر على هذا السؤال: "
                    elif current_role == "pro":
                        prompt_modifier = "أنت مستشار محامي مصري خبير. قدم إجابة قانونية تفصيلية واحترافية، وادعم إجابتك بمواد القانون المصري كلما أمكن ذلك: "
                    elif current_role == "vip":
                        prompt_modifier = "أنت قاضي مصري ومستشار قانوني من الطراز الرفيع. قم بتحليل هذه القضية أو السؤال من جميع الجوانب، قدم الحلول الممكنة، الثغرات القانونية، والتكييف القانوني الدقيق: "

                    final_prompt = prompt_modifier + "\nالسؤال/القضية: " + user_input
                    ai_response = ask_gemini_latest(final_prompt)
                    
                    st.write(ai_response)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})