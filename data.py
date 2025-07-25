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
        df = pd.read_csv(file_to_read, encoding='cp949', quoting=csv.QUOTE_NONE, on_bad_lines='skip')
        seoul_row = df.iloc[0]
        # 연령대 컬럼 필터링
        age_columns = [col for col in df.columns if '_계_' in col and any(str(i) in col or '100세 이상' in col for i in range(101))]
        age_columns_male = [col for col in df.columns if '_남_' in col and any(str(i) in col or '100세 이상' in col for i in range(101))]
        age_columns_female = [col for col in df.columns if '_여_' in col and any(str(i) in col or '100세 이상' in col for i in range(101))]
        
        ages = [col.split('_')[-1].replace('"', '') for col in age_columns]
        population_total = [int(str(seoul_row[col]).replace(" ", "").replace('"', '').replace(',', '')) for col in age_columns]
        population_male = [int(str(seoul_row[col]).replace(" ", "").replace('"', '').replace(',', '')) for col in age_columns_male]
        population_female = [int(str(seoul_row[col]).replace(" ", "").replace('"', '').replace(',', '')) for col in age_columns_female]

        tabs = st.tabs(["합계", "남", "여"])
        with tabs[0]:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=ages, y=population_total, name='서울특별시 합계'))
            fig.update_layout(
                title='서울특별시 연령별 인구 구조 (2025년 6월) - 합계',
                xaxis_title='연령',
                yaxis_title='인구 수',
                xaxis=dict(tickangle=45),
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
        with tabs[1]:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=ages, y=population_male, name='서울특별시 남자'))
            fig.update_layout(
                title='서울특별시 연령별 인구 구조 (2025년 6월) - 남',
                xaxis_title='연령',
                yaxis_title='인구 수',
                xaxis=dict(tickangle=45),
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
        with tabs[2]:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=ages, y=population_female, name='서울특별시 여자'))
            fig.update_layout(
                title='서울특별시 연령별 인구 구조 (2025년 6월) - 여',
                xaxis_title='연령',
                yaxis_title='인구 수',
                xaxis=dict(tickangle=45),
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"⚠️ 파일을 처리하는 중 오류가 발생했습니다: {e}")
else:
    st.info("CSV 파일이 존재하지 않습니다. 파일을 업로드하거나, 같은 폴더에 CSV 파일을 두세요.")
