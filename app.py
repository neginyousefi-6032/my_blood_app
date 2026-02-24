import streamlit as st

# تنظیمات ظاهر صفحه
st.set_page_config(page_title="سیستم تحلیل هوشمند سلامت", layout="wide")

# استایل‌دهی راست‌چین برای زبان فارسی
st.markdown("""
    <style>
    .reportview-container .main .block-container { direction: rtl; }
    div.stButton > button { width: 100%; border-radius: 10px; height: 3em; background-color: #ff4b4b; color: white; }
    h1, h2, h3 { text-align: right; font-family: 'Tahoma'; }
    .stNumberInput, .stSelectbox { text-align: right; }
    </style>
    """, unsafe_import_allowed=True)

st.title("🏥 سامانه پیش‌بینی و تحلیل وضعیت سلامت")
st.write("لطفاً اطلاعات آزمایش خون و سوابق خانوادگی را وارد کنید تا تحلیل انجام شود.")

# ایجاد ستون‌ها برای ظاهر بهتر
col1, col2 = st.columns(2)

with col1:
    st.header("🔬 نتایج آزمایش خون")
    glucose = st.number_input("قند خون ناشتا (mg/dL)", min_value=50, max_value=300, value=100)
    cholesterol = st.number_input("کلسترول کل (mg/dL)", min_value=100, max_value=400, value=180)
    hemoglobin = st.number_input("هموگلوبین (g/dL)", min_value=5.0, max_value=20.0, value=14.0, step=0.1)

with col2:
    st.header("🧬 سوابق و اطلاعات فردی")
    age = st.number_input("سن", min_value=1, max_value=120, value=30)
    family_history = st.selectbox("سابقه بیماری ارثی در خانواده؟", ["ندارد", "دیابت", "بیماری قلبی", "کم‌خونی"])
    gender = st.radio("جنسیت", ["مرد", "زن"])

# دکمه تحلیل
if st.button("شروع تحلیل هوشمند"):
    st.divider()
    st.subheader("📋 نتیجه تحلیل و پیش‌بینی:")
    
    results = []
    risks = []

    # منطق تحلیل (Expert System Logic)
    # تحلیل دیابت
    if glucose > 126:
        results.append("🔴 قند خون شما در محدوده دیابت است.")
        if family_history == "دیابت":
            risks.append("⚠️ ریسک ابتلای قطعی به دیابت به دلیل سابقه خانوادگی بسیار بالاست.")
    elif 100 <= glucose <= 126:
        results.append("🟡 شما در مرحله پیش‌دیابت هستید.")

    # تحلیل کلسترول
    if cholesterol > 240:
        results.append("🔴 سطح کلسترول بسیار بالاست.")
        if family_history == "بیماری قلبی":
            risks.append("⚠️ خطر سکته قلبی یا گرفتگی عروق در آینده وجود دارد.")

    # تحلیل کم‌خونی
    if (gender == "مرد" and hemoglobin < 13.5) or (gender == "زن" and hemoglobin < 12):
        results.append("🔴 شواهدی از کم‌خونی (Anemia) مشاهده شد.")

    # نمایش نتایج
    if not results and not risks:
        st.success("✅ طبق تحلیل اولیه، وضعیت فاکتورهای شما نرمال است.")
    else:
        for res in results:
            st.info(res)
        for risk in risks:
            st.warning(risk)
            
    st.info("💡 توجه: این یک تحلیل آماری است و برای تشخیص نهایی حتماً باید به پزشک مراجعه کنید.")

