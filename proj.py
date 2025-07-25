import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="자살률(연령별) 통계 시각화", layout="wide")
st.title("📊 자살률(연령별) 통계 시각화")
st.write("출처: 통계청 | 단위: 명")

csv_path = "자살률(연령별)_20250725130840.csv"
columns = ["연령별(1)", "연령별(2)", "자살 사망자수 (명)", "자살률"]
df = pd.read_csv(csv_path, encoding='utf-8', skiprows=3, names=columns)
df = df.replace("-", pd.NA)
df["자살 사망자수 (명)"] = pd.to_numeric(df["자살 사망자수 (명)"], errors="coerce")
df["자살률"] = pd.to_numeric(df["자살률"], errors="coerce")
df = df[~df["연령별(2)"].isin(["미상", "소계"])]

st.subheader("📄 데이터 미리보기")
st.dataframe(df, use_container_width=True)

st.subheader("연령별 자살 사망자수 (명)")
fig = px.bar(df, x="연령별(2)", y="자살 사망자수 (명)", title="연령별 자살 사망자수 (명)")
st.plotly_chart(fig, use_container_width=True)

    