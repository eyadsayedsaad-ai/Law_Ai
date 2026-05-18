import streamlit as st
import google.generativeai as genai

# =================================================================
# ⚙️ إعدادات الذكاء الاصطناعي (Gemini API)
# =================================================================
GENAI_API_KEY = "ضع_مفتاح_جوجل_gemini_هنا" 
genai.configure(api_key=GENAI_API_KEY)

st.set_page_config(page_title="LAW AI - منصة المستشار الرقمية", page_icon="⚖️", layout="centered")

# =================================================================
# 🔑 مكان تغيير الباسوردات ورسالة الكاش (التحكم اليدوي الكامل)
# =================================================================
# 1. اكتب الـ 5 باسات بتوع باقة الـ Pro هنا بإيدك:
ALLOWED_PRO_CODES = [
    "ANAS11",
    "PRO99",
    "LAW77",
    "PASS44",
    "VIP33"
]

# 2. اكتب الـ 5 باسات بتوع باقة الـ VIP هنا بإيدك:
ALLOWED_VIP_CODES = [
    "KING10",
    "BOSS20",
    "VIP👑99",
    "LAWVIP",
    "ANASVIP"
]

# 3. تعديل رسالة رقم التحويل (لا يوجد رقم الآن):
CASH_MESSAGE = "❌ عذراً، رقم التحويل غير متاح حالياً. يرجى التواصل مع المستشار أنس مباشرة لتفعيل حسابك وتلقي كود الدخول."
# =================================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- [الشاشة الأولى: تسجيل الدخول] ---
if not st.session_state.logged_in:
    # هنا تم تعديل الخاصية لـ unsafe_allow_html=True بنجاح عشان الشاشة الحمراء تروح
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>⚖️ LAW AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>مرحباً بك في منصة المستشار القانوني الذكي</h3>", unsafe_allow_html=True)
    st.write("")
    
    google_btn = st.button("🌐 تسجيل الدخول بواسطة حساب Google", use_container_width=True)
    if google_btn:
        st.session_state.logged_in = True
        st.rerun()

# --- [الشاشة الثانية: المنصة الرئيسية] ---
else:
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.title("⚖️ منصة LAW AI الرقمية")
    with col_logout:
        if st.button("تسجيل الخروج"):
            st.session_state.logged_in = False
            st.session_state.chat_history = []
            st.rerun()

    # قسم الباقات واختيار الاشتراك
    st.markdown("### 👑 اختر باقة الاشتراك الخاصة بك:")
    chosen_package = st.radio(
        "الباقات المتاحة:", 
        ["الخط السريع (المجاني)", "المفكر (Pro) - 100 جنيهاً شهرياً", "المستشار الملكي (VIP) - 200 جنيهاً شهرياً"],
        index=0
    )

    # تجهيز متغيرات الأمان لقفل الشات
    is_premium = False
    current_role = "free"

    # الفحص ومطابقة الكود المكتوب مع لستة الباسوردات الثابتة
    if chosen_package == "المفكر (Pro) - 100 جنيهاً شهرياً":
        auth_code = st.text_input("🔑 باقة Pro مقفولة. أدخل كود التفعيل الخاص بك:", type="password")
        if auth_code in ALLOWED_PRO_CODES:
            st.success("🎉 ممتاز! تم التحقق وتفعيل باقة الـ Pro بنجاح.")
            is_premium = True
            current_role = "pro"
        else:
            st.error(f"🔒 الشات مقفول! {CASH_MESSAGE}")

    elif chosen_package == "المستشار الملكي (VIP) - 200 جنيهاً شهرياً":
        auth_code = st.text_input("🔑 باقة VIP مقفولة. أدخل كود التفعيل الملكي:", type="password")
        if auth_code in ALLOWED_VIP_CODES:
            st.success("👑 أهلاً بك في الباقة الملكية VIP! تم الفتح بنجاح.")
            is_premium = True
            current_role = "vip"
        else:
            st.error(f"🔒 الشات مقفول! {CASH_MESSAGE}")
    
    else:
        # الباقة المجانية تفتح تلقائياً
        is_premium = True
        current_role = "free"

    # --- [قسم الشات المحمي والذكي] ---
    if is_premium:
        st.write("---")
        st.markdown("### 🤖 مستشارك القانوني جاهز للرد:")
        
        if current_role == "free":
            st.info("💡 النسخة المجانية نشطة (إجابات مختصرة وسريعة).")
        elif current_role == "pro":
            st.success("🚀 باقة Pro نشطة (إجابات تفصيلية مع المواد القانونية).")
        elif current_role == "vip":
            st.info("👑 باقة VIP الملكية نشطة (تحليل قضايا كاملة واستراتيجيات قانونية).")

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        user_input = st.chat_input("اكتب سؤالك القانوني هنا...")

        if user_input:
            with st.chat_message("user"):
                st.write(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            with st.chat_message("assistant"):
                with st.spinner("جاري مراجعة القوانين المصرية..."):
                    try:
                        prompt_modifier = ""
                        if current_role == "free":
                            prompt_modifier = "أجب باختصار كمستشار قانوني مصري: "
                        elif current_role == "pro":
                            prompt_modifier = "أنت مستشار قانوني مصري خبير، قدم إجابة مفصلة مدعمة بمواد القانون: "
                        elif current_role == "vip":
                            prompt_modifier = "أنت قاضي ومستشار قانوني مصري، حلل القضية بدقة شديدة وقدم الحلول والثغرات القانونية: "

                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content(prompt_modifier + user_input)
                        
                        st.write(response.text)
                        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error("حدث خطأ في الاتصال بالخادم، تأكد من الـ API Key.")