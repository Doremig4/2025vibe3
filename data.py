import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import csv
import os

st.set_page_config(page_title="서울시 연령별 인구 시각화", layout="wide")

st.title("🧓 서울특별시 연령별 인구 (2025년 6월)")
st.write("출처: 통계청 | 단위: 명")

uploaded_file = st.file_uploader("📂 CSV 파일 업로드 (남녀구분)", type="csv")

# 파일 경로 지정
default_csv = "202506_202506_연령별인구현황_월간 남녀구분.csv"

if uploaded_file:
    file_to_read = uploaded_file
elif os.path.exists(default_csv):
    file_to_read = default_csv
else:
    file_to_read = None

if file_to_read:
    try:
        columns = ["연령별(1)", "연령별(2)", "자살 사망자수 (명)", "자살률 (10만명당 명)"]
        df = pd.read_csv(uploaded_file, encoding='utf-8', skiprows=3, names=columns)
        df = df.replace("-", pd.NA)
        df["자살 사망자수 (명)"] = pd.to_numeric(df["자살 사망자수 (명)"], errors="coerce")
        df["자살률 (10만명당 명)"] = pd.to_numeric(df["자살률 (10만명당 명)"], errors="coerce")
        df = df[~df["연령별(2)"].isin(["미상", "소계"])]

        st.dataframe(df)

        tab1, tab2 = st.tabs(["자살 사망자수", "자살률"])
        with tab1:
            fig1 = px.bar(df, x="연령별(2)", y="자살 사망자수 (명)", title="연령별 자살 사망자수 (명)")
            st.plotly_chart(fig1, use_container_width=True)
        with tab2:
            fig2 = px.bar(df, x="연령별(2)", y="자살률 (10만명당 명)", title="연령별 자살률 (10만명당 명)")
            st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    st.info("왼쪽에서 CSV 파일을 업로드해 주세요.")
