

import streamlit as st

# تنظیمات اصلی صفحه
st.set_page_config(page_title="Health Analyzer", page_icon="🏥")

# ظاهر سازی فارسی و استایل‌دهی
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; text-align: right; }
    .stNumberInput, .stSelectbox, .stTextInput { text-align: right; }
    </style>
    """, unsafe_import_allowed=True)

st.title("🩺 سامانه تحلیل هوشمند آزمایش خون و ژنتیک")
st.write("این برنامه بر اساس الگوریتم‌های پیش‌بینی، احتمال ابتلای شما به بیماری‌ها را تحلیل می‌کند.")

# بخش ورودی اطلاعات
with st.expander("👤 مشخصات فردی و سوابق خانوادگی", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("سن شما", 1, 100, 25)
        gender = st.selectbox("جنسیت", ["مرد", "زن"])
    with col2:
        family_history = st.multiselect("سابقه بیماری در خانواده (درجه ۱ و ۲)", 
                                        ["دیابت نوع ۲", "فشار خون بالا", "بیماری قلبی", "چربی خون"])

with st.expander("🔬 نتایج آزمایش خون (مقادیر عددی)", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        fbs = st.number_input("قند خون (FBS)", 50, 300, 95)
    with c2:
        ldl = st.number_input("کلسترول بد (LDL)", 50, 250, 110)
    with c3:
        hgb = st.number_input("هموگلوبین (Hb)", 5.0, 20.0, 13.0)

# دکمه پردازش
if st.button("شروع تحلیل و پیش‌بینی"):
    st.divider()
    
    # منطق تحلیل (Core Logic)
    has_risk = False
    
    # ۱. تحلیل دیابت
    if fbs >= 126 or "دیابت نوع ۲" in family_history:
        st.error("🚨 هشدار دیابت:")
        if fbs >= 126: st.write("- قند خون شما در محدوده دیابت است.")
        if "دیابت نوع ۲" in family_history: st.write("- سابقه ارثی، ریسک ابتلا را در سنین بالاتر ۳ برابر می‌کند.")
        has_risk = True

    # ۲. تحلیل بیماری قلبی
    if ldl > 160 or "بیماری قلبی" in family_history:
        st.warning("⚠️ بررسی سلامت قلب:")
        if ldl > 160: st.write("- سطح LDL بالا است؛ خطر رسوب در عروق وجود دارد.")
        if "بیماری قلبی" in family_history: st.write("- به دلیل سابقه خانوادگی، چک‌آپ سالانه قلب توصیه می‌شود.")
        has_risk = True

    # ۳. تحلیل کم‌خونی
    if (gender == "مرد" and hgb < 13) or (gender == "زن" and hgb < 12):
        st.info("ℹ️ تحلیل هموگلوبین:")
        st.write("- سطح هموگلوبین پایین‌تر از حد نرمال است (احتمال کم‌خونی).")
        has_risk = True

    if not has_risk:
        st.success("✅ تبریک! فاکتورهای شما در محدوده ایمن قرار دارد.")

st.sidebar.markdown("---")
st.sidebar.info("این پروژه صرفاً جنبه تحقیقاتی دارد.")
