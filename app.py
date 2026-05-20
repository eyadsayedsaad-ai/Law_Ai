import streamlit as st
from google import genai
import time
from streamlit_cookies_controller import CookieController

controller = CookieController()

# =================================================================
# 🔑 الأكواد الجديدة (نمط: 1e_hf4)
# =================================================================
ALLOWED_PRO_CODES = [
    "1a_bc2", "2b_cd3", "3c_de4", "4d_ef5", "5e_fg6", "6f_gh7", "7g_hi8", "8h_ij9", "9i_jk1", "1j_kl2",
    "2k_lm3", "3l_mn4", "4m_no5", "5n_op6", "6o_pq7", "7p_qr8", "8q_rs9", "9r_st1", "1s_tu2", "2t_uv3",
    "3u_vw4", "4v_wx5", "5w_xy6", "6x_yz7", "7y_za8", "8z_ab9", "1a_cd2", "2b_de3", "3c_ef4", "4d_fg5",
    "5e_gh6", "6f_hi7", "7g_ij8", "8h_jk9", "9i_kl1", "1j_lm2", "2k_mn3", "3l_no4", "4m_op5", "5n_pq6",
    "6o_qr7", "7p_rs8", "8q_st9", "9r_tu1", "1s_uv2", "2t_vw3", "3u_wx4", "4v_xy5", "5w_yz6", "6x_za7",
    "7y_ab8", "8z_bc9", "1a_de2", "2b_ef3", "3c_fg4", "4d_gh5", "5e_hi6", "6f_ij7", "7g_jk8", "8h_kl9",
    "9i_lm1", "1j_mn2", "2k_no3", "3l_op4", "4m_pq5", "5n_qr6", "6o_rs7", "7p_st8", "8q_tu9", "9r_uv1",
    "1s_vw2", "2t_wx3", "3u_xy4", "4v_yz5", "5w_za6", "6x_ab7", "7y_bc8", "8z_cd9", "1a_ef2", "2b_fg3",
    "3c_gh4", "4d_hi5", "5e_ij6", "6f_jk7", "7g_kl8", "8h_lm9", "9i_mn1", "1j_no2", "2k_op3", "3l_pq4",
    "4m_qr5", "5n_rs6", "6o_st7", "7p_tu8", "8q_uv9", "9r_vw1", "1s_wx2", "2t_xy3", "3u_yz4", "4v_za5"
]

ALLOWED_VIP_CODES = [
    "9a_bc1", "8b_cd2", "7c_de3", "6d_ef4", "5e_fg5", "4f_gh6", "3g_hi7", "2h_ij8", "1i_jk9", "0j_kl0",
    "9k_lm1", "8l_mn2", "7m_no3", "6n_op4", "5o_pq5", "4p_qr6", "3q_rs7", "2r_st8", "1s_tu9", "0t_uv0",
    "9u_vw1", "8v_wx2", "7w_xy3", "6x_yz4", "5y_za5", "4z_ab6", "3a_bc7", "2b_cd8", "1c_de9", "0d_ef0",
    "9e_fg1", "8f_gh2", "7g_hi3", "6h_ij4", "5i_jk5", "4j_kl6", "3k_lm7", "2l_mn8", "1m_no9", "0n_op0",
    "9o_pq1", "8p_qr2", "7q_rs3", "6r_st4", "5s_tu5", "4t_uv6", "3u_vw7", "2v_wx8", "1w_xy9", "0x_yz0",
    "9y_za1", "8z_ab2", "7a_bc3", "6b_cd4", "5c_de5", "4d_ef6", "3e_fg7", "2f_gh8", "1g_hi9", "0h_ij0",
    "9i_jk1", "8j_kl2", "7k_lm3", "6l_mn4", "5m_no5", "4n_op6", "3o_pq7", "2p_qr8", "1q_rs9", "0r_st0",
    "9s_tu1", "8t_uv2", "7u_vw3", "6v_wx4", "5w_xy5", "4x_yz6", "3y_za7", "2z_ab8", "1a_bc9", "0b_cd0",
    "9c_de1", "8d_ef2", "7e_fg3", "6f_gh4", "5g_hi5", "4h_ij6", "3i_jk7", "2j_kl8", "1k_lm9", "0l_mn0",
    "9m_no1", "8n_op2", "7o_pq3", "6p_qr4", "5q_rs5", "4r_st6", "3s_tu7", "2t_uv8", "1u_vw9", "0v_wx0"
]

CASH_MESSAGE = "❌ عذراً، هذا الكود غير صحيح، أو تم تفعيله مسبقاً!"

# =================================================================
# ⚙️ إعدادات الذكاء الاصطناعي
# =================================================================
try:
    GENAI_API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=GENAI_API_KEY)
except Exception:
    st.error("⚠️ خطأ في إعدادات API.")

def ask_gemini_latest(prompt):
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text if response.text else "⚠️ خطأ."
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

st.set_page_config(page_title="LAW AI", page_icon="⚖️", layout="centered")

# إدارة الحالة
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "active_users" not in st.session_state: st.session_state.active_users = 0

# --- لوحة الإدارة ---
st.sidebar.subheader("⚙️ لوحة الإدارة")
admin_pass = st.sidebar.text_input("باسورد المدير:", type="password")
if admin_pass == "admin123":
    st.sidebar.write(f"👥 المستخدمون الأونلاين: {st.session_state.active_users}")

# --- الشاشات ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>⚖️ LAW AI</h1>", unsafe_allow_html=True)
    if st.button("🌐 تسجيل الدخول للمنصة", use_container_width=True):
        st.session_state.logged_in = True
        st.session_state.active_users += 1
        st.rerun()
else:
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.active_users -= 1
        st.rerun()

    st.title("⚖️ منصة LAW AI الرقمية")
    package = st.radio("الباقات:", ["الخط السريع (المجاني) 🟢", "المفكر (Pro) 🔵", "المستشار الملكي (VIP) 👑"])

    is_premium = False; role = "free"
    saved = controller.get('user_active_code')

    if "Pro" in package:
        if saved in ALLOWED_PRO_CODES: is_premium=True; role="pro"
        else:
            auth = st.text_input("🔑 كود Pro:", type="password")
            if auth in ALLOWED_PRO_CODES: controller.set('user_active_code', auth); st.rerun()
            elif auth: st.error(CASH_MESSAGE)
    elif "VIP" in package:
        if saved in ALLOWED_VIP_CODES: is_premium=True; role="vip"
        else:
            auth = st.text_input("🔑 كود VIP:", type="password")
            if auth in ALLOWED_VIP_CODES: controller.set('user_active_code', auth); st.rerun()
            elif auth: st.error(CASH_MESSAGE)
    else: is_premium=True; role="free"

    if is_premium:
        for m in st.session_state.chat_history:
            with st.chat_message(m["role"]): st.write(m["content"])
        u_in = st.chat_input("اكتب سؤالك...")
        if u_in:
            st.session_state.chat_history.append({"role":"user", "content":u_in})
            res = ask_gemini_latest(f"أنت مستشار قانوني ({role}): {u_in}")
            st.session_state.chat_history.append({"role":"assistant", "content":res})
            st.rerun()