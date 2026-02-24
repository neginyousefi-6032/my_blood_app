import streamlit as st

# تنظیمات صفحه
st.set_page_config(
    page_title="سیستم تحلیل هوشمند سلامت",
    page_icon="🏥",
    layout="wide"
)

# استایل حرفه‌ای RTL
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        direction: rtl;
        text-align: right;
        font-family: Tahoma;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background: linear-gradient(to right, #ff4b4b, #ff6b6b);
        color: white;
        font-size: 18px;
        font-weight: bold;
        border: none;
    }

    .stNumberInput input {
        text-align: right;
    }

    .stSelectbox div, .stRadio div {
        text-align: right;
    }

    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# عنوان
st.title("🏥 سامانه پیش‌بینی و تحلیل وضعیت سلامت")
st.write("لطفاً اطلاعات آزمایش خون و سوابق خانوادگی را وارد کنید تا تحلیل انجام شود.")

st.divider()

# ستون‌بندی
col1, col2 = st.columns(2)

with col1:
    st.header("🔬 نتایج آزمایش خون")
    glucose = st.number_input("قند خون ناشتا (mg/dL)", 50, 300, 100)
    cholesterol = st.number_input("کلسترول کل (mg/dL)", 100, 400, 180)
    hemoglobin = st.number_input("هموگلوبین (g/dL)", 5.0, 20.0, 14.0, step=0.1)

with col2:
    st.header("🧬 سوابق و اطلاعات فردی")
    age = st.number_input("سن", 1, 120, 30)
    family_history = st.selectbox(
        "سابقه بیماری ارثی در خانواده؟",
        ["ندارد", "دیابت", "بیماری قلبی", "کم‌خونی"]
    )
    gender = st.radio("جنسیت", ["مرد", "زن"])

st.divider()

# دکمه تحلیل
if st.button("🚀 شروع تحلیل هوشمند"):

    st.subheader("📋 نتیجه تحلیل و پیش‌بینی:")

    results = []
    risks = []

    # تحلیل دیابت
    if glucose > 126:
        results.append("🔴 قند خون شما در محدوده دیابت است.")
        if family_history == "دیابت":
            risks.append("⚠️ ریسک ابتلا به دیابت به دلیل سابقه خانوادگی بسیار بالاست.")
    elif 100 <= glucose <= 126:
        results.append("🟡 شما در مرحله پیش‌دیابت هستید.")

    # تحلیل کلسترول
    if cholesterol > 240:
        results.append("🔴 سطح کلسترول شما بسیار بالاست.")
        if family_history == "بیماری قلبی":
            risks.append("⚠️ خطر سکته قلبی یا گرفتگی عروق در آینده افزایش یافته است.")

    # تحلیل کم‌خونی
    if (gender == "مرد" and hemoglobin < 13.5) or (gender == "زن" and hemoglobin < 12):
        results.append("🔴 شواهدی از کم‌خونی (Anemia) مشاهده شد.")
        if family_history == "کم‌خونی":
            risks.append("⚠️ سابقه خانوادگی احتمال کم‌خونی مزمن را افزایش می‌دهد.")

    # تحلیل سن (ریسک عمومی)
    if age > 50:
        risks.append("⚠️ با توجه به سن بالای ۵۰ سال، انجام چکاپ منظم توصیه می‌شود.")

    # نمایش خروجی
    if not results and not risks:
        st.success("✅ طبق تحلیل اولیه، وضعیت فاکتورهای شما نرمال است.")
    else:
        for res in results:
            st.info(res)
        for risk in risks:
            st.warning(risk)

    st.divider()
    st.caption("💡 توجه: این تحلیل مبتنی بر منطق آماری اولیه است و جایگزین تشخیص پزشک نیست.")

