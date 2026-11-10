import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="منصة ذكاء الأعمال لمؤشرات رؤية السعودية 2030",
    layout="wide"
)

# تحميل البيانات
df = pd.read_csv("vision2030_bi_data.csv")

# حساب نسبة الإنجاز إذا لم تكن موجودة
if "نسبة_الإنجاز" not in df.columns:
    df["نسبة_الإنجاز"] = (
        df["القيمة"] / df["المستهدف_2030"] * 100
    )

# تنسيق الصفحة بالعربي
st.markdown("""
<style>
.main {
    direction: rtl;
    text-align: right;
}
h1 {
    text-align: center;
    font-size: 38px !important;
    margin-bottom: 10px;
}
h3 {
    text-align: center;
    color: #315B75;
    margin-bottom: 35px;
}
.kpi-card {
    background: linear-gradient(135deg, #F4F8FA, #E7F2F7);
    padding: 25px 15px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #D7E5EC;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    min-height: 145px;
}
.kpi-title {
    font-size: 17px;
    color: #315B75;
    font-weight: bold;
    margin-bottom: 15px;
}
.kpi-value {
    font-size: 36px;
    font-weight: bold;
    color: #173F5F;
}
.section-title {
    text-align: right;
    color: #173F5F;
    font-size: 24px;
    font-weight: bold;
    margin-top: 40px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# العنوان
st.title("منصة ذكاء الأعمال لمؤشرات رؤية السعودية 2030")

st.markdown(
    "<h3>لوحة مؤشرات الأداء الرئيسية</h3>",
    unsafe_allow_html=True
)

# فلتر المحور
st.markdown(
    '<div class="section-title">تصفية البيانات حسب المحور</div>',
    unsafe_allow_html=True
)

axis_options = ["جميع المحاور"] + sorted(
    df["المحور"].dropna().unique().tolist()
)

selected_axis = st.selectbox("اختر المحور:", axis_options)

if selected_axis == "جميع المحاور":
    filtered_df = df.copy()
else:
    filtered_df = df[df["المحور"] == selected_axis].copy()

# حساب المؤشرات حسب الفلتر
total_indicators = len(filtered_df)

achieved_indicators = (
    (filtered_df["القيمة"] >= filtered_df["المستهدف_2030"])
    & filtered_df["المستهدف_2030"].notna()
).sum()

below_target = (
    (filtered_df["القيمة"] < filtered_df["المستهدف_2030"])
    & filtered_df["المستهدف_2030"].notna()
).sum()

average_achievement = filtered_df["نسبة_الإنجاز"].mean()

# بطاقات KPI
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">إجمالي المؤشرات</div>
        <div class="kpi-value">{total_indicators}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">المؤشرات المحققة للمستهدف</div>
        <div class="kpi-value">{achieved_indicators}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">المؤشرات الأقل من المستهدف</div>
        <div class="kpi-value">{below_target}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">متوسط نسبة الإنجاز</div>
        <div class="kpi-value">{average_achievement:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

# الرسم البياني
st.markdown(
    '<div class="section-title">مقارنة القيمة الحالية بالمستهدف لعام 2030</div>',
    unsafe_allow_html=True
)

chart_df = filtered_df.dropna(
    subset=["المستهدف_2030"]
).set_index("المؤشر")[["القيمة", "المستهدف_2030"]]

chart_df = filtered_df.set_index("المؤشر")[
    ["القيمة", "المستهدف_2030"]
]

chart_df = chart_df.rename(columns={
    "القيمة": "القيمة الحالية",
    "المستهدف_2030": "المستهدف 2030"
})

if not chart_df.empty:
    st.bar_chart(chart_df)
else:
    st.info("لا توجد بيانات متاحة لهذا المحور.")

# عرض البيانات
st.markdown(
    '<div class="section-title">بيانات مؤشرات رؤية السعودية 2030</div>',
    unsafe_allow_html=True
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

