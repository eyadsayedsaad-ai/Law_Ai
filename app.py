import streamlit as st
from google import genai

# =================================================================
# ⚙️ إعدادات الذكاء الاصطناعي (أمان كامل عبر Streamlit Secrets)
# =================================================================

# محاولة قراءة المفتاح بأمان من إعدادات السيرفر المخفية بره الكود خالص
try:
    GENAI_API_KEY = st.secrets["GEMINI_API_KEY"]
    # تشغيل الـ Client الجديد كلياً لـ جوجل المتوافق مع مكتبة google-genai
    client = genai.Client(api_key=GENAI_API_KEY)
except Exception as e:
    # رسالة تظهر فقط لو المفتاح مش موجود في الـ Secrets على موقع Streamlit
    st.error("⚠️ عذراً، مفتاح الـ API غير مضبوط في إعدادات السيرفر المخفية (Secrets) على موقع Streamlit. يرجى إضافته ليعمل الذكاء الاصطناعي.")

def ask_gemini_latest(prompt):
    try:
        # التعديل النهائي: استخدام أحدث موديل مستقر ومعتمد متوافق 100%
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        if response.text:
            return response.text
        else:
            return "⚠️ تم الاتصال بنجاح ولكن لم يتم إرجاع نص."
    except Exception as e:
        return f"❌ خطأ في الاتصال بالخادم الحديث لـ جوجل: {str(e)}"

# =================================================================
# 🎨 واجهة منصة LAW AI - المستشار القانوني الرقمي الشيك
# =================================================================
st.set_page_config(page_title="LAW AI - منصة المستشار الرقمية", page_icon="⚖️", layout="centered")

# أكواد باقات الـ Pro والـ VIP
ALLOWED_PRO_CODES = ["ANAS11", "PRO99", "LAW77", "PASS44", "VIP33"]
ALLOWED_VIP_CODES = ["KING10", "BOSS20", "VIP👑99", "LAWVIP", "ANASVIP"]
CASH_MESSAGE = "❌ عذراً، رقم التحويل غير متاح حالياً. يرجى التواصل مع المستشار أنس مباشرة لتفعيل حسابك وتلقي كود الدخول."

# إعداد حالة الجلسة لتخزين الشات وتسجيل الدخول
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
    # شريط التحكم العلوي
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.title("⚖️ منصة LAW AI الرقمية")
    with col_logout:
        if st.button("تسجيل الخروج", type="primary"):
            st.session_state.logged_in = False
            st.session_state.chat_history = []
            st.rerun()

    # قسم اختيار الباقة
    st.markdown("### 👑 اختر باقة الاشتراك الخاصة بك:")
    chosen_package = st.radio(
        "الباقات المتاحة:", 
        ["الخط السريع (المجاني) 🟢", "المفكر (Pro) - 100 جنيهاً شهرياً 🔵", "المستشار الملكي (VIP) - 200 جنيهاً شهرياً 👑"],
        index=0
    )

    is_premium = False
    current_role = "free"

    # التحقق من أكواد الباقات
    if "Pro" in chosen_package:
        auth_code = st.text_input("🔑 باقة Pro مقفولة. أدخل كود التفعيل الخاص بك:", type="password")
        if auth_code in ALLOWED_PRO_CODES:
            st.success("🎉 ممتاز! تم التحقق وتفعيل باقة الـ Pro بنجاح.")
            is_premium = True
            current_role = "pro"
        elif auth_code:
            st.error(f"🔒 الكود غير صحيح! {CASH_MESSAGE}")

    elif "VIP" in chosen_package:
        auth_code = st.text_input("🔑 باقة VIP مقفولة. أدخل كود التفعيل الملكي:", type="password")
        if auth_code in ALLOWED_VIP_CODES:
            st.success("👑 أهلاً بك في الباقة الملكية VIP! تم الفتح بنجاح.")
            is_premium = True
            current_role = "vip"
        elif auth_code:
            st.error(f"🔒 الكود غير صحيح! {CASH_MESSAGE}")
    
    else:
        is_premium = True
        current_role = "free"

    # --- [قسم الشات المباشر والمحمي] ---
    if is_premium:
        st.write("---")
        
        # رسالة تعريفية حسب الباقة
        if current_role == "free":
            st.info("💡 **النسخة المجانية:** (إجابات مختصرة وسريعة للمعلومات العامة).")
        elif current_role == "pro":
            st.success("🚀 **باقة Pro النشطة:** (إجابات تفصيلية مدعمة بمواد القانون المصري).")
        elif current_role == "vip":
            st.warning("👑 **باقة VIP الملكية:** (تحليل قضايا كاملة، استراتيجيات، وتوقع قرارات القاضي).")

        # عرض سجل الشات
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # حقل إدخال الشات
        user_input = st.chat_input("اكتب سؤالك أو تفاصيل قضيتك هنا...")

        # معالجة إدخال المستخدم
        if user_input:
            with st.chat_message("user"):
                st.write(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            with st.chat_message("assistant"):
                with st.spinner("⚖️ جاري صياغة الرد القانوني..."):
                    
                    # تعديل صياغة الطلب حسب باقة الاشتراك
                    prompt_modifier = ""
                    if current_role == "free":
                        prompt_modifier = "أنت مساعد قانوني مصري. أجب باختصار شديد وبشكل مباشر على هذا السؤال: "
                    elif current_role == "pro":
                        prompt_modifier = "أنت مستشار محامي مصري خبير. قدم إجابة قانونية تفصيلية واحترافية، وادعم إجابتك بمواد القانون المصري كلما أمكن ذلك: "
                    elif current_role == "vip":
                        prompt_modifier = "أنت قاضي مصري ومستشار قانوني من الطراز الرفيع. قم بتحليل هذه القضية أو السؤال من جميع الجوانب، قدم الحلول الممكنة، الثغرات القانونية، والتكييف القانوني الدقيق: "

                    # إرسال الطلب للذكاء الاصطناعي
                    final_prompt = prompt_modifier + "\nالسؤال/القضية: " + user_input
                    ai_response = ask_gemini_latest(final_prompt)
                    
                    # عرض وتخزين رد الذكاء الاصطناعي
                    st.write(ai_response)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})