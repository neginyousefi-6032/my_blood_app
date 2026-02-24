import streamlit as st
import pytesseract
from PIL import Image
import re
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
st.write("آپلود تصویر آزمایش برای تحلیل کامل وضعیت سلامت")

uploaded_file = st.file_uploader("📤 تصویر آزمایش خون را آپلود کنید", type=["png","jpg","jpeg"])

# -------- Helper --------
def extract_value(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return float(match.group(1)) if match else None

def check_range(name, value, low, high):
    if value is None:
        return None, 0
    if value < low:
        return f"🔴 {name} پایین‌تر از حد نرمال است ({value})", -1
    elif value > high:
        return f"🔴 {name} بالاتر از حد نرمال است ({value})", -1
    else:
        return f"🟢 {name} در محدوده نرمال قرار دارد ({value})", 1

if uploaded_file:

    image = Image.open(uploaded_file)
    st.image(image, caption="تصویر آپلود شده", use_column_width=True)

    text = pytesseract.image_to_string(image)

    # -------- Extract Factors --------
    glucose = extract_value(r"Glucose\s+(\d+)", text)
    cholesterol = extract_value(r"Cholesterol\s+(\d+)", text)
    triglyceride = extract_value(r"Triglyceride\s+(\d+)", text)
    hgb = extract_value(r"Hb\s+(\d+\.?\d*)", text)
    wbc = extract_value(r"WBC\s+(\d+\.?\d*)", text)
    plt = extract_value(r"Platelet[s]?\s+(\d+)", text)
    creatinine = extract_value(r"Creatinine\s+(\d+\.?\d*)", text)
    alt = extract_value(r"ALT\s+(\d+)", text)
    ast = extract_value(r"AST\s+(\d+)", text)

    st.divider()
    st.subheader("📊 داده‌های استخراج شده")

    data = {
        "Glucose": glucose,
        "Cholesterol": cholesterol,
        "Triglyceride": triglyceride,
        "Hemoglobin": hgb,
        "WBC": wbc,
        "Platelets": plt,
        "Creatinine": creatinine,
        "ALT": alt,
        "AST": ast
    }

    df = pd.DataFrame.from_dict(data, orient='index', columns=["Value"])
    st.dataframe(df)

    st.divider()
    st.subheader("🧠 گزارش کلینیکی جامع")

    health_score = 0
    report = []

    # ---------------- Metabolic ----------------
    report.append("### 🔬 تحلیل متابولیک")
    for name, val, low, high in [
        ("قند خون", glucose, 70, 99),
        ("کلسترول", cholesterol, 0, 200),
        ("تری‌گلیسرید", triglyceride, 0, 150)
    ]:
        result, score = check_range(name, val, low, high)
        if result:
            report.append(result)
            health_score += score

    # ---------------- CBC ----------------
    report.append("### 🩸 تحلیل CBC")
    for name, val, low, high in [
        ("هموگلوبین", hgb, 12, 16),
        ("WBC", wbc, 4000, 11000),
        ("پلاکت", plt, 150000, 450000)
    ]:
        result, score = check_range(name, val, low, high)
        if result:
            report.append(result)
            health_score += score

    # ---------------- Kidney & Liver ----------------
    report.append("### 🏥 عملکرد کبد و کلیه")
    for name, val, low, high in [
        ("کراتینین", creatinine, 0.6, 1.3),
        ("ALT", alt, 0, 40),
        ("AST", ast, 0, 40)
    ]:
        result, score = check_range(name, val, low, high)
        if result:
            report.append(result)
            health_score += score

    # --------- Health Score ----------
    st.divider()
    st.subheader("📈 امتیاز کلی سلامت")

    if health_score >= 6:
        st.success(f"🟢 وضعیت کلی بسیار مطلوب است | امتیاز سلامت: {health_score}")
    elif 2 <= health_score < 6:
        st.warning(f"🟡 وضعیت متوسط - نیاز به اصلاح سبک زندگی | امتیاز سلامت: {health_score}")
    else:
        st.error(f"🔴 ریسک سلامت بالا - توصیه به مراجعه تخصصی | امتیاز سلامت: {health_score}")

    st.divider()
    st.subheader("📋 گزارش تفصیلی")

    for line in report:
        st.write(line)

    # --------- Preventive Advice ----------
    st.divider()
    st.subheader("💡 پیشنهادهای پیشگیری و بهبود سلامت")

    st.write("""
- 🥗 رژیم غذایی کم‌چرب و کم‌قند
- 🏃 حداقل 150 دقیقه فعالیت بدنی در هفته
- 🚭 پرهیز از مصرف دخانیات
- 💧 مصرف آب کافی
- 🩺 انجام چکاپ دوره‌ای هر 6 ماه
    """)

    st.caption("⚠️ این سیستم ابزار تحلیل آماری است و جایگزین تشخیص پزشک نمی‌باشد.")

