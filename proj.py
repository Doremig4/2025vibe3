import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 연령대별 자살률 시각화 (2023년 기준)")

# CSV 불러오기
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding='cp949')

    # 데이터 클리닝
    df_clean = df.iloc[2:].copy()
    df_clean.columns = ['연령별(1)', '연령별(2)', '자살 사망자수', '자살률']
    df_clean = df_clean.reset_index(drop=True)
    df_clean['자살률'] = pd.to_numeric(df_clean['자살률'], errors='coerce')
    df_clean = df_clean.dropna(subset=['자살률'])

    # '합계'의 연령별 자살률만 추출
    filtered_df = df_clean[df_clean['연령별(1)'] == '합계']

    # 시각화
    st.subheader("연령대별 자살률 (단위: 10만명당 명)")
    fig = px.bar(
        filtered_df,
        x='연령별(2)',
        y='자살률',
        title='연령대별 자살률 (2023년)',
        labels={'자살률': '자살률 (10만명당 명)', '연령별(2)': '연령대'}
    )
    st.plotly_chart(fig, use_container_width=True)

    # 데이터 테이블도 함께 표시
    st.dataframe(filtered_df[['연령별(2)', '자살률']], use_container_width=True)
