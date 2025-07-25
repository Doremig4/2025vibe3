import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 연령대별 자살자 수 시각화 (2023년 기준)")

# CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding='cp949')

    # 데이터 정리
    df_clean = df.iloc[2:].copy()
    df_clean.columns = ['연령별(1)', '연령별(2)', '자살 사망자수', '자살률']
    df_clean = df_clean.reset_index(drop=True)
    df_clean['자살 사망자수'] = pd.to_numeric(df_clean['자살 사망자수'], errors='coerce')
    df_clean = df_clean.dropna(subset=['자살 사망자수'])

    # '합계' 기준 + '소계' 제외
    filtered_df = df_clean[(df_clean['연령별(1)'] == '합계') & (df_clean['연령별(2)'] != '소계')]

    # 바 차트 생성
    st.subheader("연령대별 자살자 수 (단위: 명)")
    fig = px.bar(
        filtered_df,
        x='연령별(2)',
        y='자살 사망자수',
        title='연령대별 자살자 수 (2023년)',
        labels={'자살 사망자수': '자살자 수 (명)', '연령별(2)': '연령대'}
    )
    st.plotly_chart(fig, use_container_width=True)

    # 데이터 표시
    st.dataframe(filtered_df[['연령별(2)', '자살 사망자수']], use_container_width=True)
