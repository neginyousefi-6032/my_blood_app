import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Clinical Blood Analyzer Pro", layout="wide")

# ---------------- Modern Medical UI ----------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0e1117;
    color: white;
    direction: rtl;
    text-align: right;
    font-family: Tahoma;
}
.stButton>button {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color:white;
    font-size:18px;
    border-radius:12px;
    height:3em;
    width:100%;
    border:none;
}
.block-container {
    padding-top:2rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🧬 سیستم پیشرفته تحلیل کلینیکی آزمایش خون")
st.write("مقادیر آزمایش خون خود را وارد کنید تا تحلیل جامع انجام شود")

st.divider()

# ----------- Layout -----------
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🩸 CBC")
    hgb = st.number_input("Hemoglobin", 0.0, 25.0, 14.0)
    wbc = st.number_input("WBC", 0, 50000, 7000)
    plt = st.number_input("Platelets", 0, 1000000, 250000)

with col2:
    st.subheader("🔬 متابولیک")
    glucose = st.number_input("Glucose", 0, 500, 90)
    cholesterol = st.number_input("Cholesterol", 0, 500, 180)
    triglyceride = st.number_input("Triglyceride", 0, 1000, 120)

with col3:
    st.subheader("🏥 کبد و کلیه")
    creatinine = st.number_input("Creatinine", 0.0, 10.0, 1.0)
    alt = st.number_input("ALT", 0, 500, 25)
    ast = st.number_input("AST", 0, 500, 22)

st.divider()

def check_range(name, value, low, high):
    if value < low:
        return f"🔴 {name} پایین‌تر از حد نرمال است ({value})", -1
    elif value > high:
        return f"🔴 {name} بالاتر از حد نرمال است ({value})", -1
    else:
        return f"🟢 {name} در محدوده نرمال قرار دارد ({value})", 1

if st.button("🚀 انجام تحلیل پیشرفته"):

    health_score = 0
    report = []

    st.subheader("📊 جدول مقادیر ثبت شده")

    df = pd.DataFrame({
        "Factor": ["HGB","WBC","Platelet","Glucose","Cholesterol","Triglyceride","Creatinine","ALT","AST"],
        "Value": [hgb,wbc,plt,glucose,cholesterol,triglyceride,creatinine,alt,ast]
    })

    st.dataframe(df)

    st.divider()
    st.subheader("🧠 گزارش کلینیکی جامع")

    # CBC
    report.append("### 🩸 تحلیل CBC")
    for name, val, low, high in [
        ("هموگلوبین", hgb, 12, 16),
        ("WBC", wbc, 4000, 11000),
        ("پلاکت", plt, 150000, 450000)
    ]:
        result, score = check_range(name, val, low, high)
        report.append(result)
        health_score += score

    # Metabolic
    report.append("### 🔬 تحلیل متابولیک")
    for name, val, low, high in [
        ("قند خون", glucose, 70, 99),
        ("کلسترول", cholesterol, 0, 200),
        ("تری‌گلیسرید", triglyceride, 0, 150)
    ]:
        result, score = check_range(name, val, low, high)
        report.append(result)
        health_score += score

    # Liver & Kidney
    report.append("### 🏥 عملکرد کبد و کلیه")
    for name, val, low, high in [
        ("کراتینین", creatinine, 0.6, 1.3),
        ("ALT", alt, 0, 40),
        ("AST", ast, 0, 40)
    ]:
        result, score = check_range(name, val, low, high)
        report.append(result)
        health_score += score

    # Health Score
    st.divider()
    st.subheader("📈 امتیاز کلی سلامت")

    if health_score >= 7:
        st.success(f"🟢 وضعیت کلی بسیار مطلوب است | Health Score: {health_score}")
    elif 3 <= health_score < 7:
        st.warning(f"🟡 وضعیت متوسط - نیاز به اصلاح سبک زندگی | Health Score: {health_score}")
    else:
        st.error(f"🔴 ریسک سلامت بالا - توصیه به مراجعه تخصصی | Health Score: {health_score}")

    st.divider()
    st.subheader("📋 گزارش تفصیلی")

    for line in report:
        st.write(line)

    st.divider()
    st.subheader("💡 پیشنهادهای پیشگیری")

    st.write("""
- 🥗 رژیم غذایی سالم (کاهش قند و چربی اشباع)
- 🏃 150 دقیقه فعالیت بدنی در هفته
- 💧 مصرف آب کافی
- 🧂 کاهش نمک
- 🚭 عدم مصرف دخانیات
- 🩺 چکاپ دوره‌ای هر 6 ماه
    """)

    st.caption("⚠️ این سیستم ابزار تحلیل آماری است و جایگزین تشخیص پزشک نمی‌باشد.") 

