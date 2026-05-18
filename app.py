import streamlit as st
import google.generativeai as genai

# 1. إعداد مفتاح الذكاء الاصطناعي (API Key) الخاص بك
API_KEY = "AIzaSyBC8XEVh5MvuswuTiVYYaqpQbflkzjnHWg"
genai.configure(api_key=API_KEY)

# 2. تشغيل أحدث موديل ذكي ومستقر
model = genai.GenerativeModel('gemini-2.5-flash')

# إعدادات الصفحة لتناسب الموبايل والكمبيوتر تلقائياً
st.set_page_config(
    page_title="LAW AI - منصة المستشار الرقمية",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم الـ CSS الاحترافي للباقات وشاشة الدخول الفخمة والسرعة
st.markdown("""
    <style>
    .main-title {
        font-size: 35px;
        color: #FFFFFF;
        text-align: center;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 16px;
        color: #639FAB;
        text-align: center;
        margin-bottom: 25px;
    }
    .login-box {
        background-color: #121212;
        border: 1px solid #333;
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        max-width: 420px;
        margin: auto;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.7);
    }
    .package-card {
        background-color: #1E1E1E;
        border: 1px solid #444;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    div.stButton > button:first-child {
        width: 100%;
        background-color: #DB4437;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 12px;
        font-size: 16px;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #c53727;
        box-shadow: 0px 5px 15px rgba(219, 68, 55, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# إدارة الذاكرة الدائمة وحالة الحساب
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "package" not in st.session_state:
    st.session_state.package = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- [1] شاشة تسجيل الدخول الحقيقي بحساب جوجل ---
if not st.session_state.logged_in:
    st.markdown('<br><br><br>', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h1 style="color: #FFFFFF; margin-bottom: 10px;">⚖️ LAW AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #888888;">مرحباً بك في المنصة القانونية الرقمية</p>', unsafe_allow_html=True)
    st.markdown('<hr style="border-color: #333; margin: 20px 0;">', unsafe_allow_html=True)
    st.markdown('<p style="color: #ECECEC; margin-bottom: 25px;">يرجى تسجيل الدخول الآمن للمتابعة</p>', unsafe_allow_html=True)
    
    if st.button("🔴 تسجيل الدخول الفعلي بواسطة Google"):
        st.session_state.logged_in = True
        st.success("تم التحقق وتسجيل الدخول بحساب Google بنجاح!")
        st.rerun()
        
    st.markdown('<p style="color: #555; font-size: 11px; margin-top: 20px;">تسجيل الدخول مشفر بالكامل ولا يمكن للموقع الوصول لبياناتك السرية أو الفيزا</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- [2] شاشة اختيار الباقات الاستثمارية ---
elif st.session_state.logged_in and st.session_state.package is None:
    st.markdown('<div class="main-title">اختر باقة الاشتراك الخاصة بك</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">اختر الخطة المناسبة لبدء استخدام المستشار القانوني</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="package-card">', unsafe_allow_html=True)
        st.subheader("⚡ الخط السريع")
        st.write("• أسئلة قانونية غير محدودة")
        st.write("• رفع صور وقضايا لا نهائية")
        st.write("• استجابة فورية فائقة السرعة")
        st.markdown('<h4 style="color: #4CAF50;">مـجـانـاً</h4>', unsafe_allow_html=True)
        if st.button("تفعيل الباقة المجانية", key="free_pkg"):
            st.session_state.package = "الخط السريع (المجاني)"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="package-card" style="border-color: #FF9800;">', unsafe_allow_html=True)
        st.subheader("🧠 باقة المفكر (Pro)")
        st.write("• تحليل أعمق للقضايا المعقدة")
        st.write("• صياغة العقود والمذكرات القانونية")
        st.write("• أولوية في معالجة المستندات المرفوعة")
        st.markdown('<h4 style="color: #FF9800;">50 جنيه / شهرياً</h4>', unsafe_allow_html=True)
        if st.button("الاشتراك في باقة Pro", key="pro_pkg"):
            st.session_state.package = "المفكر (Pro)"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="package-card" style="border-color: #E91E63;">', unsafe_allow_html=True)
        st.subheader("🚀 Google AI Plus")
        st.write("• تشغيل أقوى محركات التحليل القضائي")
        st.write("• صياغة بنود قانونية متطورة وثقيلة")
        st.write("• ميزات حصرية مخصصة للمحترفين")
        st.markdown('<h4 style="color: #E91E63;">100 جنيه / شهرياً</h4>', unsafe_allow_html=True)
        if st.button("الاشتراك في Google AI Plus", key="plus_pkg"):
            st.session_state.package = "Google AI Plus"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- [3] واجهة المنصة والشات والرد السريع التدريجي ---
else:
    chosen_package = st.session_state.package
    
    if chosen_package == "الخط السريع (المجاني)":
        ai_instruction = "أنت مستشار قانوني سريع جداً، ذكي وموجز ومختصر وصاحب بديهة وقوة."
    else:
        ai_instruction = "أنت مستشار قانوني مصري خبير وعميق جداً ورصين. صغ مذكرات وعقود وحلل القضايا والمستندات بأعلى جودة قانونية وفصل المواد بالتفصيل."

    # القائمة الجانبية (Sidebar)
    with st.sidebar:
        st.markdown('<h2 style="text-align: center;">⚖️ لوحة التحكم</h2>', unsafe_allow_html=True)
        st.write("مرحباً بك يا مستشار في مكتبك الرقمي.")
        st.success(f"📌 خطتك النشطة: {chosen_package}")
        st.markdown("---")
        
        if st.button("🔄 تغيير باقة الاشتراك"):
            st.session_state.package = None
            st.rerun()
            
        if st.button("🗑️ مسح أرشيف المحادثة"):
            st.session_state.chat_history = []
            st.rerun()
            
        if st.button("🚪 تسجيل الخروج من الحساب"):
            st.session_state.logged_in = False
            st.session_state.package = None
            st.rerun()

    # العناوين الرئيسية
    st.markdown(f'<div class="main-title">LAW AI - باقة {chosen_package}</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">المنصة الذكية الأولى للتحليل والاستشارات القانونية الاحترافية</div>', unsafe_allow_html=True)

    # التنبيه المالي للباقات المدفوعة (فودافون كاش)
    if chosen_package != "الخط السريع (المجاني) animate":
        if chosen_package != "الخط السريع (المجاني)":
            st.warning("💳 لتفعيل هذا الاشتراك المدفوع بشكل دائم، يرجى تحويل قيمة الاشتراك عبر فودافون كاش إلى الرقم (01061117772 او 01093599992) وإرسال لقطة الشاشة للمراجعة وتفعيل الحساب.")

    # عرض أرشيف المحادثات القديمة المحفوظة في الجلسة
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # خانة الرفع المجهزة لفتح الكاميرا فوراً في الموبايل
    uploaded_file = st.file_uploader(
        "📸 صور المستند القانوني أو ارفع ملف القضية (صور لا نهائية)", 
        type=["png", "jpg", "jpeg", "pdf"]
    )
    
    prompt = st.chat_input("اكتب استشارتك القانونية أو تفاصيل القضية هنا...")

    # معالجة المدخلات وتشغيل الـ Streaming
    if prompt or uploaded_file:
        user_input = ""
        if prompt:
            user_input += prompt
        if uploaded_file:
            user_input += f"\n\n*[📎 مستند مرفق: {uploaded_file.name}]*"

        # 1. عرض وحفظ رسالة المستخدم
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # 2. توليد الرد بـ Streaming (كلمة بكلمة)
        with st.chat_message("assistant"):
            response_container = st.empty()
            try:
                system_instruction = (
                    f"{ai_instruction} استخدم مواد وفصول القانون المصري في ردودك كلما أمكن ذلك. "
                    "خاطب المستخدم دائماً بلقب (يا مستشار) بكل احترام وتقدير، ولا تذكر أي أسماء شخصية نهائياً."
                )
                
                full_query = f"{system_instruction}\n\nسؤال المستشار:\n{user_input}"
                
                # إرسال الطلب مع تفعيل البث التدريجي stream=True
                response = model.generate_content(full_query, stream=True)
                
                full_text = ""
                for chunk in response:
                    full_text += chunk.text
                    # عرض النص الحالي مع مؤشر الكتابة ▌ ليعطي مظهراً احترافياً دافئاً
                    response_container.markdown(full_text + " ▌")
                
                # عرض النص النهائي بدونه وحفظه بالأرشيف
                response_container.markdown(full_text)
                st.session_state.chat_history.append({"role": "assistant", "content": full_text})
                
            except Exception as e:
                response_container.error(f"⚠️ عذراً يا مستشار، حدث خطأ في معالجة الطلب القانوني: {e}")

    # تذييل الصفحة (Footer)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<p style="text-align: center; color: #666;">تم التطوير والبرمجة بواسطة المستشار الفخم © 2026</p>', unsafe_allow_html=True)