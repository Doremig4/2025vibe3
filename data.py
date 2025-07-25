import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="자살률(연령별) 통계 시각화", layout="wide")
st.title("📊 자살률(연령별) 통계 시각화")
st.write("출처: 통계청 | 단위: 명, 10만명당 명")

# 업로드 없이 로컬 파일 자동 불러오기
csv_path = "자살률(연령별)_20250725130840.csv"
columns = ["연령별(1)", "연령별(2)", "자살 사망자수 (명)", "자살률 (10만명당 명)"]
df = pd.read_csv(csv_path, encoding='utf-8', skiprows=3, names=columns)
df = df.replace("-", pd.NA)
df["자살 사망자수 (명)"] = pd.to_numeric(df["자살 사망자수 (명)"], errors="coerce")
df["자살률 (10만명당 명)"] = pd.to_numeric(df["자살률 (10만명당 명)"], errors="coerce")
df = df[~df["연령별(2)"].isin(["미상", "소계"])]

st.subheader("📄 데이터 미리보기")
st.dataframe(df, use_container_width=True)

    # 컬럼 선택
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    all_cols = df.columns.tolist()

    if numeric_cols:
        st.subheader("📈 그래프 설정")
        chart_type = st.selectbox("차트 종류", ["선 그래프", "막대 그래프", "산점도"])

        x_axis = st.selectbox("X축 선택", all_cols)
        y_axis = st.multiselect("Y축 선택 (하나 이상)", numeric_cols, default=numeric_cols[:1])

        if x_axis and y_axis:
            for y in y_axis:
                if chart_type == "선 그래프":
                    fig = px.line(df, x=x_axis, y=y, title=f"{y} vs {x_axis}")
                elif chart_type == "막대 그래프":
                    fig = px.bar(df, x=x_axis, y=y, title=f"{y} vs {x_axis}")
                elif chart_type == "산점도":
                    fig = px.scatter(df, x=x_axis, y=y, title=f"{y} vs {x_axis}")

                st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("시각화할 수 있는 숫자형 컬럼이 없습니다.")
