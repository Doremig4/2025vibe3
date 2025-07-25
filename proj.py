import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="자살률 통계 시각화", layout="wide")
st.title("📊 자살률(연령별) 통계 시각화")
st.write("출처: 통계청 | 단위: 명, 10만명당 명")

uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")

if uploaded_file:
    try:
        # 4번째 줄부터 데이터 시작, 첫 3줄은 skip
        df = pd.read_csv(uploaded_file, encoding='utf-8', skiprows=3)
        # 미상, -, 등은 NaN 처리
        df = df.replace("-", pd.NA)
        # 숫자형 변환
        df["자살 사망자수 (명)"] = pd.to_numeric(df["자살 사망자수 (명)"], errors="coerce")
        df["자살률 (10만명당 명)"] = pd.to_numeric(df["자살률 (10만명당 명)"], errors="coerce")
        # 미상, 합계 등 제외
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
