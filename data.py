import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import csv

st.set_page_config(page_title="서울시 연령별 인구 시각화", layout="wide")

st.title("🧓 서울특별시 연령별 인구 (2025년 6월)")
st.write("출처: 통계청 | 단위: 명")

# 파일 업로드
uploaded_file = st.file_uploader("📂 CSV 파일 업로드 (남녀구분)", type="csv")

if uploaded_file:
    try:
        # CSV 파일 읽기
        df = pd.read_csv(uploaded_file, encoding='cp949', quoting=csv.QUOTE_NONE, on_bad_lines='skip')

        # 서울특별시 전체 인구 행 (보통 첫 번째 행)
        seoul_row = df.iloc[0]

        # 연령대 컬럼 필터링
        age_columns = [col for col in df.columns if '_계_' in col and any(str(i) in col or '100세 이상' in col for i in range(101))]

        # 연령/인구 데이터 정리
        ages = [col.split('_')[-1].replace('"', '') for col in age_columns]
        population = [int(str(seoul_row[col]).replace(" ", "").replace('"', '').replace(',', '')) for col in age_columns]

        # Plotly 그래프
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ages, y=population, mode='lines+markers', name='서울특별시'))

        fig.update_layout(
            title='서울특별시 연령별 인구 구조 (2025년 6월)',
            xaxis_title='연령',
            yaxis_title='인구 수',
            xaxis=dict(tickangle=45),
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ 파일을 처리하는 중 오류가 발생했습니다: {e}")
else:
    st.info("왼쪽 사이드바에서 CSV 파일을 업로드해 주세요.")
