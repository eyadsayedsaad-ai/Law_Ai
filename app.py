# ==============================================================================
# 🌟 LAW AI - النسخة النهائية المحسنة (فخمة + مستقرة)
# ==============================================================================

import streamlit as st
import openai
import firebase_admin
from firebase_admin import credentials, firestore
import re
import datetime

st.set_page_config(page_title="LAW AI", page_icon="⚖️", layout="wide")

# ====================== التصميم الفخم ======================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1328 100%);
        color: #e0e1dd;
        font-family: 'Cairo', sans-serif;
    }
    
    h1, h2, h3 { color: #d4af37 !important; text-align: center; font-weight: 900; }
    
    .ai-bubble {
        background: linear-gradient(145deg, #1f1629, #2a1f3d);
        padding: 22px;
        border-radius: 20px 8px 20px 20px;
        margin: 15px 0;
        border-right: 7px solid #d4af37;
        box-shadow: 0 8px 25px rgba(0,0,0,0.5);
        direction: rtl;
        line-height: 1.85;
    }
    
    .user-bubble {
        background: linear-gradient(145deg, #0f1b3a, #1e2a4d);
        padding: 22px;
        border-radius: 8px 20px 20px 20px;
        margin: 15px 0;
        border-left: 7px solid #4CAF50;
        box-shadow: 0 8px 25px rgba(0,0,0,0.5);
        direction: rtl;
    }
    
    .stChatInput input {
        border: 2px solid #d4af37 !important;
        border-radius: 15px !important;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #d4af37, #c9a02f);
        color: #0a0e1a !important;
        font-weight: 700;
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# ====================== OpenRouter من Streamlit Secrets ======================
openai.api_key = st.secrets["OPENROUTER_API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"

# ====================== Firebase ======================
FIREBASE_CREDS = {
    "type": "service_account",
    "project_id": "law-ai-d02c9",
    "private_key_id": "a2bf3b50454cd0d05297f8285527e3ffc14dc5a6",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCyrkJ35+gf9OkP\nJvvW872GjqiELyer21n5XFggQnDP7IpleATL7jQ7IhKE4FAUWEqn6Xj9Wc/R6UCw\nis8SU41ggtnKJR0Fmr6sE0fR8HWlqD7pFoSUpDYrowA1NeD02FtVR/b86OoCdNCo\nMxXCl7aqmdygh+xe72nO17sCdMTxrdCzC1GRS4Nes2j3H4w4SqErZxeXpJucxH+t\nHIHmi/+kpQQ+e8Ajpq4y547D9PSQqnrFPgDpN0a7HQCK0q6Of/SSqurkl3pz0SA9\nfYULF8dNWiZbkI0e6b05Pxga+iy1e4kYhsG0ACUwjn3UqvYy1rTDYeOjWy75WSrL\np7rVDZW5AgMBAAECggEABb6nQbeD+kJ6dup24Mr7Or3rlc8/KxBFSqPrWbWZJaUU\neb1nLO8KBUoeFHNyqxg2wR4AUp6ohu1FIayDryAVknuShEjuL5WWAoC6MMNEU+nw\nzZL4jPsqUUT8/e/TvWAXHe90CBW/iy7RAbrUc8WwzQE69ujljhywlNT1yqA1wjcZ\nu5m9qd3j59X2+RKhiqiZAL8+C4KZSyCw/mj63MIKZlVxgJw6ZAYxuDRYZdMec6t/\nbaeVk+4BSusg3shtOv8zyNOTCcH1uiIPI/WOs9trMiCcrWGjkZMXqxzhB1KaAWER\ns5v66cywprJ0vZRAGH7D/ozAc3E/sl3njxv9xp0tCQKBgQDWD35/BB1r9NdOkcOG\njvZ6bj7HGNOAZ4jnIJso/Z/ERQgQVltBUBeUEKDzG9hfx4miegMHB/RhL/YmDHNJ\nnF0Z3Hw4D06loLS2MKqePyV3svwn1WFI9GnT5rDUlkblbROjjm67kQRgjmkcytjV\new1nMghUPj00e+UMUkTLQMu4nQKBgQDVsD2rscu3YOKFsHuzgzbXsuVg1Pc+vDmY\nBA0uhbmF5nmXZg4h0R5nEf8GqAXYY5BmkqIxb7sdmNjTru0XYVJOvsPXnVp1cHTb\nG7WDwN30OVduYQm4tNrdYd35RwISaJWfCqYcQh4ASvOBBax4DVhFGlUSyUrCPaot\nHxMKVrnAzQKBgAfMwLs4Fypb3YyLWyiIBQspATiX+vzuyNpDIeQ4eZ3ZNhYCT4jt\nti46/OJe3V+AEc/NylZzP8Ba0wlH4tuHywyqMAyK4j6+wFbzJwRlIKRf7Tg2Wjki\nTsjd2wuj/ilV9CU9h2NmQVaTWdkmuwfsV+yusgb/zZMgAJSWWtNdJQ8xAoGAWq04\n3jzKN3yzYwuq0lgh05IkZ9y3NjXlMq61cUJpoXpVqnsyEAOPJSmr0IVIRbSqN/yN\nOvEws7SCfgFCtqMjrCqjLEGneyJHVBsEAW68QMB8a2heGbUVEtBOw1LwfCNJKn34\nUxFzbahggCWKND9lb51m8Fvej2Jfblo7WC3JERkCgYBqNKJuZaU42dXRMug+vvVx\nOMpofgeCEuBaOIyAc7Z/qLuJGojqAOwIRFzmudxNDou+c17Fmv8SlGh8Nx3jv5dm\ncSiGAMOpapOICwZhQpqGQInJbxou2H+i63B80mE+AnJoXCAJRL17FxAq5Xd179CA\ny13tcYpBgDGtfyfYyEKfAw==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-fbsvc@law-ai-d02c9.iam.gserviceaccount.com",
    "client_id": "111631610644688913419",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40law-ai-d02c9.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDS)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ====================== الدوال ======================
def save_conversation(user_id, topic, messages, role):
    try:
        db.collection("users").document(user_id).collection("conversations").document(topic).set({
            "topic": topic,
            "messages": messages,
            "role": role,
            "updated_at": datetime.datetime.now().isoformat()
        })
    except: pass

def load_conversations(user_id):
    try:
        docs = db.collection("users").document(user_id).collection("conversations").order_by("updated_at", direction=firestore.Query.DESCENDING).stream()
        return [doc.to_dict() for doc in docs]
    except: return []

def generate_topic(text):
    return " ".join(text.strip().split()[:8]) or "استشارة جديدة"

def sanitize_input(text):
    if not text: return ""
    return re.sub(r'[^a-zA-Z0-9\s\u0600-\u06FF\؟\!\.\,\:\-\_\(\)\'\"]', '', text).strip()

# ====================== الذكاء الاصطناعي ======================
def ask_law_ai(prompt, role):
    personas = {
        "vip": "قاضي محكمة نقض مصري من الطراز الرفيع وعضو مجلس الدولة",
        "pro": "محامي استئناف مصري متميز وخبير",
        "free": "مساعد قانوني مصري بسيط"
    }

    system_prompt = f"""
    أنت {personas.get(role, personas["free"])} متخصص في القانون المصري.
    أجب باحترافية، استشهد بالمواد القانونية بدقة، ورتب الرد كالتالي:
    - الوقائع
    - المواد القانونية المنطبقة
    - التحليل
    - النصيحة العملية
    أنهِ الرد دائماً بتنبيه قانوني.
    لا تكتب أكواد برمجية أبداً.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.65,
            max_tokens=2300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ حدث خطأ: {str(e)[:150]}"

# ====================== الباقات ======================
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

# ====================== الجلسة ======================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "current_topic" not in st.session_state: st.session_state.current_topic = None
if "current_role" not in st.session_state: st.session_state.current_role = "free"
if "is_premium" not in st.session_state: st.session_state.is_premium = True
if "conversations" not in st.session_state: st.session_state.conversations = []
if "failed_attempts" not in st.session_state: st.session_state.failed_attempts = 0
if "show_code_input" not in st.session_state: st.session_state.show_code_input = None

# ====================== الواجهة ======================
if not st.session_state.logged_in:
    st.markdown("<h1>⚖️ LAW AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3>مستشارك القانوني الذكي للقانون المصري</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div style='background:linear-gradient(145deg,#0b132b,#1c2541);padding:20px;border-radius:15px;border:2px solid #d4af37;text-align:center;color:#fdf5e6;'>
        <h3>🟢 مجانية</h3><h2>مجاني</h2><p>إجابة قانونية سريعة</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div style='background:linear-gradient(145deg,#0b132b,#1c2541);padding:20px;border-radius:15px;border:2px solid #d4af37;text-align:center;color:#fdf5e6;'>
        <h3>🔵 Pro</h3><h2>20$</h2><p>تحليل قانوني تفصيلي</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div style='background:linear-gradient(145deg,#1a1105,#2a1b0a);padding:20px;border-radius:15px;border:2px solid #FFD700;text-align:center;color:#fdf5e6;'>
        <h3>👑 VIP</h3><h2>50$</h2><p>استراتيجية دفاع محكمة كاملة</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name = st.text_input("👤 أدخل اسمك", placeholder="أحمد محمد")
        if st.button("🚪 دخول المنصة", use_container_width=True):
            if name.strip():
                st.session_state.user_name = name.strip()
                st.session_state.user_id = re.sub(r'[^a-zA-Z0-9\u0600-\u06FF]', '_', name.strip())
                st.session_state.logged_in = True
                st.session_state.conversations = load_conversations(st.session_state.user_id)
                st.rerun()
            else:
                st.error("⚠️ من فضلك اكتب اسمك أولاً")

else:
    with st.sidebar:
        st.success(f"👤 {st.session_state.user_name}")
        st.write("---")

        if st.session_state.current_role == "vip":
            st.warning("👑 باقة VIP مفعّلة")
        elif st.session_state.current_role == "pro":
            st.success("🔵 باقة Pro مفعّلة")
        else:
            st.info("🟢 الباقة المجانية")

        st.write("---")

        if st.session_state.conversations:
            st.markdown("**📚 محادثاتك السابقة:**")
            for conv in st.session_state.conversations[:10]:
                topic = conv.get("topic", "محادثة")
                if st.button(f"💬 {topic[:25]}", key=f"conv_{topic}"):
                    st.session_state.chat_history = conv.get("messages", [])
                    st.session_state.current_topic = topic
                    st.session_state.current_role = conv.get("role", "free")
                    st.rerun()
            st.write("---")

        if st.button("➕ محادثة جديدة", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.current_topic = None
            st.rerun()

        if st.button("🗑️ مسح المحادثة الحالية", use_container_width=True):
            if st.session_state.current_topic:
                try:
                    db.collection("users").document(st.session_state.user_id).collection("conversations").document(st.session_state.current_topic).delete()
                except: pass
            st.session_state.chat_history = []
            st.session_state.current_topic = None
            st.session_state.conversations = load_conversations(st.session_state.user_id)
            st.success("✅ تم المسح!")
            st.rerun()

        if st.button("🗑️ مسح كل المحادثات", use_container_width=True):
            try:
                convs = db.collection("users").document(st.session_state.user_id).collection("conversations").stream()
                for conv in convs:
                    conv.reference.delete()
            except: pass
            st.session_state.chat_history = []
            st.session_state.current_topic = None
            st.session_state.conversations = []
            st.success("✅ تم مسح كل المحادثات!")
            st.rerun()

        if st.button("🚪 تسجيل الخروج", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.title("⚖️ قاعة الاستشارات القانونية")

    # اختيار الباقة
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🟢 مجانية", use_container_width=True):
            st.session_state.current_role = "free"
            st.session_state.show_code_input = None
            st.rerun()
    with col2:
        if st.button("🔵 Pro - 20$", use_container_width=True):
            st.session_state.show_code_input = "pro"
            st.rerun()
    with col3:
        if st.button("👑 VIP - 50$", use_container_width=True):
            st.session_state.show_code_input = "vip"
            st.rerun()

    # خانة كلمة السر
    if st.session_state.show_code_input == "pro":
        st.info("💬 للاشتراك في باقة Pro بـ 20$، تواصل على واتساب: **01094130731** وسنرسل لك رقم التحويل وكود التفعيل.")
        code = st.text_input("🔑 أدخل كود تفعيل Pro:", type="password", key="pro_code")
        if code:
            if code in ALLOWED_PRO_CODES:
                st.session_state.current_role = "pro"
                st.session_state.show_code_input = None
                st.success("✅ تم التفعيل! أهلاً بك في باقة Pro")
                st.rerun()
            else:
                st.session_state.failed_attempts += 1
                st.error(f"❌ كود خاطئ. متبقي {5 - st.session_state.failed_attempts} محاولات.")

    elif st.session_state.show_code_input == "vip":
        st.warning("👑 للاشتراك في باقة VIP بـ 50$، تواصل على واتساب: **01094130731** وسنرسل لك رقم التحويل وكود التفعيل.")
        code = st.text_input("👑 أدخل كود تفعيل VIP:", type="password", key="vip_code")
        if code:
            if code in ALLOWED_VIP_CODES:
                st.session_state.current_role = "vip"
                st.session_state.show_code_input = None
                st.success("👑 مرحباً بك! باقة VIP مفعّلة")
                st.rerun()
            else:
                st.session_state.failed_attempts += 1
                st.error(f"❌ كود خاطئ. متبقي {5 - st.session_state.failed_attempts} محاولات.")

    st.write("---")

    # عرض المحادثات
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'><b>👤 سؤالك:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ai-bubble'><b>⚖️ المستشار:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

    # حقل الإدخال
    if prompt := st.chat_input("اكتب سؤالك أو وقائع القضية بالتفصيل..."):
        clean_prompt = sanitize_input(prompt)
        if clean_prompt:
            if not st.session_state.current_topic:
                st.session_state.current_topic = generate_topic(clean_prompt)

            st.session_state.chat_history.append({"role": "user", "content": clean_prompt})

            with st.spinner("⚖️ المستشار يحلل القضية..."):
                answer = ask_law_ai(clean_prompt, st.session_state.current_role)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})

            save_conversation(st.session_state.user_id, st.session_state.current_topic, st.session_state.chat_history, st.session_state.current_role)
            st.session_state.conversations = load_conversations(st.session_state.user_id)
            st.rerun()